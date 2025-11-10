from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.routes.user_routes import router as user_router
from backend.routes.subject_routes import router as subject_router
from backend.init_db import create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    create_all()
    yield
    # Shutdown: Add cleanup logic here if needed
    # e.g., close database connections, cleanup resources


app = FastAPI(
    title="AI Student Planner API",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(user_router)
app.include_router(subject_router)


@app.get("/")
def root():
    return {"message": "AI Student Planner API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
