from sqlalchemy import Column, Integer, String,create_engine
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel,EmailStr


engine =create_engine('postgresql://postgres:123456@localhost/postgres')
Base=declarative_base()



class Student(Base):
    __tablename__='student'


    student_id =Column(Integer,primary_key =True,autoincrement =True)
    student_mail=Column(String(50),nullable=False,unique=True )#unique tanımlamak için
    student_password=Column(String(50),nullable=False)
    student_name=Column(String(10),nullable=False)
    student_last_name =Column(String(10),nullable=False)


    waste_1 = relationship('Waste', back_populates='student')



class StudentPydantic(BaseModel):
    student_mail:EmailStr # bu tanımlama e mail yapısında olacağını belirtir
    student_password:str
    student_name:str
    student_last_name:str

    class Config:
        from_attributes = True

Base.metadata.create_all(engine)
