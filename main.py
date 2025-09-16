from fastapi import FastAPI
from web.patient_web import patient_router
from web.doctor_web import doctor_router
from web.staff_web import staff_router
from web.appointment_web import appointment_router
from web.auth_web import auth_router

app = FastAPI(
    title="Hospital API",
    description="A FastAPI project for managing hospital patients",
    version="1.0.0",
    contact={
        "name": "Mithilesh Chaurasiya",
        "url": "https://mithilesh-cv.onrender.com/",
        "email": "your.email@example.com",
    },
)

app.include_router(patient_router)
# app.include_router(doctor_router)
# app.include_router(staff_router)
# app.include_router(appointment_router)
# app.include_router(auth_router)
@app.get("/", tags=["Root"])
def hello():
    return {"message": "Welcome to my homepage"}


@app.get("/about", tags=["Root"])
def about():
    return {"message": "This is About page"}
