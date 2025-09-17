# 📱 Streamlit App - Practical Usage Guide

## 🚀 Quick Start Commands

### **Step 1: Start FastAPI Backend**
```bash
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m src.app
```
**✅ Success indicators:**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### **Step 2: Start Streamlit App** (New Terminal)
```bash
cd "/Users/jeffjackson/Desktop/Project for workflow api"
python3 -m streamlit run streamlit_app.py
```
**✅ Success indicators:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### **Step 3: Open Your Browser**
Navigate to: **http://localhost:8501**

---

## 📊 What You'll See - Page by Page

### **1. Dashboard (Landing Page)**

**🔝 Header:**
```
📊 Workflow Dashboard
```

**📈 Key Metrics (4 boxes across top):**
```
Total Integrations    Active Tasks    High Priority Tasks    Story Points Remaining
        4                 5                   5                      29
```

**📊 Charts Section:**
- **Left Chart**: "Integrations by Stage" (Pie Chart)
  - Build: 2 integrations (50%)
  - Testing: 2 integrations (50%)
  
- **Right Chart**: "Tasks by Kanban Column" (Bar Chart)
  - Backlog: 1 task
  - To Do: 2 tasks
  - In Progress: 3 tasks
  - In Review: 1 task
  - Testing: 1 task
  - Done: 2 tasks
  - Blocked: 0 tasks

**📋 Recent Updates:**
```
F&I Express / Cox Automotive    Stage: Testing    Active: 1 tasks    09/17 14:07
Provider Exchange Network      Stage: Testing    Active: 2 tasks    09/17 14:07
MenuMetric Integration         Stage: Build      Active: 0 tasks    09/17 14:07
Vision Dealer API Integration  Stage: Build      Active: 2 tasks    09/17 14:07
```

### **2. Kanban Board**

**🎯 Header:**
```
📋 Kanban Board
```

**🔧 Controls:**
```
Select Integration: [Vision Dealer API Integration (Vision Dealer Solutions) ▼]
Filter by Sprint:   [All Sprints ▼]
```

**📊 Summary:**
```
Total Tasks: 3    Total Story Points: 8    Showing: All Tasks
```

**📋 Kanban Columns (7 columns across):**

**📝 Backlog (0 tasks)**
```
📝 Backlog
0 tasks
(empty column)
```

**📋 To Do (1 task)**
```
📋 To Do  
1 tasks

┌─────────────────────────────────────┐
│ 🤝 Schedule follow-up meeting with Brandon │
│ Medium Priority (yellow border)            │
│ Set up regular check-ins to track progress │
│ 👤 Ramisa              📊 1 pts           │
│ #meeting #follow-up                        │
│ [⬅️ Move] [ℹ️ Details] [➡️ Move]          │
└─────────────────────────────────────┘
```

**⚡ In Progress (2 tasks)**
```
⚡ In Progress
2 tasks

┌─────────────────────────────────────┐
│ 🤝 Confirm latest communication status     │
│ High Priority (red border)                 │
│ Confirm status with Brandon...              │
│ 👤 Ramisa              📊 2 pts           │
│ #communication #status-check               │
│ [⬅️ Move] [ℹ️ Details] [➡️ Move]          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📖 Deliver API documentation              │
│ High Priority (red border)                │
│ Share API docs, test dealers, products    │
│ 👤 Sona Team           📊 5 pts          │
│ #documentation #delivery                  │
│ [⬅️ Move] [ℹ️ Details] [➡️ Move]         │
└─────────────────────────────────────┘
```

**👀 In Review (0 tasks)**
```
👀 In Review
0 tasks
(empty column)
```

**🧪 Testing (0 tasks)**
```
🧪 Testing
0 tasks
(empty column)
```

**✅ Done (0 tasks)**
```
✅ Done
0 tasks
(empty column)
```

**🚫 Blocked (0 tasks)**
```
🚫 Blocked
0 tasks
(empty column)
```

### **3. Integrations Page**

**🤝 Header:**
```
🤝 Integrations
```

**📋 Integration Cards (4 expandable sections):**

**🏢 Vision Dealer API Integration - Vision Dealer Solutions**
```
▼ (Click to expand)

Stage: Build
Description: API integration with Vision Dealer's new system, similar to PCMI specs

Contacts:
- Brandon Steup (brandon.steup@visiondealersolutions.com) - Business Analyst

Next Steps:
- Confirm current stage (Research → Build → Testing → Launch)
- Deliver API documentation and test data by end of week
- Schedule follow-up meeting with Brandon

                                    Total Tasks: 3
                                    Completed: 0
                                    In Progress: 2
                                    ████████░░ 0.0% Complete
```

**🏢 MenuMetric Integration - MenuMetric**
```
▼ (Click to expand)

Stage: Build
Description: Menu integration requiring eligibility guidelines and API documentation

Contacts:
- Hannah Honeybrook (hannah@menumetric.com) - Integration Lead

Next Steps:
- Complete delivery of remaining items to Hannah
- Begin direct coordination once API docs delivered
- Follow up on testing progress

                                    Total Tasks: 3
                                    Completed: 1
                                    In Progress: 0
                                    ███░░░░░░░ 33.3% Complete
```

### **4. Add Task Page**

**➕ Header:**
```
➕ Add New Task
```

**📝 Task Details Form:**
```
Integration *: [Vision Dealer API Integration (Vision Dealer Solutions) ▼]

┌─── Left Column ───┐  ┌─── Right Column ───┐
│ Task Title *       │  │ Story Points        │
│ [____________]     │  │ [1        ] 0-20    │
│                    │  │                     │
│ Task Type          │  │ Sprint              │
│ [feature ▼]        │  │ [____________]      │
│                    │  │                     │
│ Priority           │  │ Reporter            │
│ [medium ▼]         │  │ [____________]      │
│                    │  │                     │
│ Assigned To        │  │ Due Date            │
│ [____________]     │  │ [📅 Select date]   │
└────────────────────┘  └─────────────────────┘

Description *
┌─────────────────────────────────────────────┐
│                                             │
│                                             │
│                                             │
└─────────────────────────────────────────────┘

Tags (comma-separated)
[____________]

                [Create Task]
```

**After successful creation:**
```
✅ Task 'Your Task Name' created successfully!

{
  "id": "vision-dealer-002",
  "title": "Your Task Name",
  "description": "Your description",
  "status": "pending",
  "kanban_status": "backlog",
  "priority": "medium",
  "task_type": "feature",
  "assigned_to": "Team Member",
  "story_points": 3,
  "sprint": "Sprint 2",
  "tags": ["api", "integration"]
}
```

### **5. Analytics Page**

**📈 Header:**
```
📈 Analytics
```

**🏃‍♂️ Sprint Analytics:**
```
Sprint Analytics

┌─── Tasks by Sprint (Bar Chart) ───┐  ┌─── Story Points by Sprint ───┐
│                                    │  │                               │
│    Sprint 1  █████████ 9 Total    │  │    Sprint 1  █████████ 31 Total│
│              ███ 2 Completed      │  │              ██ 4 Completed   │
│                                    │  │                               │
│    Sprint 2  ██ 2 Total           │  │    Sprint 2  ██ 5 Total       │
│              ░ 0 Completed        │  │              ░ 0 Completed    │
└────────────────────────────────────┘  └───────────────────────────────┘

Sprint Completion Rate (Line Chart)
┌─────────────────────────────────────────────────────────────┐
│ 25% ●                                                       │
│     │\                                                      │
│     │ \                                                     │
│  0% │  ●─────────────────────────────────────────────────  │
│     Sprint 1                                    Sprint 2    │
└─────────────────────────────────────────────────────────────┘
```

**⚡ Priority Distribution:**
```
Tasks by Priority (Pie Chart)
┌─────────────────────────────────────┐
│        High (70%)                   │
│    ████████████████████             │
│                                     │
│    Medium (30%)                     │
│    ████████                         │
│                                     │
│    Low (0%)  Critical (0%)          │
└─────────────────────────────────────┘
```

**📊 Story Points Progress:**
```
Total Story Points: 33    Completed: 4    Remaining: 29

Overall Progress: 12.1%
████████████████████████████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░
```

---

## 🎮 Interactive Features

### **Moving Tasks**
1. **Click ⬅️ Move**: Moves task to previous column
2. **Click ➡️ Move**: Moves task to next column
3. **Success message**: "Task moved to In Progress"
4. **Page refreshes**: Shows updated position

### **Viewing Task Details**
1. **Click ℹ️ Details**: Expands task information
2. **Shows**: ID, Type, Priority, Status, Assignee, Reporter, Story Points, Sprint
3. **Displays**: Full description, tags, comments (if any)

### **Creating New Tasks**
1. **Fill required fields**: Title and Description
2. **Select options**: Integration, Priority, Task Type
3. **Add details**: Story points, sprint, assignee
4. **Click Create Task**: Shows success message and JSON response
5. **Task appears**: In Backlog column of Kanban board

### **Filtering and Navigation**
1. **Integration Selector**: Switch between projects on Kanban board
2. **Sprint Filter**: Show only tasks from specific sprint
3. **Sidebar Navigation**: Switch between pages
4. **API Status**: Green checkmark when backend connected

---

## 🔧 Troubleshooting Visual Cues

### **✅ Everything Working:**
- Sidebar shows: "✅ API Connected"
- Dashboard loads with 4 metrics
- Charts display data
- Kanban board shows tasks in columns

### **❌ API Not Connected:**
- Sidebar shows: "❌ API Disconnected"
- Error message: "🔌 Cannot connect to API"
- Info message: "Run: `make dev` or `python3 -m src.app`"
- Pages show empty or error states

### **🔄 Loading States:**
- Streamlit shows spinning wheel during API calls
- Charts may show "Loading..." temporarily
- Task movements show brief loading state

---

## 📱 Mobile/Responsive Behavior

The app automatically adapts to different screen sizes:
- **Desktop**: Full 7-column Kanban layout
- **Tablet**: Columns stack in smaller groups
- **Mobile**: Single column view with horizontal scrolling

---

## 🎯 Daily Usage Patterns

### **Morning Standup:**
1. Start with **Dashboard** - check high priority tasks
2. Review **Kanban Board** - see what's in progress
3. Check **Analytics** - review yesterday's progress

### **Task Management:**
1. Use **Add Task** - create new work items
2. Move tasks on **Kanban Board** - update status
3. Check **Integrations** - review project progress

### **Weekly Review:**
1. **Analytics** page - check sprint velocity
2. **Dashboard** - overall project health
3. **Integrations** - contact stakeholders as needed

Your Streamlit app provides a complete, intuitive interface for managing all your workflow integration projects! 🚀
