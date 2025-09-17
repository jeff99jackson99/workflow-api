# 🚀 Complete Streamlit App Details

## 📋 Application Overview

**File**: `streamlit_app.py` (21,468 bytes)
**Purpose**: Interactive web interface for workflow management with Kanban boards
**Technology Stack**: Streamlit + Plotly + Pandas + Requests

---

## 🏗️ Code Structure & Components

### **1. Core Imports & Configuration**
```python
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
```

### **2. API Configuration**
```python
API_BASE_URL = "http://localhost:8000"  # FastAPI backend URL
```

### **3. Custom CSS Styling**
```python
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
    .task-card-high { border-left-color: #dc3545; }
    .task-card-medium { border-left-color: #ffc107; }
    .task-card-low { border-left-color: #28a745; }
</style>
""", unsafe_allow_html=True)
```

---

## 🔧 Core Functions

### **API Communication**
```python
def make_api_request(endpoint, method="GET", data=None, params=None):
    """
    Make API request with comprehensive error handling
    
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, PUT, DELETE)
        data: JSON data for POST/PUT requests
        params: Query parameters
        
    Returns:
        JSON response or None on error
    """
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
        st.error("🔌 Cannot connect to API. Please ensure the FastAPI server is running")
        st.info("Run: `make dev` or `python3 -m src.app`")
        return None
```

### **UI Helper Functions**
```python
def get_priority_color(priority):
    """Get color based on task priority"""
    colors = {
        "critical": "#dc3545",  # Red
        "high": "#fd7e14",      # Orange
        "medium": "#ffc107",    # Yellow
        "low": "#28a745"        # Green
    }
    return colors.get(priority, "#6c757d")

def get_task_type_emoji(task_type):
    """Get emoji for different task types"""
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
```

### **Task Card Display**
```python
def display_task_card(task, show_move_buttons=False, integration_id=None):
    """
    Display a beautifully formatted task card
    
    Features:
    - Priority color coding
    - Task type emojis
    - Assignee and story points
    - Tags as badges
    - Optional move buttons
    """
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
```

---

## 📱 Page Functions Detail

### **1. Dashboard Page** (`dashboard_page()`)

**Purpose**: Main overview with metrics and charts

**Features**:
- **4 Key Metrics**: Total integrations, active tasks, high priority, story points
- **Interactive Charts**: Stage distribution (pie), Kanban statistics (bar)
- **Recent Updates**: Timeline of integration activity

**Code Structure**:
```python
def dashboard_page():
    st.title("📊 Workflow Dashboard")
    
    # Get dashboard data from API
    dashboard_data = make_api_request("/dashboard")
    
    # Key Metrics Row (4 columns)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Integrations", dashboard_data['total_integrations'])
    # ... more metrics
    
    # Charts Row (2 columns)
    col1, col2 = st.columns(2)
    with col1:
        # Stage distribution pie chart
        fig = px.pie(values=..., names=..., title="Integrations by Stage")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Updates List
    for update in dashboard_data.get('recent_updates', []):
        # Display update information
```

### **2. Kanban Board Page** (`kanban_board_page()`)

**Purpose**: Interactive Kanban board with task management

**Features**:
- **7 Kanban Columns**: Backlog → To Do → In Progress → In Review → Testing → Done → Blocked
- **Task Movement**: Left/Right buttons to move tasks
- **Sprint Filtering**: Filter by specific sprint
- **Task Details**: Expandable task information

**Code Structure**:
```python
def kanban_board_page():
    st.title("📋 Kanban Board")
    
    # Integration selector
    integrations = make_api_request("/integrations")
    selected_integration_id = st.selectbox("Select Integration", ...)
    
    # Sprint filter
    sprints_data = make_api_request("/sprints")
    selected_sprint = st.selectbox("Filter by Sprint", ...)
    
    # Get Kanban data
    kanban_data = make_api_request(f"/integrations/{integration_id}/kanban")
    
    # Display 7 columns in grid
    cols = st.columns(7)
    column_names = {
        'backlog': '📝 Backlog',
        'todo': '📋 To Do',
        'in_progress': '⚡ In Progress',
        'in_review': '👀 In Review',
        'testing': '🧪 Testing',
        'done': '✅ Done',
        'blocked': '🚫 Blocked'
    }
    
    for idx, (status, title) in enumerate(column_names.items()):
        with cols[idx]:
            st.markdown(f"### {title}")
            for task in columns[status]:
                display_task_card(task, show_move_buttons=True, integration_id=integration_id)
```

### **3. Integrations Page** (`integrations_page()`)

**Purpose**: Overview of all integration projects

**Features**:
- **Expandable Cards**: Each integration in a collapsible section
- **Contact Information**: All stakeholder details
- **Progress Tracking**: Task summaries and completion rates
- **Next Steps**: AI-generated recommendations

**Code Structure**:
```python
def integrations_page():
    st.title("🤝 Integrations")
    
    integrations = make_api_request("/integrations")
    
    for integration in integrations:
        with st.expander(f"🏢 {integration['name']} - {integration['company']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Stage:** {integration['stage'].title()}")
                st.write(f"**Description:** {integration['description']}")
                
                # Display contacts
                if integration['contacts']:
                    st.write("**Contacts:**")
                    for contact in integration['contacts']:
                        st.write(f"- {contact['name']} ({contact['email']})")
            
            with col2:
                # Task metrics and progress bar
                tasks = integration['tasks']
                total_tasks = len(tasks)
                completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
                progress = completed_tasks / total_tasks if total_tasks > 0 else 0
                st.progress(progress)
```

### **4. Add Task Page** (`add_task_page()`)

**Purpose**: Form to create new tasks

**Features**:
- **Complete Task Form**: All task properties
- **Integration Selection**: Choose which project
- **Validation**: Required fields checking
- **Success Feedback**: Confirmation of task creation

**Code Structure**:
```python
def add_task_page():
    st.title("➕ Add New Task")
    
    integrations = make_api_request("/integrations")
    
    with st.form("add_task_form"):
        # Integration selection
        selected_integration_id = st.selectbox("Integration *", ...)
        
        # Task details in columns
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Task Title *")
            task_type = st.selectbox("Task Type", ["feature", "bug", "documentation", ...])
            priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
            assigned_to = st.text_input("Assigned To")
        
        with col2:
            story_points = st.number_input("Story Points", min_value=0, max_value=20)
            sprint = st.text_input("Sprint")
            reporter = st.text_input("Reporter")
            due_date = st.date_input("Due Date (optional)")
        
        description = st.text_area("Description *")
        tags = st.text_input("Tags (comma-separated)")
        
        submitted = st.form_submit_button("Create Task")
        
        if submitted:
            # Validation and API call
            task_data = {
                "title": title,
                "description": description,
                # ... other fields
            }
            result = make_api_request(f"/integrations/{integration_id}/tasks", 
                                    method="POST", data=task_data)
```

### **5. Analytics Page** (`analytics_page()`)

**Purpose**: Performance analytics and reporting

**Features**:
- **Sprint Analytics**: Task and story point completion by sprint
- **Priority Distribution**: Visual breakdown of task priorities
- **Velocity Tracking**: Team performance over time
- **Progress Visualization**: Story points progress

**Code Structure**:
```python
def analytics_page():
    st.title("📈 Analytics")
    
    dashboard_data = make_api_request("/dashboard")
    sprints_data = make_api_request("/sprints")
    
    # Sprint Analytics
    if sprints_data:
        sprint_df = pd.DataFrame([
            {
                "Sprint": sprint,
                "Total Tasks": data["total_tasks"],
                "Completed Tasks": data["completed_tasks"],
                "Completion Rate": data["completed_tasks"] / data["total_tasks"]
            }
            for sprint, data in sprints_data.items()
        ])
        
        # Charts
        fig = px.bar(sprint_df, x="Sprint", y=["Total Tasks", "Completed Tasks"])
        st.plotly_chart(fig, use_container_width=True)
    
    # Priority Distribution
    priority_data = dashboard_data['priority_statistics']
    fig = px.pie(values=list(priority_data.values()), names=list(priority_data.keys()))
    st.plotly_chart(fig, use_container_width=True)
```

---

## 🎯 Task Movement Functions

### **Move Task Left/Right**
```python
def move_task_left(integration_id, task_id, current_status):
    """Move task to previous Kanban column"""
    status_order = ["backlog", "todo", "in_progress", "in_review", "testing", "done", "blocked"]
    try:
        current_index = status_order.index(current_status)
        if current_index > 0:
            new_status = status_order[current_index - 1]
            result = make_api_request(f"/integrations/{integration_id}/tasks/{task_id}/move", 
                                    method="PUT", params={"new_status": new_status})
            if result:
                st.success(f"Task moved to {new_status.replace('_', ' ').title()}")
                st.rerun()  # Refresh the page
    except ValueError:
        st.error("Invalid status")

def move_task_right(integration_id, task_id, current_status):
    """Move task to next Kanban column"""
    # Similar logic but moves forward in the status_order
```

### **Task Details Modal**
```python
def show_task_details(task):
    """Show detailed task information in expandable section"""
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
        
        if task['comments']:
            st.write("**Comments:**")
            for comment in task['comments']:
                st.write(f"- {comment['author']}: {comment['content']}")
```

---

## 🎨 Visual Design System

### **Color Scheme**
```python
# Priority Colors
PRIORITY_COLORS = {
    "critical": "#dc3545",  # Red
    "high": "#fd7e14",      # Orange  
    "medium": "#ffc107",    # Yellow
    "low": "#28a745"        # Green
}

# Task Type Emojis
TASK_EMOJIS = {
    "feature": "⭐",
    "bug": "🐛", 
    "documentation": "📖",
    "research": "🔍",
    "meeting": "🤝",
    "review": "👀",
    "deployment": "🚀"
}
```

### **Layout Structure**
- **Wide Layout**: Maximizes screen real estate
- **Sidebar Navigation**: Persistent menu for page switching
- **Column Layouts**: Responsive grid system
- **Card Design**: Modern card-based UI with shadows and borders

---

## 📊 Data Integration

### **API Endpoints Used**
```python
# Dashboard data
GET /dashboard

# Integration management
GET /integrations
GET /integrations/{id}
POST /integrations

# Kanban board
GET /integrations/{id}/kanban
PUT /integrations/{id}/tasks/{task_id}/move

# Task management  
POST /integrations/{id}/tasks
PUT /integrations/{id}/tasks/{task_id}
POST /integrations/{id}/tasks/{task_id}/comments

# Analytics
GET /sprints
```

### **Data Flow**
1. **Streamlit** makes HTTP requests to **FastAPI** backend
2. **FastAPI** returns JSON data
3. **Streamlit** processes data with **Pandas**
4. **Plotly** creates interactive charts
5. **Custom CSS** styles the interface

---

## 🚀 Main Application Entry Point

```python
def main():
    """Main Streamlit app with navigation"""
    st.sidebar.title("🚀 Workflow Management")
    
    # API connection check
    health_check = make_api_request("/healthz")
    if health_check:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Disconnected")
        st.sidebar.info("Start the API server with: `make dev`")
    
    # Navigation menu
    pages = {
        "📊 Dashboard": dashboard_page,
        "📋 Kanban Board": kanban_board_page,
        "🤝 Integrations": integrations_page,
        "➕ Add Task": add_task_page,
        "📈 Analytics": analytics_page
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    # Run selected page function
    pages[selected_page]()

if __name__ == "__main__":
    main()
```

---

## 🔧 Running the Application

### **Prerequisites**
```bash
# Install dependencies
python3 -m pip install --user streamlit plotly pandas requests
```

### **Start Commands**
```bash
# Terminal 1: FastAPI Backend
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m src.app

# Terminal 2: Streamlit Frontend  
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m streamlit run streamlit_app.py
```

### **Access URLs**
- **Streamlit App**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📱 User Experience Features

### **Real-time Updates**
- **Auto-refresh**: Page reloads after task movements
- **Live Data**: Always shows current state from API
- **Error Handling**: Graceful fallbacks and user-friendly messages

### **Interactive Elements**
- **Clickable Buttons**: Move tasks, view details, create tasks
- **Form Validation**: Required field checking
- **Visual Feedback**: Success/error messages and progress indicators
- **Responsive Design**: Works on different screen sizes

### **Navigation**
- **Sidebar Menu**: Persistent navigation
- **Page State**: Maintains selections across interactions
- **Breadcrumbs**: Clear indication of current location

Your Streamlit app provides a complete, professional workflow management interface with all the features needed to manage your integration projects effectively! 🚀
