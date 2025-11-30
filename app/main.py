from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db, Base, engine
from app.database import crud, models

app = FastAPI(
    title="IoT Sensor Data Collection Platform - API Layer",
    version="0.1.0"
)


@app.on_event("startup")
def startup_event():
    """
    Uygulama başlarken veritabanı tablolarını oluşturur.
    """
    Base.metadata.create_all(bind=engine)

# -----------------------------
#  Pydantic modelleri (REST)
# -----------------------------

class SensorReadingIn(BaseModel):
    sensor_id: str
    sensor_type: str
    value: float
    timestamp: Optional[datetime] = None


class SensorReadingOut(BaseModel):
    id: int
    sensor_id: str
    sensor_type: str
    value: float
    timestamp: datetime


class AverageResponse(BaseModel):
    sensor_type: str
    average: Optional[float]


# ----------------------------------------
#  FAKE DB KODLARI (Artık kullanılmıyor - gerçek DB kullanıyoruz)
#  Yedek olarak yorum satırında bırakıldı
# ----------------------------------------

# FAKE_DB: List[SensorReadingOut] = []
# _next_id = 1
#
#
# def save_reading_to_fake_db(data: SensorReadingIn) -> SensorReadingOut:
#     """
#     Gerçek DB yokken veriyi RAM'deki listeye kaydettim.
#     Sonra burayı kalan layerları yapacak kişiler değiştirecek.
#     """
#     global _next_id
#
#     ts = data.timestamp or datetime.utcnow()
#
#     record = SensorReadingOut(
#         id=_next_id,
#         sensor_id=data.sensor_id,
#         sensor_type=data.sensor_type,
#         value=data.value,
#         timestamp=ts
#     )
#     _next_id += 1
#     FAKE_DB.append(record)
#     return record
#
#
# def get_latest_from_fake_db(sensor_id: str) -> Optional[SensorReadingOut]:
#     readings = [r for r in FAKE_DB if r.sensor_id == sensor_id]
#     if not readings:
#         return None
#     readings.sort(key=lambda r: r.timestamp, reverse=True)
#     return readings[0]
#
#
# def get_history_from_fake_db(sensor_id: str, limit: int = 50) -> List[SensorReadingOut]:
#     readings = [r for r in FAKE_DB if r.sensor_id == sensor_id]
#     readings.sort(key=lambda r: r.timestamp, reverse=True)
#     return readings[:limit]
#
#
# def get_average_from_fake_db(sensor_type: str) -> Optional[float]:
#     values = [r.value for r in FAKE_DB if r.sensor_type == sensor_type]
#     if not values:
#         return None
#     return sum(values) / len(values)


# -----------------------------
#  REST ENDPOINTLERİ
# -----------------------------

@app.get("/")
def root():
    return {"message": "API layer is running"}


@app.post("/sensor/readings", response_model=SensorReadingOut)
def create_sensor_reading(reading: SensorReadingIn, db: Session = Depends(get_db)):
    """
    Yeni bir sensör verisi alır ve veritabanına kaydeder.
    """
    db_reading = crud.create_sensor_reading(db, reading)
    return SensorReadingOut(
        id=db_reading.id,
        sensor_id=db_reading.sensor_id,
        sensor_type=db_reading.sensor_type,
        value=db_reading.value,
        timestamp=db_reading.timestamp
    )


@app.get(
    "/sensor/readings/latest/{sensor_id}",
    response_model=SensorReadingOut
)
def get_latest_reading(sensor_id: str, db: Session = Depends(get_db)):
    """
    Verilen sensor_id için en son kaydı döner.
    """
    db_reading = crud.get_latest_reading(db, sensor_id)
    if not db_reading:
        raise HTTPException(status_code=404, detail="No data found for this sensor")
    return SensorReadingOut(
        id=db_reading.id,
        sensor_id=db_reading.sensor_id,
        sensor_type=db_reading.sensor_type,
        value=db_reading.value,
        timestamp=db_reading.timestamp
    )


@app.get(
    "/sensor/readings/{sensor_id}",
    response_model=List[SensorReadingOut]
)
def get_sensor_history(sensor_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """
    Verilen sensor_id için geçmiş verileri döner.
    """
    db_readings = crud.get_sensor_history(db, sensor_id, limit)
    return [
        SensorReadingOut(
            id=r.id,
            sensor_id=r.sensor_id,
            sensor_type=r.sensor_type,
            value=r.value,
            timestamp=r.timestamp
        )
        for r in db_readings
    ]


@app.get(
    "/analytics/average",
    response_model=AverageResponse
)
def get_average_value(sensor_type: str, db: Session = Depends(get_db)):
    """
    Verilen sensor_type (örn. 'temperature') için ortalama değeri hesaplar.
    """
    avg = crud.get_average_by_type(db, sensor_type)
    return AverageResponse(sensor_type=sensor_type, average=avg)
