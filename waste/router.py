from fastapi import APIRouter,Depends,Body,HTTPException,status
from .model import WastePydantic,Waste,WasteEnum
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine
from building.model import BuildingEnum
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError


from enum import Enum



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal() #Oturum Başlatma
    try:
        yield db #Oturumun Kullanıma Sunulması
    finally:
        db.close() #Oturumun Kapatılması

@router.post("/add_waste/", response_model=WastePydantic)
async def add_waste(waste: WastePydantic=Body(...), db: Session = Depends(get_db)):


    if waste.waste_type not in [wt.value for wt in WasteEnum]:
        raise HTTPException(status_code=400, detail="Geçersiz atık türü")
    if waste.building_type not in [wt.value for wt in BuildingEnum]:
        raise HTTPException(status_code=400, detail="Geçersiz bina türü")
    if waste.quantity <= 0 or waste.quantity > 1000:
        raise HTTPException(status_code=400, detail="Yanlış miktar girdiniz")

    db_waste = Waste( building_id=waste.building_id, student_id=waste.student_id,waste_name=waste.waste_name,quantity=waste.quantity,waste_type=waste.waste_type,building_type=waste.building_type)
    db.add(db_waste)
    db.commit()
    db.refresh(db_waste)
    return db_waste




@router.get("/get_wastes/", response_model=list[WastePydantic])
async def get_wastes(skip: int=0,limit:int=100,db: Session = Depends(get_db)):
    db_waste = db.query(Waste).offset(skip).limit(limit).all()
    return db_waste


@router.get("/get_waste/{building_type}",response_model=WastePydantic)
async def get_building_type_waste(building_type:BuildingEnum,db: Session = Depends(get_db)):
    db_waste=db.query(Waste).filter(Waste.building_type == building_type).first()
    if db_waste is None:
        raise HTTPException(status_code=404, detail="Bina bulunamadı")
    return db_waste


@router.get("/wastes/", response_model=List[WastePydantic])
def read_wastes(waste_type: WasteEnum, db: Session = next(get_db())):
    try:
        wastes = db.query(Waste).filter(Waste.waste_type == waste_type).all()
        if not wastes:
            raise HTTPException(status_code=404, detail="Waste not found")
        return wastes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))












@router.put("/update_wastes/{waste_id}", response_model=WastePydantic)
async def update_wastes(waste_id:int, waste:WastePydantic, db:Session = Depends(get_db)):
    db_waste = db.query(Waste).filter(Waste.waste_id == waste_id).first()
    if not db_waste:
        raise HTTPException(status_code=404, detail="Atık bulunamadı,geçersiz id")
    if waste.quantity <= 0 or waste.quantity > 1000:
        raise HTTPException(status_code=400, detail="Yanlış miktar girdiniz")


    db_waste.building_id = waste.building_id
    db_waste.student_id = waste.student_id        #gelen verileri oluşturduğumuz yenidb deki değerlerine atıyoruz
    db_waste.waste_name = waste.waste_name
    db_waste.quantity = waste.quantity
    db_waste.waste_type = waste.waste_type.value
    db_waste.building_type = waste.building_type.value

    #Gelen verileri güncelle bu for fonksiyonu da yukardaki blok ile aynı işlevi yapar
    #for field, value in waste.dict().items():
    #    setattr(db_waste, field, value)


    db.commit()
    db.refresh(db_waste)

    return db_waste


class DeletedWaste(BaseModel):
    waste_id:int
    building_id:int
    building_type:BuildingEnum
    waste_name:str
    quantity:int
    waste_type:WasteEnum
    student_id:int

@router.delete("/waste/{waste_id}",response_model=DeletedWaste)
async def delete_waste(waste_id:int,db: Session = Depends(get_db)):
    db_waste = db.query(Waste).filter(Waste.waste_id == waste_id).first()
    if not db_waste:
        raise HTTPException(status_code=400, detail="Atık bulunamadı")
    db.delete(db_waste)
    db.commit()
    return db_waste



