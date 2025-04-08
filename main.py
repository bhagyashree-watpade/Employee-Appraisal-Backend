from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import employee

from routes.appraisal_cycle import router as cycle_router
from routes.stage import router as stage_router
from routes.parameter import router as parameter_router
from routes.questions import router as question_router
from routes.login import router as login_router
from routes.assignment import router as assignment_router
from routes.employee_allocation import router as employee_allocation_router
from routes.lead_assessment import router as lead_assessment_router

app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"], 
     # allow_origins=["https://employee-appraisal-frontend-kz69.vercel.app"],  #akanksha
    allow_origins=["https://employee-appraisal-frontend-finalllllllllll.vercel.app"],   #bhagyashree
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#existing routes
app.include_router(cycle_router)
app.include_router(stage_router)
app.include_router(parameter_router)
app.include_router(employee.router)
app.include_router(question_router)
app.include_router(login_router)
app.include_router(assignment_router)
app.include_router(employee_allocation_router)
app.include_router(lead_assessment_router)
