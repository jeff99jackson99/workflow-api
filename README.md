# Workflow API - Enhanced Kanban System

A comprehensive workflow management system for tracking developer and vendor integrations through various stages of development, featuring a full Kanban board implementation.

## 🚀 Features

### **Enhanced Kanban Board**
- **7 Kanban Columns**: Backlog → To Do → In Progress → In Review → Testing → Done → Blocked
- **Drag & Drop Support**: Move tasks between columns via API
- **Sprint Management**: Filter tasks by sprint
- **Story Points**: Track effort estimation and velocity
- **Task Types**: Feature, Bug, Documentation, Research, Meeting, Review, Deployment

### **Advanced Task Management**
- **Rich Task Properties**: Priority, type, reporter, assignee, story points, sprint
- **Comments System**: Add comments and track discussions
- **Dependencies**: Link related tasks
- **Tags & Labels**: Organize and categorize tasks
- **Due Dates**: Track deadlines and overdue items

### **Workflow Stages**
- **Research** → **Build** → **Testing** → **Launch** → **Maintenance**
- Stage-specific recommendations and next steps
- Progress tracking across all integrations

### **Analytics & Reporting**
- **Dashboard**: Real-time statistics and KPIs
- **Sprint Analytics**: Story points completion, velocity tracking
- **Priority Distribution**: High/Medium/Low priority breakdown
- **Kanban Metrics**: Tasks per column, cycle time insights

## 🏃 Quick Start

### Setup & Run
```bash
# Install dependencies
make setup

# Start FastAPI backend server
make dev

# In a new terminal, start Streamlit web interface
make streamlit

# Run tests
make test
```

**Access Points:**
- **Streamlit Web UI**: `http://localhost:8501` (Main Interface)
- **FastAPI Backend**: `http://localhost:8000` 
- **API Documentation**: `http://localhost:8000/docs`

## 🖥️ Streamlit Web Interface

The Streamlit app provides a comprehensive web interface with:

### **📊 Dashboard**
- Real-time metrics and KPIs
- Stage and priority distribution charts
- Recent activity feed
- Story points progress tracking

### **📋 Kanban Board**
- Interactive Kanban board with all 7 columns
- Task cards with priority color coding
- Move tasks between columns with buttons
- Sprint filtering capabilities
- Task details and comments

### **🤝 Integrations**
- Overview of all integration projects
- Contact information and next steps
- Progress tracking and completion rates
- Expandable integration details

### **➕ Add Task**
- User-friendly form to create new tasks
- All task properties supported (priority, type, story points, etc.)
- Integration and sprint selection
- Tag and due date management

### **📈 Analytics**
- Sprint performance analytics
- Story points velocity tracking
- Priority distribution analysis
- Completion rate trends

## 📋 Kanban API Endpoints

### **Board Management**
- `GET /integrations/{id}/kanban` - Get Kanban board
- `GET /integrations/{id}/kanban?sprint=Sprint1` - Filter by sprint
- `PUT /integrations/{id}/tasks/{task_id}/move` - Move task between columns

### **Task Management**
- `POST /integrations/{id}/tasks` - Create new task
- `PUT /integrations/{id}/tasks/{task_id}` - Update task
- `DELETE /integrations/{id}/tasks/{task_id}` - Delete task
- `POST /integrations/{id}/tasks/{task_id}/comments` - Add comment

### **Sprint & Analytics**
- `GET /sprints` - Get all sprints with statistics
- `GET /dashboard` - Enhanced dashboard with Kanban metrics

## 🎯 Current Integrations (Pre-loaded)

### **1. Vision Dealer** (Build Stage)
- **Contact**: Brandon Steup
- **Tasks**: 3 tasks across different Kanban columns
- **Focus**: API integration and documentation delivery

### **2. MenuMetric** (Build Stage)
- **Contact**: Hannah Honeybrook
- **Tasks**: Eligibility guidelines and dealer setup
- **Status**: 1 completed, 2 pending

### **3. PEN - Provider Exchange Network** (Testing Stage)
- **Contacts**: Jason Malak, Carl Ciaramitaro
- **Tasks**: BETA validation and nullable field support
- **Story Points**: 13 points total

### **4. F&I Express / Cox Automotive** (Testing Stage)
- **Contacts**: Katie Rupp, Stephany Spiker, Kerri Massura
- **Tasks**: Environment setup and maintenance resolution

## 🔧 Kanban Workflow

### **Column Definitions**
1. **Backlog**: Ideas and future tasks
2. **To Do**: Ready to start
3. **In Progress**: Currently being worked on
4. **In Review**: Awaiting review/approval
5. **Testing**: Under testing/validation
6. **Done**: Completed tasks
7. **Blocked**: Tasks with impediments

### **Task Properties**
```json
{
  "id": "vd-001",
  "title": "Deliver API documentation",
  "description": "Share API docs, test dealers, and products",
  "status": "in_progress",
  "kanban_status": "in_progress",
  "priority": "high",
  "task_type": "documentation",
  "assigned_to": "Sona Team",
  "reporter": "Jeff Jackson",
  "story_points": 5,
  "sprint": "Sprint 1",
  "tags": ["documentation", "delivery"],
  "due_date": "2024-09-20T00:00:00Z"
}
```

## 📊 Enhanced Dashboard

The dashboard now includes:
- **Kanban Statistics**: Tasks per column
- **Priority Breakdown**: Critical/High/Medium/Low distribution
- **Story Points**: Total, completed, and remaining
- **Sprint Progress**: Velocity and completion rates
- **Overdue Tasks**: Automatic identification
- **Recent Activity**: Real-time updates

## 🔄 Adding New Tasks

### Via API:
```bash
curl -X POST "http://localhost:8000/integrations/vision-dealer/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Integration Task",
    "description": "Task description here",
    "priority": "high",
    "task_type": "feature",
    "assigned_to": "Team Member",
    "story_points": 3,
    "sprint": "Sprint 2",
    "tags": ["integration", "api"]
  }'
```

### Task Types Available:
- **feature**: New functionality
- **bug**: Bug fixes
- **documentation**: Documentation tasks
- **research**: Investigation and analysis
- **meeting**: Meetings and discussions
- **review**: Code/design reviews
- **deployment**: Deployment activities

## 🚀 Deployment

### Docker
```bash
make docker/build
make docker/run
```

### Production
The system includes GitHub Actions for CI/CD and automatic deployment to GitHub Container Registry.

## 🧪 Testing

Comprehensive test suite includes:
- Kanban board functionality
- Task CRUD operations
- Sprint management
- Comment system
- Dashboard analytics

```bash
make test
```

## 🎨 Customization

The system is designed to be easily extensible:
- Add new task types
- Create custom Kanban columns
- Integrate with external tools
- Add custom analytics

## 📈 Analytics Features

- **Velocity Tracking**: Story points per sprint
- **Cycle Time**: Time tasks spend in each column
- **Burndown Charts**: Progress visualization (via dashboard)
- **Team Performance**: Individual and team metrics

This enhanced Kanban system provides a complete project management solution for your integration workflows, with room to add unlimited tasks and comprehensive tracking capabilities.
