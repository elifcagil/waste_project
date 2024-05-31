from pydantic import BaseModel
from sqlalchemy.orm import Session ,sessionmaker
from sqlalchemy import create_engine
from fastapi import FastAPI,APIRouter,Depends,HTTPException
from .model import Attendant,AttendantPydantic

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



router =APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/attendants/", response_model=list[AttendantPydantic])
async def get_attendants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    attendants = db.query(Attendant).offset(skip).limit(limit).all()
    return attendants
@router.get("/attendant/{attendant_id}/", response_model=AttendantPydantic)
async def get_attendant(attendant_id : int, db:Session = Depends(get_db)):
    db_attendant = db.query(Attendant).filter(Attendant.attendant_id == attendant_id).first()
    if db_attendant is None:
        raise HTTPException(detail="Attendant not found",status_code=404)
    return db_attendant


@router.post("/add_attendant/",response_model=AttendantPydantic)
async def add_attendant(attendant: AttendantPydantic,db:Session = Depends(get_db)):
    db_attendant = Attendant(**attendant.dict())
    db.add(db_attendant)
    db.commit()
    db.refresh(db_attendant)
    return db_attendant


@router.delete("delete_attendant/{attendant_id}",response_model=AttendantPydantic)
async def delete_attendant(attendant_id:int,db:Session = Depends(get_db)):
    db_attendant=db.query(Attendant).filter(Attendant.attendant_id == attendant_id).first()
    if db_attendant is None:
        raise HTTPException(detail="Attendant not found")
    db.delete(db_attendant)
    db.commit()
    return db_attendant

@router.put("/update_attendant/{attendant_id}",response_model=AttendantPydantic)
async def update_attendant(attendant_id:int , attendant:AttendantPydantic,db:Session = Depends(get_db)):
    db_attendant=db.query(Attendant).filter(Attendant.attendant_id == attendant_id).first()
    if db_attendant is None:
        raise HTTPException(detail="Attendant not found")

    for attr,value in vars(attendant).items():
        setattr(db_attendant, attr, value)
    db.commit()
    return db_attendant




