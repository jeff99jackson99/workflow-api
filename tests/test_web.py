"""
Tests for the workflow API web application with Kanban functionality.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from src.app.web import app, WorkflowStage, TaskStatus, Priority, KanbanStatus, TaskType

# Initialize the test client and trigger startup events
client = TestClient(app)

# Ensure data is initialized for tests
def setup_module():
    """Setup test data"""
    from src.app.web import initialize_data
    initialize_data()

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_integrations():
    """Test getting all integrations"""
    response = client.get("/integrations")
    assert response.status_code == 200
    integrations = response.json()
    assert len(integrations) == 4  # Vision Dealer, MenuMetric, PEN, F&I Express
    
    # Check that Vision Dealer integration exists
    vision_dealer = next((i for i in integrations if i["id"] == "vision-dealer"), None)
    assert vision_dealer is not None
    assert vision_dealer["name"] == "Vision Dealer API Integration"
    assert vision_dealer["stage"] == WorkflowStage.BUILD

def test_get_integration_by_id():
    """Test getting specific integration"""
    response = client.get("/integrations/vision-dealer")
    assert response.status_code == 200
    integration = response.json()
    assert integration["id"] == "vision-dealer"
    assert integration["company"] == "Vision Dealer Solutions"
    assert len(integration["contacts"]) == 1
    assert integration["contacts"][0]["name"] == "Brandon Steup"

def test_get_kanban_board():
    """Test getting Kanban board for integration"""
    response = client.get("/integrations/vision-dealer/kanban")
    assert response.status_code == 200
    kanban = response.json()
    assert kanban["integration_id"] == "vision-dealer"
    assert "columns" in kanban
    assert "total_tasks" in kanban
    assert "total_story_points" in kanban
    
    # Check that columns exist
    assert KanbanStatus.BACKLOG in kanban["columns"]
    assert KanbanStatus.TODO in kanban["columns"]
    assert KanbanStatus.IN_PROGRESS in kanban["columns"]
    assert KanbanStatus.DONE in kanban["columns"]

def test_create_task_with_kanban():
    """Test creating new task with Kanban properties"""
    new_task = {
        "title": "Test Kanban Task",
        "description": "Test task with Kanban properties",
        "priority": Priority.HIGH,
        "task_type": TaskType.FEATURE,
        "assigned_to": "Test User",
        "reporter": "Test Reporter",
        "tags": ["test", "kanban"],
        "story_points": 5,
        "sprint": "Test Sprint"
    }
    
    response = client.post("/integrations/vision-dealer/tasks", json=new_task)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Kanban Task"
    assert task["priority"] == Priority.HIGH
    assert task["task_type"] == TaskType.FEATURE
    assert task["status"] == TaskStatus.PENDING
    assert task["kanban_status"] == KanbanStatus.BACKLOG
    assert task["story_points"] == 5
    assert task["sprint"] == "Test Sprint"

def test_move_task_kanban():
    """Test moving task between Kanban columns"""
    # First create a task
    new_task = {
        "title": "Task to Move",
        "description": "Task for testing Kanban movement",
        "priority": Priority.MEDIUM
    }
    
    create_response = client.post("/integrations/vision-dealer/tasks", json=new_task)
    task_id = create_response.json()["id"]
    
    # Move task to IN_PROGRESS
    response = client.put(f"/integrations/vision-dealer/tasks/{task_id}/move", 
                         params={"new_status": KanbanStatus.IN_PROGRESS})
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["kanban_status"] == KanbanStatus.IN_PROGRESS
    assert updated_task["status"] == TaskStatus.IN_PROGRESS

def test_update_task_with_kanban():
    """Test updating task with Kanban properties"""
    # First create a task
    new_task = {
        "title": "Task to Update",
        "description": "Original description",
        "priority": Priority.MEDIUM
    }
    
    create_response = client.post("/integrations/vision-dealer/tasks", json=new_task)
    task_id = create_response.json()["id"]
    
    # Update the task with Kanban properties
    update_data = {
        "kanban_status": KanbanStatus.IN_REVIEW,
        "story_points": 3,
        "sprint": "Sprint 2"
    }
    
    response = client.put(f"/integrations/vision-dealer/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["kanban_status"] == KanbanStatus.IN_REVIEW
    assert updated_task["story_points"] == 3
    assert updated_task["sprint"] == "Sprint 2"

def test_add_comment_to_task():
    """Test adding comment to task"""
    # Use existing task
    response = client.post("/integrations/vision-dealer/tasks/vd-001/comments",
                          params={"content": "Test comment", "author": "Test User"})
    assert response.status_code == 200
    comment = response.json()
    assert comment["content"] == "Test comment"
    assert comment["author"] == "Test User"
    assert "id" in comment

def test_delete_task():
    """Test deleting a task"""
    # First create a task
    new_task = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "priority": Priority.LOW
    }
    
    create_response = client.post("/integrations/vision-dealer/tasks", json=new_task)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/integrations/vision-dealer/tasks/{task_id}")
    assert response.status_code == 200
    assert "deleted_task" in response.json()

def test_get_dashboard_with_kanban():
    """Test dashboard with Kanban statistics"""
    response = client.get("/dashboard")
    assert response.status_code == 200
    dashboard = response.json()
    assert "total_integrations" in dashboard
    assert "kanban_statistics" in dashboard
    assert "priority_statistics" in dashboard
    assert "story_points" in dashboard
    assert dashboard["total_integrations"] >= 4

def test_get_sprints():
    """Test getting sprint information"""
    response = client.get("/sprints")
    assert response.status_code == 200
    sprints = response.json()
    assert isinstance(sprints, dict)
    # Should have at least Sprint 1 from our test data
    if "Sprint 1" in sprints:
        assert "total_tasks" in sprints["Sprint 1"]
        assert "completed_tasks" in sprints["Sprint 1"]
        assert "total_story_points" in sprints["Sprint 1"]

def test_get_next_steps_enhanced():
    """Test getting enhanced next steps with emojis"""
    response = client.get("/integrations/vision-dealer/next-steps")
    assert response.status_code == 200
    next_steps = response.json()
    assert "integration_id" in next_steps
    assert "current_stage" in next_steps
    assert "next_steps" in next_steps
    assert isinstance(next_steps["next_steps"], list)

def test_filter_kanban_by_sprint():
    """Test filtering Kanban board by sprint"""
    response = client.get("/integrations/vision-dealer/kanban", params={"sprint": "Sprint 1"})
    assert response.status_code == 200
    kanban = response.json()
    assert kanban["integration_id"] == "vision-dealer"
    
    # All tasks should be from Sprint 1 or None
    for column_tasks in kanban["columns"].values():
        for task in column_tasks:
            assert task["sprint"] in ["Sprint 1", None]
