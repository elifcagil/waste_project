from sqlalchemy import Column,create_engine,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel


engine=create_engine ('postgresql://postgres:123456@localhost/postgres') #veritabanına bağlanmak için bir veritabanı motoru oluşturur.
Base=declarative_base() #orm modellerinin türetilmesi için temel class oluşturmaya yarar.




class Waste(Base):
    __tablename__='waste'

    waste_id=Column (Integer,primary_key=True,autoincrement=True)
    building_id=Column (Integer,ForeignKey('building.building_id'),nullable=False)
    student_id=Column(Integer,ForeignKey('student.student_id'),nullable=False)
    waste_component_id=Column(Integer,ForeignKey('waste_component.waste_component_id'),nullable=False)
    waste_name=Column(String(20),nullable=False)
    quantity=Column(Integer,nullable=False)

    build=relationship('Building',back_populates='waste')
    student =relationship('Student',back_populates='waste_1')
    waste_components=relationship('Waste_Component',back_populates='waste_2')
    reports=relationship('Report',back_populates='waste_3')

class WastePydantic(BaseModel):
    waste_id:int
    building_id:int
    student_id:int
    waste_componenet_name:str
    waste_name:str
    quantity:int

    class Config:
        from_attributes = True #orm modellemesi için bu class yapısı kullanıldı bize pydantic modellemesinde kolaylık sağladı

Base.metadata.create_all(engine) #tanımlanan tüm modelleri veritabanında oluşturur.
