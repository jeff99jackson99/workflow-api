"""
Workflow API - Main FastAPI application for managing developer and vendor integrations.
Enhanced with Kanban-style task management.
"""
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import uvicorn

# Workflow Stage Definitions
class WorkflowStage(str, Enum):
    RESEARCH = "research"
    BUILD = "build" 
    TESTING = "testing"
    LAUNCH = "launch"
    MAINTENANCE = "maintenance"

# Kanban Column Status (more detailed than basic task status)
class KanbanStatus(str, Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    TESTING = "testing"
    DONE = "done"
    BLOCKED = "blocked"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskType(str, Enum):
    FEATURE = "feature"
    BUG = "bug"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    MEETING = "meeting"
    REVIEW = "review"
    DEPLOYMENT = "deployment"

# Pydantic Models
class Contact(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    role: Optional[str] = None
    company: str

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    kanban_status: KanbanStatus = KanbanStatus.BACKLOG
    priority: Priority = Priority.MEDIUM
    task_type: TaskType = TaskType.FEATURE
    assigned_to: Optional[str] = None
    reporter: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    story_points: Optional[int] = None
    sprint: Optional[str] = None
    comments: List[Dict[str, Any]] = Field(default_factory=list)
    attachments: List[str] = Field(default_factory=list)

class Integration(BaseModel):
    id: str
    name: str
    company: str
    stage: WorkflowStage = WorkflowStage.RESEARCH
    description: str
    contacts: List[Contact] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
    next_steps: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    current_sprint: Optional[str] = None

class CreateIntegrationRequest(BaseModel):
    name: str
    company: str
    description: str
    stage: WorkflowStage = WorkflowStage.RESEARCH
    contacts: List[Contact] = Field(default_factory=list)

class CreateTaskRequest(BaseModel):
    title: str
    description: str
    priority: Priority = Priority.MEDIUM
    task_type: TaskType = TaskType.FEATURE
    assigned_to: Optional[str] = None
    reporter: Optional[str] = None
    due_date: Optional[datetime] = None
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    story_points: Optional[int] = None
    sprint: Optional[str] = None

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    kanban_status: Optional[KanbanStatus] = None
    priority: Optional[Priority] = None
    task_type: Optional[TaskType] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    story_points: Optional[int] = None
    sprint: Optional[str] = None

class KanbanBoard(BaseModel):
    integration_id: str
    integration_name: str
    columns: Dict[str, List[Task]] = Field(default_factory=dict)
    total_tasks: int = 0
    total_story_points: int = 0

class Comment(BaseModel):
    id: str
    task_id: str
    author: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Initialize FastAPI app
app = FastAPI(
    title="Workflow API",
    description="Workflow management system for developer and vendor integrations with Kanban board",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
integrations_db: Dict[str, Integration] = {}
task_counter = 0
comment_counter = 0

# Initialize with your current integration data
def initialize_data():
    """Initialize with current integration tracks"""
    global integrations_db
    
    # Vision Dealer Integration
    vision_dealer = Integration(
        id="vision-dealer",
        name="Vision Dealer API Integration",
        company="Vision Dealer Solutions",
        stage=WorkflowStage.BUILD,
        description="API integration with Vision Dealer's new system, similar to PCMI specs",
        contacts=[
            Contact(
                name="Brandon Steup",
                email="brandon.steup@visiondealersolutions.com",
                role="Business Analyst",
                company="Vision Dealer Solutions"
            )
        ],
        tasks=[
            Task(
                id="vd-001",
                title="Confirm latest communication status",
                description="Confirm the status of the latest communication with Brandon and identify current stage",
                status=TaskStatus.IN_PROGRESS,
                kanban_status=KanbanStatus.IN_PROGRESS,
                priority=Priority.HIGH,
                task_type=TaskType.MEETING,
                assigned_to="Ramisa",
                reporter="Jeff Jackson",
                tags=["communication", "status-check"],
                story_points=2,
                sprint="Sprint 1"
            ),
            Task(
                id="vd-002", 
                title="Deliver API documentation",
                description="Share API docs, test dealers, and products with Vision Dealer",
                status=TaskStatus.IN_PROGRESS,
                kanban_status=KanbanStatus.IN_PROGRESS,
                priority=Priority.HIGH,
                task_type=TaskType.DOCUMENTATION,
                assigned_to="Sona Team",
                reporter="Jeff Jackson",
                tags=["documentation", "delivery"],
                story_points=5,
                sprint="Sprint 1"
            ),
            Task(
                id="vd-003",
                title="Schedule follow-up meeting with Brandon",
                description="Set up regular check-ins to track progress",
                status=TaskStatus.PENDING,
                kanban_status=KanbanStatus.TODO,
                priority=Priority.MEDIUM,
                task_type=TaskType.MEETING,
                assigned_to="Ramisa",
                tags=["meeting", "follow-up"],
                story_points=1,
                sprint="Sprint 1"
            )
        ],
        next_steps=[
            "Confirm current stage (Research → Build → Testing → Launch)",
            "Deliver API documentation and test data by end of week",
            "Schedule follow-up meeting with Brandon"
        ],
        metadata={
            "api_specs": "New API from new system, similar (not identical) to PCMI",
            "implementation": "New auth credentials + endpoints, some mapping required",
            "documentation_status": "Exists, shared with PEN & F&I Express"
        },
        current_sprint="Sprint 1"
    )
    
    # MenuMetric Integration  
    menumetric = Integration(
        id="menumetric",
        name="MenuMetric Integration",
        company="MenuMetric",
        stage=WorkflowStage.BUILD,
        description="Menu integration requiring eligibility guidelines and API documentation",
        contacts=[
            Contact(
                name="Hannah Honeybrook",
                email="hannah@menumetric.com", 
                role="Integration Lead",
                company="MenuMetric"
            )
        ],
        tasks=[
            Task(
                id="mm-001",
                title="Provide Eligibility Guidelines",
                description="Deliver eligibility guidelines to Hannah's team",
                status=TaskStatus.PENDING,
                kanban_status=KanbanStatus.TODO,
                priority=Priority.HIGH,
                task_type=TaskType.DOCUMENTATION,
                assigned_to="Sona Team",
                reporter="Jeff Jackson",
                tags=["guidelines", "delivery"],
                story_points=3,
                sprint="Sprint 1"
            ),
            Task(
                id="mm-002",
                title="Provide Testing Dealer ID",
                description="Testing Dealer ID with ALL products enrolled",
                status=TaskStatus.COMPLETED,
                kanban_status=KanbanStatus.DONE,
                priority=Priority.HIGH,
                task_type=TaskType.FEATURE,
                assigned_to="Sona Team",
                reporter="Jeff Jackson",
                tags=["testing", "dealer-setup"],
                story_points=2,
                sprint="Sprint 1"
            ),
            Task(
                id="mm-003",
                title="List of industries with products",
                description="Provide list of industries with associated products",
                status=TaskStatus.PENDING,
                kanban_status=KanbanStatus.BACKLOG,
                priority=Priority.MEDIUM,
                task_type=TaskType.DOCUMENTATION,
                assigned_to="Sona Team",
                tags=["documentation", "products"],
                story_points=2,
                sprint="Sprint 2"
            )
        ],
        next_steps=[
            "Complete delivery of remaining items to Hannah",
            "Begin direct coordination once API docs delivered",
            "Follow up on testing progress"
        ],
        current_sprint="Sprint 1"
    )
    
    # PEN Integration
    pen = Integration(
        id="pen",
        name="Provider Exchange Network (PEN)",
        company="Provider Exchange Network", 
        stage=WorkflowStage.TESTING,
        description="Ongoing nullable fields support and API updates",
        contacts=[
            Contact(
                name="Jason Malak",
                email="jmalak@providerexchangenetwork.com",
                phone="313-749-0469",
                role="Integration Manager",
                company="Provider Exchange Network"
            ),
            Contact(
                name="Carl Ciaramitaro", 
                email="cciaramitaro@providerexchangenetwork.com",
                phone="313-749-0943",
                company="Provider Exchange Network"
            )
        ],
        tasks=[
            Task(
                id="pen-001",
                title="Validate BETA changes",
                description="Confirm BETA behavior for nullable/optional fields",
                status=TaskStatus.IN_PROGRESS,
                kanban_status=KanbanStatus.TESTING,
                priority=Priority.HIGH,
                task_type=TaskType.FEATURE,
                assigned_to="PEN Team",
                reporter="Shivani",
                tags=["testing", "validation", "beta"],
                story_points=5,
                sprint="Sprint 1"
            ),
            Task(
                id="pen-002",
                title="CreateContract nullable support",
                description="Complete CreateContract nullable support implementation",
                status=TaskStatus.IN_PROGRESS,
                kanban_status=KanbanStatus.IN_PROGRESS,
                priority=Priority.HIGH,
                task_type=TaskType.FEATURE,
                assigned_to="Sona Team",
                reporter="Shivani",
                tags=["development", "nullable-fields"],
                story_points=8,
                sprint="Sprint 1"
            )
        ],
        next_steps=[
            "Track delivery of latest API documentation",
            "Validate CreateContract once deployed",
            "Confirm all nullable field behavior"
        ],
        metadata={
            "beta_status": "GetEligibleCoverages updated and deployed",
            "in_progress": "CreateContract nullable support",
            "completed": "Optional fields logic fixed"
        },
        current_sprint="Sprint 1"
    )
    
    # F&I Express Integration
    fi_express = Integration(
        id="fi-express",
        name="F&I Express / Cox Automotive",
        company="Cox Automotive",
        stage=WorkflowStage.TESTING,
        description="Integration with Cox Automotive team, addressing environment and token setup",
        contacts=[
            Contact(
                name="Katie Rupp",
                email="Kathrine.Rupp@coxautoinc.com",
                role="Technical Customer Care Analyst I – API",
                company="Cox Automotive"
            ),
            Contact(
                name="Stephany Spiker",
                email="Stephany.Spiker@coxautoinc.com",
                company="Cox Automotive"
            ),
            Contact(
                name="Kerri Massura",
                email="Kerri.massura@coxautoinc.com", 
                company="Cox Automotive"
            )
        ],
        tasks=[
            Task(
                id="fi-001",
                title="Confirm environment/token setup",
                description="Clarify if one token used for both NonProd and Prod environments",
                status=TaskStatus.IN_PROGRESS,
                kanban_status=KanbanStatus.IN_REVIEW,
                priority=Priority.MEDIUM,
                task_type=TaskType.RESEARCH,
                assigned_to="Katie Rupp",
                reporter="Shivani",
                tags=["environment", "authentication"],
                story_points=3,
                sprint="Sprint 1"
            ),
            Task(
                id="fi-002",
                title="Resolve website maintenance issues",
                description="Ensure BETA environment is accessible after maintenance",
                status=TaskStatus.COMPLETED,
                kanban_status=KanbanStatus.DONE,
                priority=Priority.HIGH,
                task_type=TaskType.BUG,
                assigned_to="Sona Team",
                reporter="Katie Rupp",
                tags=["maintenance", "environment"],
                story_points=2,
                sprint="Sprint 1"
            )
        ],
        next_steps=[
            "Confirm token setup requirements",
            "Provide availability timeline post-maintenance",
            "Send revised Coverage Surcharges documentation"
        ],
        metadata={
            "dev_cycle": "2-week sprints",
            "integration_timeline": "6-8 weeks for new API integrations",
            "recent_updates": "dealerRemit and dealerSoftPack properties added"
        },
        current_sprint="Sprint 1"
    )
    
    integrations_db.update({
        "vision-dealer": vision_dealer,
        "menumetric": menumetric, 
        "pen": pen,
        "fi-express": fi_express
    })

# Health check endpoint
@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

# Integration endpoints
@app.get("/integrations", response_model=List[Integration])
async def get_integrations(
    stage: Optional[WorkflowStage] = Query(None, description="Filter by workflow stage"),
    company: Optional[str] = Query(None, description="Filter by company name")
):
    """Get all integrations with optional filtering"""
    integrations = list(integrations_db.values())
    
    if stage:
        integrations = [i for i in integrations if i.stage == stage]
    if company:
        integrations = [i for i in integrations if company.lower() in i.company.lower()]
    
    return integrations

@app.get("/integrations/{integration_id}", response_model=Integration)
async def get_integration(integration_id: str):
    """Get specific integration by ID"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integrations_db[integration_id]

@app.post("/integrations", response_model=Integration)
async def create_integration(request: CreateIntegrationRequest):
    """Create new integration"""
    integration_id = request.name.lower().replace(" ", "-")
    
    if integration_id in integrations_db:
        raise HTTPException(status_code=400, detail="Integration already exists")
    
    integration = Integration(
        id=integration_id,
        name=request.name,
        company=request.company,
        description=request.description,
        stage=request.stage,
        contacts=request.contacts
    )
    
    integrations_db[integration_id] = integration
    return integration

@app.put("/integrations/{integration_id}/stage")
async def update_integration_stage(integration_id: str, stage: WorkflowStage):
    """Update integration workflow stage"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integrations_db[integration_id].stage = stage
    integrations_db[integration_id].updated_at = datetime.now(timezone.utc)
    return integrations_db[integration_id]

# Kanban Board endpoints
@app.get("/integrations/{integration_id}/kanban", response_model=KanbanBoard)
async def get_kanban_board(integration_id: str, sprint: Optional[str] = Query(None)):
    """Get Kanban board for integration"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integration = integrations_db[integration_id]
    tasks = integration.tasks
    
    # Filter by sprint if specified
    if sprint:
        tasks = [t for t in tasks if t.sprint == sprint]
    
    # Organize tasks by Kanban status
    columns = {
        KanbanStatus.BACKLOG: [],
        KanbanStatus.TODO: [],
        KanbanStatus.IN_PROGRESS: [],
        KanbanStatus.IN_REVIEW: [],
        KanbanStatus.TESTING: [],
        KanbanStatus.DONE: [],
        KanbanStatus.BLOCKED: []
    }
    
    total_story_points = 0
    for task in tasks:
        columns[task.kanban_status].append(task)
        if task.story_points:
            total_story_points += task.story_points
    
    return KanbanBoard(
        integration_id=integration_id,
        integration_name=integration.name,
        columns=columns,
        total_tasks=len(tasks),
        total_story_points=total_story_points
    )

@app.put("/integrations/{integration_id}/tasks/{task_id}/move")
async def move_task_kanban(integration_id: str, task_id: str, new_status: KanbanStatus):
    """Move task to different Kanban column"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integration = integrations_db[integration_id]
    task = next((t for t in integration.tasks if t.id == task_id), None)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update Kanban status and corresponding task status
    task.kanban_status = new_status
    task.updated_at = datetime.now(timezone.utc)
    
    # Update task status based on Kanban status
    status_mapping = {
        KanbanStatus.BACKLOG: TaskStatus.PENDING,
        KanbanStatus.TODO: TaskStatus.PENDING,
        KanbanStatus.IN_PROGRESS: TaskStatus.IN_PROGRESS,
        KanbanStatus.IN_REVIEW: TaskStatus.IN_PROGRESS,
        KanbanStatus.TESTING: TaskStatus.IN_PROGRESS,
        KanbanStatus.DONE: TaskStatus.COMPLETED,
        KanbanStatus.BLOCKED: TaskStatus.BLOCKED
    }
    task.status = status_mapping[new_status]
    
    integration.updated_at = datetime.now(timezone.utc)
    
    return task

# Task endpoints
@app.post("/integrations/{integration_id}/tasks", response_model=Task)
async def create_task(integration_id: str, request: CreateTaskRequest):
    """Create new task for integration"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    global task_counter
    task_counter += 1
    task_id = f"{integration_id}-{task_counter:03d}"
    
    task = Task(
        id=task_id,
        title=request.title,
        description=request.description,
        priority=request.priority,
        task_type=request.task_type,
        assigned_to=request.assigned_to,
        reporter=request.reporter,
        due_date=request.due_date,
        dependencies=request.dependencies,
        tags=request.tags,
        story_points=request.story_points,
        sprint=request.sprint
    )
    
    integrations_db[integration_id].tasks.append(task)
    integrations_db[integration_id].updated_at = datetime.now(timezone.utc)
    
    return task

@app.put("/integrations/{integration_id}/tasks/{task_id}")
async def update_task(integration_id: str, task_id: str, request: UpdateTaskRequest):
    """Update existing task"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integration = integrations_db[integration_id]
    task = next((t for t in integration.tasks if t.id == task_id), None)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task fields
    if request.title is not None:
        task.title = request.title
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status
    if request.kanban_status is not None:
        task.kanban_status = request.kanban_status
    if request.priority is not None:
        task.priority = request.priority
    if request.task_type is not None:
        task.task_type = request.task_type
    if request.assigned_to is not None:
        task.assigned_to = request.assigned_to
    if request.due_date is not None:
        task.due_date = request.due_date
    if request.story_points is not None:
        task.story_points = request.story_points
    if request.sprint is not None:
        task.sprint = request.sprint
    
    task.updated_at = datetime.now(timezone.utc)
    integration.updated_at = datetime.now(timezone.utc)
    
    return task

@app.delete("/integrations/{integration_id}/tasks/{task_id}")
async def delete_task(integration_id: str, task_id: str):
    """Delete a task"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integration = integrations_db[integration_id]
    task_index = next((i for i, t in enumerate(integration.tasks) if t.id == task_id), None)
    
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted_task = integration.tasks.pop(task_index)
    integration.updated_at = datetime.now(timezone.utc)
    
    return {"message": f"Task {task_id} deleted successfully", "deleted_task": deleted_task}

# Comment endpoints
@app.post("/integrations/{integration_id}/tasks/{task_id}/comments")
async def add_comment(integration_id: str, task_id: str, content: str, author: str):
    """Add comment to task"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integration = integrations_db[integration_id]
    task = next((t for t in integration.tasks if t.id == task_id), None)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    global comment_counter
    comment_counter += 1
    comment_id = f"comment-{comment_counter:03d}"
    
    comment = {
        "id": comment_id,
        "author": author,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    task.comments.append(comment)
    task.updated_at = datetime.now(timezone.utc)
    integration.updated_at = datetime.now(timezone.utc)
    
    return comment

@app.get("/integrations/{integration_id}/next-steps")
async def get_next_steps(integration_id: str):
    """Get AI-generated next steps for integration"""
    if integration_id not in integrations_db:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    integration = integrations_db[integration_id]
    
    # Generate next steps based on current stage and tasks
    next_steps = []
    pending_tasks = [t for t in integration.tasks if t.status == TaskStatus.PENDING]
    blocked_tasks = [t for t in integration.tasks if t.status == TaskStatus.BLOCKED]
    in_progress_tasks = [t for t in integration.tasks if t.status == TaskStatus.IN_PROGRESS]
    
    if blocked_tasks:
        next_steps.append(f"🚫 Resolve {len(blocked_tasks)} blocked task(s)")
        for task in blocked_tasks[:3]:  # Show first 3 blocked tasks
            next_steps.append(f"   - {task.title}")
    
    if in_progress_tasks:
        high_priority_in_progress = [t for t in in_progress_tasks if t.priority == Priority.HIGH]
        if high_priority_in_progress:
            next_steps.append(f"🔥 Focus on {len(high_priority_in_progress)} high-priority task(s) in progress")
    
    if pending_tasks:
        high_priority = [t for t in pending_tasks if t.priority == Priority.HIGH]
        if high_priority:
            next_steps.append(f"⭐ Start {len(high_priority)} high-priority pending task(s)")
    
    # Stage-specific recommendations
    if integration.stage == WorkflowStage.RESEARCH:
        next_steps.extend([
            "📋 Gather technical requirements",
            "🤝 Schedule kickoff meeting with stakeholders",
            "🎯 Define success criteria and timeline"
        ])
    elif integration.stage == WorkflowStage.BUILD:
        next_steps.extend([
            "📖 Finalize API documentation",
            "🛠️ Set up development environment",
            "⚡ Begin implementation of core features"
        ])
    elif integration.stage == WorkflowStage.TESTING:
        next_steps.extend([
            "🧪 Execute test scenarios",
            "✅ Validate API responses",
            "🤝 Coordinate with external team for testing"
        ])
    elif integration.stage == WorkflowStage.LAUNCH:
        next_steps.extend([
            "🚀 Prepare production deployment",
            "📅 Schedule go-live date",
            "📊 Set up monitoring and alerts"
        ])
    
    return {
        "integration_id": integration_id,
        "current_stage": integration.stage,
        "next_steps": next_steps,
        "generated_at": datetime.now(timezone.utc)
    }

@app.get("/dashboard")
async def get_dashboard():
    """Get dashboard overview of all integrations"""
    integrations = list(integrations_db.values())
    
    # Calculate statistics
    total_integrations = len(integrations)
    stage_counts = {}
    for stage in WorkflowStage:
        stage_counts[stage.value] = len([i for i in integrations if i.stage == stage])
    
    # Task statistics
    all_tasks = [task for integration in integrations for task in integration.tasks]
    task_stats = {}
    for status in TaskStatus:
        task_stats[status.value] = len([t for t in all_tasks if t.status == status])
    
    # Kanban statistics
    kanban_stats = {}
    for status in KanbanStatus:
        kanban_stats[status.value] = len([t for t in all_tasks if t.kanban_status == status])
    
    # Priority statistics
    priority_stats = {}
    for priority in Priority:
        priority_stats[priority.value] = len([t for t in all_tasks if t.priority == priority])
    
    # High priority tasks
    high_priority_tasks = [t for t in all_tasks if t.priority == Priority.HIGH and t.status != TaskStatus.COMPLETED]
    
    # Overdue tasks
    now = datetime.now(timezone.utc)
    overdue_tasks = [t for t in all_tasks if t.due_date and t.due_date < now and t.status != TaskStatus.COMPLETED]
    
    # Story points summary
    total_story_points = sum(t.story_points or 0 for t in all_tasks)
    completed_story_points = sum(t.story_points or 0 for t in all_tasks if t.status == TaskStatus.COMPLETED)
    
    return {
        "total_integrations": total_integrations,
        "stage_distribution": stage_counts,
        "task_statistics": task_stats,
        "kanban_statistics": kanban_stats,
        "priority_statistics": priority_stats,
        "high_priority_tasks": len(high_priority_tasks),
        "overdue_tasks": len(overdue_tasks),
        "story_points": {
            "total": total_story_points,
            "completed": completed_story_points,
            "remaining": total_story_points - completed_story_points
        },
        "recent_updates": [
            {
                "integration": i.name,
                "updated_at": i.updated_at,
                "stage": i.stage,
                "active_tasks": len([t for t in i.tasks if t.status == TaskStatus.IN_PROGRESS])
            }
            for i in sorted(integrations, key=lambda x: x.updated_at, reverse=True)[:5]
        ]
    }

# Sprint management endpoints
@app.get("/sprints")
async def get_sprints():
    """Get all sprints across integrations"""
    all_tasks = [task for integration in integrations_db.values() for task in integration.tasks]
    sprints = list(set(task.sprint for task in all_tasks if task.sprint))
    
    sprint_data = {}
    for sprint in sprints:
        sprint_tasks = [t for t in all_tasks if t.sprint == sprint]
        sprint_data[sprint] = {
            "total_tasks": len(sprint_tasks),
            "completed_tasks": len([t for t in sprint_tasks if t.status == TaskStatus.COMPLETED]),
            "total_story_points": sum(t.story_points or 0 for t in sprint_tasks),
            "completed_story_points": sum(t.story_points or 0 for t in sprint_tasks if t.status == TaskStatus.COMPLETED)
        }
    
    return sprint_data

# Initialize data on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application data"""
    initialize_data()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
