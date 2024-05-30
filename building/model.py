from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base ,relationship
from pydantic import BaseModel


engine = create_engine ('postgresql://postgres:123456@localhost/postgres')
Base = declarative_base()


class Building(Base):
    __tablename__='building'

    building_id = Column(Integer,primary_key=True,autoincrement=True)
    building_name=Column(String(100),nullable=False)
    building_type=Column(String(100),nullable=False)

    waste=relationship('Waste',back_populates='build')

class BuildingPydantic(BaseModel):
    building_id:int
    building_name:str
    building_type:str

    class Config:
        from_attributes = True



Base.metadata.create_all(engine)
