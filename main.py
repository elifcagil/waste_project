from fastapi import FastAPI
from student.router import router as student_route
from attendant.router import router as attendant_route
from building.router import router as building_route
from waste.router import router as waste_route
app= FastAPI()

app.include_router(student_route,prefix="/api")
app.include_router(attendant_route,prefix="/api")
app.include_router(building_route,prefix="/api")
app.include_router(waste_route,prefix="/api")
