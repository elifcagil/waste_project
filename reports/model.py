from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel


engine =create_engine('postgresql://postgres:123456@localhost/postgres')
Base =declarative_base()


class Reports(Base):
    __tablename__= 'reports'

    reports_id=Column(Integer ,primary_key=True,autoincrement=True)
    waste_id=Column(Integer,ForeignKey('waste.waste_id'),nullable=False)
    build_id=Column(Integer,nullable=False) #building_type tutmalısın

    waste_3=relationship("Waste",back_populates="reports")


class ReportsPydantic(BaseModel):
    reports_id:int
    waste_id:int
    build_id:int

    class Config:
        from_attributes=True



Base.metadata.create_all(engine)