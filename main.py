from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import employee

from routes.appraisal_cycle import router as cycle_router
from routes.stage import router as stage_router
from routes.parameter import router as parameter_router
from routes.questions import router as question_router
import models
from database.connection import engine
import os

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running on Railway!"}

#existing routes
app.include_router(cycle_router)
app.include_router(stage_router)
app.include_router(parameter_router)
app.include_router(employee.router)
app.include_router(question_router)
