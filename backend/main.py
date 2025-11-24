from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.user_routes import router as user_router
from backend.routes.subject_routes import router as subject_router
from backend.routes.ai_task_routes import router as ai_task
from backend.routes.feedback_routes import router as feedback_router
from backend.routes.project_routes import router as project_router
from backend.init_db import create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    create_all()
    yield


app = FastAPI(
    title="AI Student Planner API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(subject_router)
app.include_router(ai_task)
app.include_router(project_router)
app.include_router(feedback_router)

@app.get("/")
def root():
    return {"message": "AI Student Planner API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
