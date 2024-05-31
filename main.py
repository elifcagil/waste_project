from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from waste_component.router import router as waste_route
from student.router import router as student_route
from attendant.router import router as attendant_route

app= FastAPI()

app.include_router(waste_route,prefix="/api")
app.include_router(student_route,prefix="/api")
app.include_router(attendant_route,prefix="/api")
