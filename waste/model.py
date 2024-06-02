from sqlalchemy import Column,create_engine,Integer,String,ForeignKey,Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel,EmailStr
from enum import Enum



engine=create_engine ('postgresql://postgres:123456@localhost/postgres') #veritabanına bağlanmak için bir veritabanı motoru oluşturur.
Base=declarative_base() #orm modellerinin türetilmesi için temel class oluşturmaya yarar.

class Building(Base):
    __tablename__='building'

    building_id = Column(Integer,primary_key=True,autoincrement=True)
    building_name=Column(String(100),nullable=False)
    building_type=Column(String(100),nullable=False) #Enum(BuildingEnum) yazarak tipini enum aldığını belirtebilirsin


    waste = relationship('Waste', back_populates='building')


class BuildingEnum(str, Enum):
    yerlesim_yeri = "Yerleşim yeri"
    akademik_bina = "Akademik bina"
    idari_bina = "İdari bina"
    kafeterya = "Kafeterya"

class BuildingPydantic(BaseModel):
    building_name:str
    building_type:BuildingEnum



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

class WasteEnum(str, Enum):
    gida_atiklari = "Gıda Atıkları"
    ambalaj_atiklari = "Ambalaj Atıkları"
    cam_atiklari = "Cam Atıkları"
    diger_atiklar = "Diğer Atıklar"

class Waste(Base):
    __tablename__='waste'

    waste_id=Column (Integer,primary_key=True,autoincrement=True)
    building_id=Column (Integer,ForeignKey('building.building_id'),nullable=False)
    student_id=Column(Integer,ForeignKey('student.student_id'),nullable=False)
    waste_name=Column(String(20),nullable=False)
    quantity=Column(Integer,nullable=False)
    waste_type = Column(SQLAlchemyEnum(WasteEnum))
    building_type = Column(SQLAlchemyEnum(BuildingEnum))  #tuttuğumuz değerin enum olduğunu belirtiriz


    building=relationship('Building',back_populates='waste')
    student =relationship('Student',back_populates='waste_1')

class WastePydantic(BaseModel):
    building_id:int
    student_id:int
    waste_name:str
    quantity:int
    waste_type: WasteEnum
    building_type :BuildingEnum
    class Config:
        from_attributes = True #orm modellemesi için bu class yapısı kullanıldı bize pydantic modellemesinde kolaylık sağladı

Base.metadata.create_all(engine) #tanımlanan tüm modelleri veritabanında oluşturur.
