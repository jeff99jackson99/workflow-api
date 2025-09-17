"""
Entry point for running the workflow API application.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.web:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )
