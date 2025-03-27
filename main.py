from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.appraisal_cycle import router as cycle_router
from routes.stage import router as stage_router
from routes.parameter import router as parameter_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#existing routes
app.include_router(cycle_router)
app.include_router(stage_router)
app.include_router(parameter_router)