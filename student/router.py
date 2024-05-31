from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,EmailStr

import student.model
from .model import StudentPydantic,Student
from sqlalchemy.orm import Session ,sessionmaker
from sqlalchemy import create_engine



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


router=APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/students/", response_model = list[StudentPydantic]) #referans aldığımız modelden gelen her veri listenin içinde tutuluyor
def read_students(skip: int = 0, limit: int = 10, db: SessionLocal = Depends(get_db)): #skip ve limit veri tabanından alınacak kişilerin sayısını ve aralığını bildirir arada kaç kişi olacağını bildirir
    students = db.query(Student).offset(skip).limit(limit).all() #students değişkenine skip ve limit değerleri sınıflandırılarak atanır(aall ile hepsi demek)
    return students #filtrelediğimiz öğrencileri atadığımız değişkeni geri döndürür.

@router.get ("/student/{student_id}",response_model =StudentPydantic)
async def get_student(student_id:int,db:Session =Depends(get_db)):
    db_student =db.query (Student).filter(Student.student_id==student_id).first()
    if db_student is None:
        raise HTTPException(detail="student not found")
    return db_student


@router.post("/add_student/",response_model=StudentPydantic)
def add_student (student:StudentPydantic,db:Session = Depends(get_db)):
    db_student =Student (**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


class DeletedStudent(BaseModel):
    student_id:int
    student_mail:EmailStr
    student_password:str
    student_name:str
    student_last_name:str

@router.delete("/student_delete/{student_id}",response_model=DeletedStudent)
def delete_student(student_id:int,db:Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404,detail="student not found")


    db.delete(db_student)
    db.commit()
    return db_student


@router.put("student_update/{student_id}",response_model=StudentPydantic)
def update_student(student_id:int, student : StudentPydantic,db:Session =Depends(get_db)):
    db_student = db.query(Student).filter(Student.student_id ==student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404,detail="Student not found")

    for attr,value in vars(student).items():
        setattr(db_student, attr, value)
    db.commit()
    return db_student