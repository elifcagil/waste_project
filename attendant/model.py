from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel,EmailStr

engine = create_engine ('postgresql://postgres:123456@localhost/postgres')
Base = declarative_base()


class Attendant(Base):
    __tablename__='attendant'


    attendant_id = Column(Integer,primary_key=True,autoincrement=True)
    attendant_name =Column(String(50),nullable=False)
    attendant_last_name=Column(String(50),nullable=False)
    attendant_mail= Column(String(50),nullable=False,unique=True)
    attendant_password = Column(String(10),nullable=False)


class AttendantPydantic(BaseModel):
    attendant_name :str
    attendant_last_name:str
    attendant_mail:EmailStr
    attendant_password:str


Base.metadata.create_all(engine)

