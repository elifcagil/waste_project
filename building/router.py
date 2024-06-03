from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from fastapi import APIRouter,Depends,HTTPException,status
from .model import BuildingPydantic,Building
from enum import Enum
from starlette import status





SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)  #veri tabanına kaydetme işlemi otomatik olarak yapılmaz.commit() i çağırmamzı gerekir
 #sessionlocal yeni bir veri tabanı oturumu(session) oluşturur..
#sessionmaker fonksiyonunun içinde temel veritabanı bağlantısı ve oturumun nasıl davrancağını belirtirirz


router=APIRouter()



def get_db():
    db = SessionLocal() #Oturum Başlatma
    try:
        yield db #Oturumun Kullanıma Sunulması
    finally:
        db.close() #Oturumun Kapatılması



class BuildingEnum(str,Enum):
      yerlesim_yeri="yerleşim yeri"
      akademik_bina="akademik bina"
      idari_bina ="idari bina"
      kafeterya ="kafeterya"



@router.get("/builds/{building_type}",response_model=BuildingPydantic)
async def get_buildings(building_type:BuildingEnum=BuildingEnum,db:Session =Depends(get_db)):
    db_building=db.query(Building).filter(Building.building_type == building_type).first()
    if db_building is None:
        raise HTTPException(detail="No such building", status_code=status.HTTP_404_NOT_FOUND)
    return db_building




@router.post("/add_build", response_model=BuildingPydantic)
async def add_building(building_name: str, building_type: BuildingEnum, db: Session = Depends(get_db)):
    try:
        # Yeni bina oluşturma
        db_building = Building(building_name=building_name,building_type=building_type.value ) # .value ifadesi aldığımı veri setinde yani burada building_type enum değerde olduğu için stringe çevirir
        db.add(db_building)
        db.commit()
        db.refresh(db_building)
        return db_building
    except Exception as e:
        db.rollback() #try bloğunda hata gerçekleşirse yapılan değişiklerş geri almamızı sağlar
        raise HTTPException(status_code=500, detail=str(e))





@router.put("/update_building/{building_name}", response_model=BuildingPydantic)
async def update_building(building_name: str, building_type: BuildingEnum, db: Session = Depends(get_db)):
    db_building = db.query(Building).filter(Building.building_name == building_name).first()
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    db_building.building_type = building_type.value  # db_buildingdeki building_type nesnesine buildingenum daki nesneleri stringe dönüştürüp atıyoruz db_building e referans alması için Building tablosunu verdik bu yüzden building_type db_building nesnesinin içinde
    db.commit()
    db.refresh(db_building)
    return db_building