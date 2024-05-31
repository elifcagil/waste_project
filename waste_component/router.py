from fastapi import FastAPI, Query, Path, Depends , APIRouter
from enum import Enum
from .model import Waste_ComponentPydantic,Waste_Component


router=APIRouter()

class waste_componentEnum(str,Enum):
    gida_atiklari = "gıda atıkları"
    ambalaj_atıkları = "ambalaj atıkları"
    cam_atiklari = "cam atıkları"
    diger_atiklari = "diğer atıklar"
@router.get("/waste_componenet" ,response_model=Waste_ComponentPydantic)
async def get_waste_component(waste_component_id : int,waste_component_name : waste_componentEnum):
    return {"message":{get_waste_component}}