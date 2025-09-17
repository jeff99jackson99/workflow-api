# 🚀 Streamlit App Setup Guide

## Complete Setup Instructions for Workflow Management Streamlit App

### 📋 Prerequisites
- Python 3.9+ installed
- FastAPI backend running on port 8000
- All dependencies installed

### 🛠️ Step-by-Step Setup

#### 1. **Install Dependencies**
```bash
cd "/Users/jeffjackson/Desktop/Project for workflow api"

# Install all required packages
python3 -m pip install --user streamlit plotly pandas requests fastapi uvicorn pydantic
```

#### 2. **Verify Installation**
```bash
# Check Streamlit version
python3 -m streamlit --version

# Should output: Streamlit, version 1.49.1 (or newer)
```

#### 3. **Start the Backend API** (Required!)
```bash
# Terminal 1 - Start FastAPI backend
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m src.app

# Should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 4. **Start Streamlit App**
```bash
# Terminal 2 - Start Streamlit (keep backend running)
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m streamlit run streamlit_app.py

# Or use the Makefile:
make streamlit
```

#### 5. **Access the Application**
- **Streamlit Web UI**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🖥️ Streamlit App Features

### **📊 Dashboard Page**
- **Real-time Metrics**: 
  - Total integrations: 4
  - Active tasks: 5
  - High priority tasks: 5
  - Story points remaining: 29

- **Interactive Charts**:
  - Stage distribution pie chart
  - Kanban column bar chart
  - Recent activity timeline

### **📋 Kanban Board**
- **7 Interactive Columns**:
  - 📝 Backlog
  - 📋 To Do
  - ⚡ In Progress
  - 👀 In Review
  - 🧪 Testing
  - ✅ Done
  - 🚫 Blocked

- **Task Management**:
  - Color-coded priority cards
  - Move tasks with ⬅️➡️ buttons
  - View task details with ℹ️ button
  - Sprint filtering dropdown

### **🤝 Integrations**
- **4 Pre-loaded Integrations**:
  - Vision Dealer (Build stage)
  - MenuMetric (Build stage)
  - PEN (Testing stage)
  - F&I Express (Testing stage)

- **Features**:
  - Expandable integration cards
  - Contact information display
  - Progress bars and metrics
  - Next steps recommendations

### **➕ Add Task**
- **Complete Form**:
  - Integration selection
  - Task title and description
  - Priority: Low, Medium, High, Critical
  - Task type: Feature, Bug, Documentation, Research, Meeting, Review, Deployment
  - Story points (0-20)
  - Sprint assignment
  - Assignee and reporter
  - Tags (comma-separated)
  - Due date picker

### **📈 Analytics**
- **Sprint Analytics**:
  - Task completion by sprint
  - Story points velocity
  - Completion rate trends

- **Visual Charts**:
  - Bar charts for sprint progress
  - Line charts for completion rates
  - Pie charts for priority distribution

---

## 🎨 Streamlit App Code Structure

### **Main Components**

#### **1. API Integration Functions**
```python
def make_api_request(endpoint, method="GET", data=None, params=None):
    """Make API request with error handling"""
    # Handles all API communication with FastAPI backend
```

#### **2. UI Helper Functions**
```python
def get_priority_color(priority):
    """Get color based on priority"""
    # Returns colors: Critical=red, High=orange, Medium=yellow, Low=green

def get_task_type_emoji(task_type):
    """Get emoji for task type"""
    # Returns emojis: Feature=⭐, Bug=🐛, Documentation=📖, etc.

def display_task_card(task, show_move_buttons=False, integration_id=None):
    """Display a task card with styling"""
    # Creates beautiful task cards with priority colors and metadata
```

#### **3. Page Functions**
```python
def dashboard_page():
    """Main dashboard with metrics and charts"""

def kanban_board_page():
    """Interactive Kanban board"""

def integrations_page():
    """Integration management"""

def add_task_page():
    """Task creation form"""

def analytics_page():
    """Analytics and reporting"""
```

### **4. Custom CSS Styling**
```python
st.markdown("""
<style>
    .task-card {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
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

## 🔧 Troubleshooting

### **Common Issues**

#### **1. "Cannot connect to API" Error**
```bash
# Solution: Start the FastAPI backend first
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m src.app
```

#### **2. "Module not found" Error**
```bash
# Solution: Install missing dependencies
python3 -m pip install --user streamlit plotly pandas requests
```

#### **3. "Port already in use" Error**
```bash
# Solution: Kill existing processes
lsof -ti:8501 | xargs kill -9  # Kill Streamlit
lsof -ti:8000 | xargs kill -9  # Kill FastAPI
```

#### **4. Streamlit not found in PATH**
```bash
# Solution: Use python module instead
python3 -m streamlit run streamlit_app.py
# Instead of: streamlit run streamlit_app.py
```

### **5. Empty Dashboard**
- **Cause**: FastAPI backend not running
- **Solution**: Start backend with `python3 -m src.app`
- **Check**: Visit http://localhost:8000/healthz

---

## 📱 Using the Streamlit App

### **Navigation**
1. **Sidebar Menu**: Use the dropdown to navigate between pages
2. **API Status**: Green ✅ means backend is connected
3. **Real-time Updates**: Data refreshes automatically

### **Workflow**
1. **Start with Dashboard**: Get overview of all projects
2. **Use Kanban Board**: Manage day-to-day tasks
3. **Add New Tasks**: Use the form to create work items
4. **Check Analytics**: Monitor team performance
5. **Review Integrations**: Track project progress

### **Tips**
- Keep both FastAPI backend and Streamlit running
- Use the move buttons to update task status
- Filter Kanban board by sprint for focused view
- Check dashboard for high-priority items
- Use analytics to track team velocity

---

## 🚀 Quick Commands

```bash
# Start everything (2 terminals needed)
Terminal 1: cd "/Users/jeffjackson/Desktop/Project for workflow api" && python3 -m src.app
Terminal 2: cd "/Users/jeffjackson/Desktop/Project for workflow api" && python3 -m streamlit run streamlit_app.py

# Or use Makefile
Terminal 1: make dev
Terminal 2: make streamlit

# Access URLs
# Streamlit: http://localhost:8501
# FastAPI: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

Your Streamlit app is now ready to manage your workflow integrations! 🎉
