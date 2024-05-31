from sqlalchemy import Column,create_engine,Integer,String,ForeignKey
from sqlalchemy.orm import declarative_base ,relationship
from pydantic import BaseModel



engine=create_engine ('postgresql://postgres:123456@localhost/postgres')
Base=declarative_base()



class Waste_Component(Base):
    __tablename__='waste_component'


    waste_component_id=Column(Integer,primary_key=True,autoincrement=True)
    waste_component_name=Column(String(10),nullable=False)

    waste_2 =relationship('Waste',back_populates='waste_components')

class Waste_ComponentPydantic(BaseModel):
    waste_component:int
    waste_component_id:int

    class Config:
        from_attributes=True




Base.metadata.create_all(bind=engine)

