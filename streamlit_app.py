"""
Streamlit Web Interface for Workflow API
A comprehensive Kanban-style workflow management system
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Workflow Management System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
<style>
    .kanban-column {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        min-height: 300px;
    }
    .task-card {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .task-card-high {
        border-left-color: #dc3545;
    }
    .task-card-medium {
        border-left-color: #ffc107;
    }
    .task-card-low {
        border-left-color: #28a745;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint, method="GET", data=None, params=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, params=params)
        elif method == "PUT":
            response = requests.put(url, json=data, params=params)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API. Please ensure the FastAPI server is running on http://localhost:8000")
        st.info("Run: `make dev` or `python3 -m src.app` in your project directory")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def get_priority_color(priority):
    """Get color based on priority"""
    colors = {
        "critical": "#dc3545",
        "high": "#fd7e14", 
        "medium": "#ffc107",
        "low": "#28a745"
    }
    return colors.get(priority, "#6c757d")

def get_task_type_emoji(task_type):
    """Get emoji for task type"""
    emojis = {
        "feature": "⭐",
        "bug": "🐛",
        "documentation": "📖",
        "research": "🔍",
        "meeting": "🤝",
        "review": "👀",
        "deployment": "🚀"
    }
    return emojis.get(task_type, "📝")

def display_task_card(task, show_move_buttons=False, integration_id=None):
    """Display a task card with styling"""
    priority_class = f"task-card-{task['priority']}"
    
    with st.container():
        st.markdown(f"""
        <div class="task-card {priority_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>{get_task_type_emoji(task['task_type'])} {task['title']}</strong>
                <span style="background-color: {get_priority_color(task['priority'])}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                    {task['priority'].upper()}
                </span>
            </div>
            <p style="margin: 8px 0; color: #666;">{task['description']}</p>
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888;">
                <span>👤 {task['assigned_to'] or 'Unassigned'}</span>
                <span>📊 {task['story_points'] or 0} pts</span>
            </div>
            <div style="margin-top: 5px;">
                {"".join([f'<span style="background-color: #e9ecef; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-right: 4px;">#{tag}</span>' for tag in task['tags']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_move_buttons and integration_id:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"⬅️ Move", key=f"move_left_{task['id']}"):
                    move_task_left(integration_id, task['id'], task['kanban_status'])
            with col2:
                if st.button(f"ℹ️ Details", key=f"details_{task['id']}"):
                    show_task_details(task)
            with col3:
                if st.button(f"➡️ Move", key=f"move_right_{task['id']}"):
                    move_task_right(integration_id, task['id'], task['kanban_status'])

def move_task_left(integration_id, task_id, current_status):
    """Move task to previous column"""
    status_order = ["backlog", "todo", "in_progress", "in_review", "testing", "done", "blocked"]
    try:
        current_index = status_order.index(current_status)
        if current_index > 0:
            new_status = status_order[current_index - 1]
            result = make_api_request(f"/integrations/{integration_id}/tasks/{task_id}/move", 
                                    method="PUT", params={"new_status": new_status})
            if result:
                st.success(f"Task moved to {new_status.replace('_', ' ').title()}")
                st.rerun()
    except ValueError:
        st.error("Invalid status")

def move_task_right(integration_id, task_id, current_status):
    """Move task to next column"""
    status_order = ["backlog", "todo", "in_progress", "in_review", "testing", "done", "blocked"]
    try:
        current_index = status_order.index(current_status)
        if current_index < len(status_order) - 1:
            new_status = status_order[current_index + 1]
            result = make_api_request(f"/integrations/{integration_id}/tasks/{task_id}/move", 
                                    method="PUT", params={"new_status": new_status})
            if result:
                st.success(f"Task moved to {new_status.replace('_', ' ').title()}")
                st.rerun()
    except ValueError:
        st.error("Invalid status")

def show_task_details(task):
    """Show detailed task information in a modal"""
    with st.expander(f"📋 Task Details: {task['title']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {task['id']}")
            st.write(f"**Type:** {get_task_type_emoji(task['task_type'])} {task['task_type'].title()}")
            st.write(f"**Priority:** {task['priority'].title()}")
            st.write(f"**Status:** {task['kanban_status'].replace('_', ' ').title()}")
            
        with col2:
            st.write(f"**Assigned to:** {task['assigned_to'] or 'Unassigned'}")
            st.write(f"**Reporter:** {task['reporter'] or 'Unknown'}")
            st.write(f"**Story Points:** {task['story_points'] or 0}")
            st.write(f"**Sprint:** {task['sprint'] or 'No sprint'}")
        
        st.write(f"**Description:** {task['description']}")
        
        if task['tags']:
            st.write(f"**Tags:** {', '.join(task['tags'])}")
        
        if task['comments']:
            st.write("**Comments:**")
            for comment in task['comments']:
                st.write(f"- {comment['author']}: {comment['content']}")

def dashboard_page():
    """Main dashboard page"""
    st.title("📊 Workflow Dashboard")
    
    # Get dashboard data
    dashboard_data = make_api_request("/dashboard")
    if not dashboard_data:
        return
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Integrations",
            value=dashboard_data['total_integrations']
        )
    
    with col2:
        st.metric(
            label="Active Tasks",
            value=dashboard_data['task_statistics']['in_progress']
        )
    
    with col3:
        st.metric(
            label="High Priority Tasks",
            value=dashboard_data['high_priority_tasks']
        )
    
    with col4:
        st.metric(
            label="Story Points Remaining",
            value=dashboard_data['story_points']['remaining']
        )
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Stage Distribution")
        stage_data = dashboard_data['stage_distribution']
        if any(stage_data.values()):
            fig = px.pie(
                values=list(stage_data.values()),
                names=[name.title() for name in stage_data.keys()],
                title="Integrations by Stage"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Kanban Statistics")
        kanban_data = dashboard_data['kanban_statistics']
        if any(kanban_data.values()):
            fig = px.bar(
                x=list(kanban_data.keys()),
                y=list(kanban_data.values()),
                title="Tasks by Kanban Column",
                labels={'x': 'Kanban Column', 'y': 'Number of Tasks'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Updates
    st.subheader("🔄 Recent Updates")
    recent_updates = dashboard_data.get('recent_updates', [])
    
    for update in recent_updates:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"**{update['integration']}**")
            with col2:
                st.write(f"Stage: {update['stage'].title()}")
            with col3:
                st.write(f"Active: {update['active_tasks']} tasks")
            with col4:
                updated_time = datetime.fromisoformat(update['updated_at'].replace('Z', '+00:00'))
                st.write(f"{updated_time.strftime('%m/%d %H:%M')}")

def kanban_board_page():
    """Kanban board page"""
    st.title("📋 Kanban Board")
    
    # Get integrations
    integrations = make_api_request("/integrations")
    if not integrations:
        return
    
    # Integration selector
    integration_names = {i['id']: f"{i['name']} ({i['company']})" for i in integrations}
    selected_integration_id = st.selectbox(
        "Select Integration",
        options=list(integration_names.keys()),
        format_func=lambda x: integration_names[x]
    )
    
    if not selected_integration_id:
        return
    
    # Sprint filter
    sprints_data = make_api_request("/sprints")
    if sprints_data:
        sprint_options = ["All Sprints"] + list(sprints_data.keys())
        selected_sprint = st.selectbox("Filter by Sprint", sprint_options)
        sprint_param = None if selected_sprint == "All Sprints" else selected_sprint
    else:
        sprint_param = None
    
    # Get Kanban board data
    params = {"sprint": sprint_param} if sprint_param else None
    kanban_data = make_api_request(f"/integrations/{selected_integration_id}/kanban", params=params)
    
    if not kanban_data:
        return
    
    st.subheader(f"🎯 {kanban_data['integration_name']}")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", kanban_data['total_tasks'])
    with col2:
        st.metric("Total Story Points", kanban_data['total_story_points'])
    with col3:
        if sprint_param:
            st.info(f"Showing: {sprint_param}")
        else:
            st.info("Showing: All Tasks")
    
    # Kanban columns
    columns = kanban_data['columns']
    column_names = {
        'backlog': '📝 Backlog',
        'todo': '📋 To Do', 
        'in_progress': '⚡ In Progress',
        'in_review': '👀 In Review',
        'testing': '🧪 Testing',
        'done': '✅ Done',
        'blocked': '🚫 Blocked'
    }
    
    # Display columns in a grid
    cols = st.columns(len(column_names))
    
    for idx, (status, title) in enumerate(column_names.items()):
        with cols[idx]:
            st.markdown(f"### {title}")
            st.markdown(f"**{len(columns[status])} tasks**")
            
            # Display tasks in this column
            for task in columns[status]:
                display_task_card(task, show_move_buttons=True, integration_id=selected_integration_id)

def integrations_page():
    """Integrations management page"""
    st.title("🤝 Integrations")
    
    # Get integrations
    integrations = make_api_request("/integrations")
    if not integrations:
        return
    
    # Display integrations
    for integration in integrations:
        with st.expander(f"🏢 {integration['name']} - {integration['company']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Stage:** {integration['stage'].title()}")
                st.write(f"**Description:** {integration['description']}")
                
                # Contacts
                if integration['contacts']:
                    st.write("**Contacts:**")
                    for contact in integration['contacts']:
                        st.write(f"- {contact['name']} ({contact['email']}) - {contact.get('role', 'N/A')}")
                
                # Next steps
                if integration['next_steps']:
                    st.write("**Next Steps:**")
                    for step in integration['next_steps']:
                        st.write(f"- {step}")
            
            with col2:
                # Task summary
                tasks = integration['tasks']
                total_tasks = len(tasks)
                completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
                in_progress_tasks = len([t for t in tasks if t['status'] == 'in_progress'])
                
                st.metric("Total Tasks", total_tasks)
                st.metric("Completed", completed_tasks)
                st.metric("In Progress", in_progress_tasks)
                
                # Progress bar
                if total_tasks > 0:
                    progress = completed_tasks / total_tasks
                    st.progress(progress)
                    st.write(f"{progress:.1%} Complete")

def add_task_page():
    """Add new task page"""
    st.title("➕ Add New Task")
    
    # Get integrations
    integrations = make_api_request("/integrations")
    if not integrations:
        return
    
    # Form to add new task
    with st.form("add_task_form"):
        st.subheader("Task Details")
        
        # Integration selection
        integration_names = {i['id']: f"{i['name']} ({i['company']})" for i in integrations}
        selected_integration_id = st.selectbox(
            "Integration *",
            options=list(integration_names.keys()),
            format_func=lambda x: integration_names[x]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Task Title *")
            task_type = st.selectbox("Task Type", 
                                   ["feature", "bug", "documentation", "research", "meeting", "review", "deployment"])
            priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
            assigned_to = st.text_input("Assigned To")
        
        with col2:
            story_points = st.number_input("Story Points", min_value=0, max_value=20, value=1)
            sprint = st.text_input("Sprint (e.g., Sprint 2)")
            reporter = st.text_input("Reporter")
            due_date = st.date_input("Due Date (optional)")
        
        description = st.text_area("Description *")
        tags = st.text_input("Tags (comma-separated)")
        
        submitted = st.form_submit_button("Create Task")
        
        if submitted:
            if not title or not description:
                st.error("Title and description are required!")
            else:
                # Prepare task data
                task_data = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "task_type": task_type,
                    "assigned_to": assigned_to if assigned_to else None,
                    "reporter": reporter if reporter else None,
                    "story_points": story_points if story_points > 0 else None,
                    "sprint": sprint if sprint else None,
                    "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                    "due_date": due_date.isoformat() if due_date else None
                }
                
                # Create task
                result = make_api_request(f"/integrations/{selected_integration_id}/tasks", 
                                        method="POST", data=task_data)
                
                if result:
                    st.success(f"✅ Task '{title}' created successfully!")
                    st.json(result)

def analytics_page():
    """Analytics and reporting page"""
    st.title("📈 Analytics")
    
    # Get dashboard and sprint data
    dashboard_data = make_api_request("/dashboard")
    sprints_data = make_api_request("/sprints")
    
    if not dashboard_data:
        return
    
    # Sprint Analytics
    if sprints_data:
        st.subheader("🏃‍♂️ Sprint Analytics")
        
        sprint_df = pd.DataFrame([
            {
                "Sprint": sprint,
                "Total Tasks": data["total_tasks"],
                "Completed Tasks": data["completed_tasks"], 
                "Total Story Points": data["total_story_points"],
                "Completed Story Points": data["completed_story_points"],
                "Completion Rate": data["completed_tasks"] / data["total_tasks"] if data["total_tasks"] > 0 else 0
            }
            for sprint, data in sprints_data.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(sprint_df, x="Sprint", y=["Total Tasks", "Completed Tasks"],
                        title="Tasks by Sprint", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(sprint_df, x="Sprint", y=["Total Story Points", "Completed Story Points"],
                        title="Story Points by Sprint", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        
        # Sprint completion rates
        fig = px.line(sprint_df, x="Sprint", y="Completion Rate", 
                     title="Sprint Completion Rate", markers=True)
        fig.update_yaxis(tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)
    
    # Priority Distribution
    st.subheader("⚡ Priority Distribution")
    priority_data = dashboard_data['priority_statistics']
    
    if any(priority_data.values()):
        fig = px.pie(
            values=list(priority_data.values()),
            names=[name.title() for name in priority_data.keys()],
            title="Tasks by Priority",
            color_discrete_map={
                "Critical": "#dc3545",
                "High": "#fd7e14",
                "Medium": "#ffc107", 
                "Low": "#28a745"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Story Points Progress
    st.subheader("📊 Story Points Progress")
    story_points = dashboard_data['story_points']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Story Points", story_points['total'])
    with col2:
        st.metric("Completed", story_points['completed'])
    with col3:
        st.metric("Remaining", story_points['remaining'])
    
    # Progress visualization
    if story_points['total'] > 0:
        progress = story_points['completed'] / story_points['total']
        st.progress(progress)
        st.write(f"Overall Progress: {progress:.1%}")

def main():
    """Main Streamlit app"""
    st.sidebar.title("🚀 Workflow Management")
    
    # Check API connection
    health_check = make_api_request("/healthz")
    if health_check:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Disconnected")
        st.sidebar.info("Start the API server with: `make dev`")
    
    # Navigation
    pages = {
        "📊 Dashboard": dashboard_page,
        "📋 Kanban Board": kanban_board_page,
        "🤝 Integrations": integrations_page,
        "➕ Add Task": add_task_page,
        "📈 Analytics": analytics_page
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    # API Status in sidebar
    if health_check:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📡 API Status")
        st.sidebar.write(f"**Server Time:** {health_check.get('timestamp', 'Unknown')}")
    
    # Run selected page
    pages[selected_page]()

if __name__ == "__main__":
    main()
