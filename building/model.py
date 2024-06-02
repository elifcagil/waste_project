from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base ,relationship
from pydantic import BaseModel
from enum import Enum


engine = create_engine ('postgresql://postgres:123456@localhost/postgres')
Base = declarative_base()


class Building(Base):
    __tablename__='building'

    building_id = Column(Integer,primary_key=True,autoincrement=True)
    building_name=Column(String(100),nullable=False)
    building_type=Column(String(100),nullable=False)


    waste = relationship('Waste', back_populates='build')


class BuildingEnum(str, Enum):
    yerlesim_yeri = "Yerleşim yeri"
    akademik_bina = "Akademik bina"
    idari_bina = "İdari bina"
    kafeterya = "Kafeterya"

class BuildingPydantic(BaseModel):
    building_name:str
    building_type:BuildingEnum

    class Config:
        from_attributes = True



Base.metadata.create_all(engine)
