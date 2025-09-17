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
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #f5f2ed;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #e8e2d5;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #f5f2ed;
        padding-top: 2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #5d4e37;
        font-weight: 600;
    }
    
    /* Kanban columns */
    .kanban-column {
        background-color: #faf8f5;
        border: 1px solid #d4c4a8;
        padding: 15px;
        border-radius: 8px;
        margin: 5px;
        min-height: 300px;
    }
    
    /* Task cards */
    .task-card {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 6px;
        margin: 8px 0;
        border-left: 4px solid #8b7355;
        box-shadow: 0 2px 4px rgba(93, 78, 55, 0.1);
        border: 1px solid #e6dcc6;
    }
    
    /* Priority-based card colors */
    .task-card-critical {
        border-left-color: #8b2635;
        background-color: #fdf8f8;
    }
    .task-card-high {
        border-left-color: #a0522d;
        background-color: #fdf9f5;
    }
    .task-card-medium {
        border-left-color: #b8860b;
        background-color: #fffdf5;
    }
    .task-card-low {
        border-left-color: #556b2f;
        background-color: #f8fdf5;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #faf8f5;
        border: 1px solid #d4c4a8;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #8b7355;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #5d4e37;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #faf8f5;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f5f2ed;
        color: #5d4e37;
    }
    
    /* Forms */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 1px solid #d4c4a8;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #d4c4a8;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        border: 1px solid #d4c4a8;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #f0f8f0;
        border: 1px solid #90c695;
    }
    
    .stError {
        background-color: #fdf2f2;
        border: 1px solid #e6a8a8;
    }
    
    .stInfo {
        background-color: #f0f4f8;
        border: 1px solid #a8c8e6;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #8b7355;
    }
</style>
""", unsafe_allow_html=True)

def get_mock_data():
    """Return mock data when API is not available"""
    return {
        "dashboard": {
            "total_integrations": 4,
            "stage_distribution": {"build": 2, "testing": 2, "research": 0, "launch": 0, "maintenance": 0},
            "task_statistics": {"pending": 3, "in_progress": 5, "completed": 2, "blocked": 0},
            "kanban_statistics": {"backlog": 1, "todo": 2, "in_progress": 3, "in_review": 1, "testing": 1, "done": 2, "blocked": 0},
            "priority_statistics": {"low": 0, "medium": 3, "high": 7, "critical": 0},
            "high_priority_tasks": 5,
            "overdue_tasks": 0,
            "story_points": {"total": 33, "completed": 4, "remaining": 29},
            "recent_updates": [
                {"integration": "F&I Express / Cox Automotive", "updated_at": "2025-09-17T14:07:35.525638+00:00", "stage": "testing", "active_tasks": 1},
                {"integration": "Provider Exchange Network (PEN)", "updated_at": "2025-09-17T14:07:35.525628+00:00", "stage": "testing", "active_tasks": 2},
                {"integration": "MenuMetric Integration", "updated_at": "2025-09-17T14:07:35.525614+00:00", "stage": "build", "active_tasks": 0},
                {"integration": "Vision Dealer API Integration", "updated_at": "2025-09-17T14:07:35.525584+00:00", "stage": "build", "active_tasks": 2}
            ]
        },
        "integrations": [
            {
                "id": "vision-dealer",
                "name": "Vision Dealer API Integration", 
                "company": "Vision Dealer Solutions",
                "stage": "build",
                "description": "API integration with Vision Dealer's new system, similar to PCMI specs",
                "contacts": [{"name": "Brandon Steup", "email": "brandon.steup@visiondealersolutions.com", "role": "Business Analyst", "company": "Vision Dealer Solutions"}],
                "tasks": [
                    {"id": "vd-001", "title": "Confirm latest communication status", "description": "Confirm the status of the latest communication with Brandon", "status": "in_progress", "kanban_status": "in_progress", "priority": "high", "task_type": "meeting", "assigned_to": "Ramisa", "story_points": 2, "sprint": "Sprint 1", "tags": ["communication", "status-check"]},
                    {"id": "vd-002", "title": "Deliver API documentation", "description": "Share API docs, test dealers, and products with Vision Dealer", "status": "in_progress", "kanban_status": "in_progress", "priority": "high", "task_type": "documentation", "assigned_to": "Sona Team", "story_points": 5, "sprint": "Sprint 1", "tags": ["documentation", "delivery"]},
                    {"id": "vd-003", "title": "Schedule follow-up meeting with Brandon", "description": "Set up regular check-ins to track progress", "status": "pending", "kanban_status": "todo", "priority": "medium", "task_type": "meeting", "assigned_to": "Ramisa", "story_points": 1, "sprint": "Sprint 1", "tags": ["meeting", "follow-up"]}
                ],
                "next_steps": ["Confirm current stage", "Deliver API documentation", "Schedule follow-up meeting"]
            },
            {
                "id": "menumetric",
                "name": "MenuMetric Integration",
                "company": "MenuMetric", 
                "stage": "build",
                "description": "Menu integration requiring eligibility guidelines and API documentation",
                "contacts": [{"name": "Hannah Honeybrook", "email": "hannah@menumetric.com", "role": "Integration Lead", "company": "MenuMetric"}],
                "tasks": [
                    {"id": "mm-001", "title": "Provide Eligibility Guidelines", "description": "Deliver eligibility guidelines to Hannah's team", "status": "pending", "kanban_status": "todo", "priority": "high", "task_type": "documentation", "assigned_to": "Sona Team", "story_points": 3, "sprint": "Sprint 1", "tags": ["guidelines", "delivery"]},
                    {"id": "mm-002", "title": "Provide Testing Dealer ID", "description": "Testing Dealer ID with ALL products enrolled", "status": "completed", "kanban_status": "done", "priority": "high", "task_type": "feature", "assigned_to": "Sona Team", "story_points": 2, "sprint": "Sprint 1", "tags": ["testing", "dealer-setup"]},
                    {"id": "mm-003", "title": "List of industries with products", "description": "Provide list of industries with associated products", "status": "pending", "kanban_status": "backlog", "priority": "medium", "task_type": "documentation", "assigned_to": "Sona Team", "story_points": 2, "sprint": "Sprint 2", "tags": ["documentation", "products"]}
                ],
                "next_steps": ["Complete delivery of remaining items", "Begin direct coordination", "Follow up on testing progress"]
            },
            {
                "id": "pen",
                "name": "Provider Exchange Network (PEN)",
                "company": "Provider Exchange Network",
                "stage": "testing", 
                "description": "Ongoing nullable fields support and API updates",
                "contacts": [
                    {"name": "Jason Malak", "email": "jmalak@providerexchangenetwork.com", "phone": "313-749-0469", "role": "Integration Manager", "company": "Provider Exchange Network"},
                    {"name": "Carl Ciaramitaro", "email": "cciaramitaro@providerexchangenetwork.com", "phone": "313-749-0943", "role": "", "company": "Provider Exchange Network"}
                ],
                "tasks": [
                    {"id": "pen-001", "title": "Validate BETA changes", "description": "Confirm BETA behavior for nullable/optional fields", "status": "in_progress", "kanban_status": "testing", "priority": "high", "task_type": "feature", "assigned_to": "PEN Team", "story_points": 5, "sprint": "Sprint 1", "tags": ["testing", "validation", "beta"]},
                    {"id": "pen-002", "title": "CreateContract nullable support", "description": "Complete CreateContract nullable support implementation", "status": "in_progress", "kanban_status": "in_progress", "priority": "high", "task_type": "feature", "assigned_to": "Sona Team", "story_points": 8, "sprint": "Sprint 1", "tags": ["development", "nullable-fields"]}
                ],
                "next_steps": ["Track delivery of latest API documentation", "Validate CreateContract once deployed", "Confirm all nullable field behavior"]
            },
            {
                "id": "fi-express",
                "name": "F&I Express / Cox Automotive",
                "company": "Cox Automotive",
                "stage": "testing",
                "description": "Integration with Cox Automotive team, addressing environment and token setup", 
                "contacts": [
                    {"name": "Katie Rupp", "email": "Kathrine.Rupp@coxautoinc.com", "role": "Technical Customer Care Analyst I – API", "company": "Cox Automotive"},
                    {"name": "Stephany Spiker", "email": "Stephany.Spiker@coxautoinc.com", "role": "", "company": "Cox Automotive"},
                    {"name": "Kerri Massura", "email": "Kerri.massura@coxautoinc.com", "role": "", "company": "Cox Automotive"}
                ],
                "tasks": [
                    {"id": "fi-001", "title": "Confirm environment/token setup", "description": "Clarify if one token used for both NonProd and Prod environments", "status": "in_progress", "kanban_status": "in_review", "priority": "medium", "task_type": "research", "assigned_to": "Katie Rupp", "story_points": 3, "sprint": "Sprint 1", "tags": ["environment", "authentication"]},
                    {"id": "fi-002", "title": "Resolve website maintenance issues", "description": "Ensure BETA environment is accessible after maintenance", "status": "completed", "kanban_status": "done", "priority": "high", "task_type": "bug", "assigned_to": "Sona Team", "story_points": 2, "sprint": "Sprint 1", "tags": ["maintenance", "environment"]}
                ],
                "next_steps": ["Confirm token setup requirements", "Provide availability timeline post-maintenance", "Send revised Coverage Surcharges documentation"]
            }
        ],
        "sprints": {
            "Sprint 1": {"total_tasks": 9, "completed_tasks": 2, "total_story_points": 31, "completed_story_points": 4},
            "Sprint 2": {"total_tasks": 2, "completed_tasks": 0, "total_story_points": 5, "completed_story_points": 0}
        }
    }

def make_api_request(endpoint, method="GET", data=None, params=None):
    """Make API request with error handling and fallback to mock data"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params, timeout=2)
        elif method == "POST":
            response = requests.post(url, json=data, params=params, timeout=2)
        elif method == "PUT":
            response = requests.put(url, json=data, params=params, timeout=2)
        elif method == "DELETE":
            response = requests.delete(url, timeout=2)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"API Error: {response.status_code} - Using demo data")
            return get_fallback_data(endpoint)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        st.info("Using demo data - API not available")
        return get_fallback_data(endpoint)
    except Exception as e:
        st.warning(f"Error: {str(e)} - Using demo data")
        return get_fallback_data(endpoint)

def get_fallback_data(endpoint):
    """Return appropriate mock data based on endpoint"""
    mock_data = get_mock_data()
    
    if endpoint == "/healthz":
        return {"status": "demo", "timestamp": datetime.now().isoformat()}
    elif endpoint == "/dashboard":
        return mock_data["dashboard"]
    elif endpoint == "/integrations":
        return mock_data["integrations"]
    elif endpoint == "/sprints":
        return mock_data["sprints"]
    elif endpoint.startswith("/integrations/") and endpoint.endswith("/kanban"):
        # Extract integration ID from endpoint
        integration_id = endpoint.split("/")[2]
        integration = next((i for i in mock_data["integrations"] if i["id"] == integration_id), mock_data["integrations"][0])
        
        # Organize tasks by Kanban status
        columns = {
            "backlog": [],
            "todo": [],
            "in_progress": [],
            "in_review": [],
            "testing": [],
            "done": [],
            "blocked": []
        }
        
        total_story_points = 0
        for task in integration["tasks"]:
            columns[task["kanban_status"]].append(task)
            total_story_points += task.get("story_points", 0)
        
        return {
            "integration_id": integration_id,
            "integration_name": integration["name"],
            "columns": columns,
            "total_tasks": len(integration["tasks"]),
            "total_story_points": total_story_points
        }
    else:
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

def get_task_type_label(task_type):
    """Get professional label for task type"""
    labels = {
        "feature": "[FEATURE]",
        "bug": "[BUG]",
        "documentation": "[DOCS]",
        "research": "[RESEARCH]",
        "meeting": "[MEETING]",
        "review": "[REVIEW]",
        "deployment": "[DEPLOY]"
    }
    return labels.get(task_type, "[TASK]")

def display_task_card(task, show_move_buttons=False, integration_id=None):
    """Display a task card with styling"""
    priority_class = f"task-card-{task['priority']}"
    
    with st.container():
        st.markdown(f"""
        <div class="task-card {priority_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>{get_task_type_label(task['task_type'])} {task['title']}</strong>
                <span style="background-color: {get_priority_color(task['priority'])}; color: white; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600;">
                    {task['priority'].upper()}
                </span>
            </div>
            <p style="margin: 10px 0; color: #5d4e37; line-height: 1.4;">{task['description']}</p>
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #8b7355;">
                <span><strong>Assigned:</strong> {task['assigned_to'] or 'Unassigned'}</span>
                <span><strong>Points:</strong> {task['story_points'] or 0}</span>
            </div>
            <div style="margin-top: 8px;">
                {"".join([f'<span style="background-color: #e8e2d5; color: #5d4e37; padding: 2px 8px; border-radius: 4px; font-size: 10px; margin-right: 6px; font-weight: 500;">#{tag}</span>' for tag in task['tags']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_move_buttons and integration_id:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Previous", key=f"move_left_{task['id']}", disabled=True):
                    st.info("Task movement disabled in demo mode")
            with col2:
                if st.button("View Details", key=f"details_{task['id']}"):
                    show_task_details(task)
            with col3:
                if st.button("Next →", key=f"move_right_{task['id']}", disabled=True):
                    st.info("Task movement disabled in demo mode")

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
    with st.expander(f"Task Details: {task['title']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {task['id']}")
            st.write(f"**Type:** {get_task_type_label(task['task_type'])} {task['task_type'].title()}")
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
    st.title("Workflow Dashboard")
    
    try:
        # Get dashboard data
        dashboard_data = make_api_request("/dashboard")
        if not dashboard_data:
            st.error("Unable to load dashboard data")
            return
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
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
        st.subheader("Stage Distribution")
        try:
            stage_data = dashboard_data['stage_distribution']
            # Filter out zero values
            filtered_stage_data = {k: v for k, v in stage_data.items() if v > 0}
            if filtered_stage_data:
                fig = px.pie(
                    values=list(filtered_stage_data.values()),
                    names=[name.title() for name in filtered_stage_data.keys()],
                    title="Integrations by Stage"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No stage data available")
        except Exception as e:
            st.error(f"Error creating stage chart: {str(e)}")
    
    with col2:
        st.subheader("Kanban Statistics")
        kanban_data = dashboard_data['kanban_statistics']
        if any(kanban_data.values()):
            try:
                # Create DataFrame for better handling
                columns = [k.replace('_', ' ').title() for k in kanban_data.keys()]
                values = list(kanban_data.values())
                
                fig = px.bar(
                    x=columns,
                    y=values,
                    title="Tasks by Kanban Column",
                    labels={'x': 'Kanban Column', 'y': 'Number of Tasks'}
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
                # Fallback: simple table
                st.table(pd.DataFrame([
                    {'Column': k.replace('_', ' ').title(), 'Tasks': v} 
                    for k, v in kanban_data.items()
                ]))
        else:
            st.info("No Kanban data available")
    
    # Recent Updates
    st.subheader("Recent Updates")
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
    st.title("Kanban Board")
    
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
    
    st.subheader(f"Project: {kanban_data['integration_name']}")
    
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
        'backlog': 'Backlog',
        'todo': 'To Do', 
        'in_progress': 'In Progress',
        'in_review': 'In Review',
        'testing': 'Testing',
        'done': 'Done',
        'blocked': 'Blocked'
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
    st.title("Integration Projects")
    
    # Get integrations
    integrations = make_api_request("/integrations")
    if not integrations:
        return
    
    # Display integrations
    for integration in integrations:
        with st.expander(f"{integration['name']} - {integration['company']}", expanded=False):
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
    st.title("Add New Task")
    st.info("Demo Mode - Task creation is simulated for demonstration")
    
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
                    st.success(f"Task '{title}' created successfully!")
                    st.json(result)

def analytics_page():
    """Analytics and reporting page"""
    st.title("Analytics & Reporting")
    
    try:
        # Get dashboard and sprint data
        dashboard_data = make_api_request("/dashboard")
        sprints_data = make_api_request("/sprints")
        
        if not dashboard_data:
            st.error("Unable to load analytics data")
            return
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
        return
    
    # Sprint Analytics
    if sprints_data:
        st.subheader("Sprint Performance")
        
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
        
        if not sprint_df.empty:
            try:
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
                fig.update_layout(yaxis_tickformat=".1%")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating sprint charts: {str(e)}")
                # Fallback: show data as table
                st.table(sprint_df)
        else:
            st.info("No sprint data available")
    
    # Priority Distribution
    st.subheader("Priority Distribution")
    try:
        priority_data = dashboard_data['priority_statistics']
        
        if any(priority_data.values()):
            # Filter out zero values for better visualization
            filtered_data = {k: v for k, v in priority_data.items() if v > 0}
            if filtered_data:
                fig = px.pie(
                    values=list(filtered_data.values()),
                    names=[name.title() for name in filtered_data.keys()],
                    title="Tasks by Priority",
                    color_discrete_map={
                        "Critical": "#dc3545",
                        "High": "#fd7e14",
                        "Medium": "#ffc107", 
                        "Low": "#28a745"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No priority data available")
        else:
            st.info("No priority data available")
    except Exception as e:
        st.error(f"Error creating priority chart: {str(e)}")
        # Fallback: show priority data as metrics
        try:
            priority_data = dashboard_data.get('priority_statistics', {})
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Critical", priority_data.get('critical', 0))
            with col2:
                st.metric("High", priority_data.get('high', 0))
            with col3:
                st.metric("Medium", priority_data.get('medium', 0))
            with col4:
                st.metric("Low", priority_data.get('low', 0))
        except:
            st.info("Priority data unavailable")
    
    # Story Points Progress
    st.subheader("Story Points Progress")
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
    st.sidebar.title("Workflow Management System")
    
    # Check API connection
    health_check = make_api_request("/healthz")
    if health_check and health_check.get("status") != "demo":
        st.sidebar.success("API Connected")
        api_mode = "live"
    else:
        st.sidebar.info("Demo Mode")
        st.sidebar.caption("Using sample data for demonstration")
        api_mode = "demo"
    
    # Navigation
    pages = {
        "Dashboard": dashboard_page,
        "Kanban Board": kanban_board_page,
        "Integration Projects": integrations_page,
        "Add Task": add_task_page,
        "Analytics": analytics_page
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    # API Status in sidebar
    st.sidebar.markdown("---")
    if api_mode == "live":
        st.sidebar.markdown("### API Status")
        st.sidebar.write(f"**Server Time:** {health_check.get('timestamp', 'Unknown')}")
    else:
        st.sidebar.markdown("### System Status")
        st.sidebar.write("**Mode:** Demo")
        st.sidebar.write("**Data:** Sample workflow data")
        st.sidebar.write("**Features:** Full functionality demo")
        st.sidebar.caption("To use with live data, connect to FastAPI backend")
    
    # Run selected page
    pages[selected_page]()

if __name__ == "__main__":
    main()
