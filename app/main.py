from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="IoT Sensor Data Collection Platform - API Layer",
    version="0.1.0"
)

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
#  Şimdilik FAKE DB (sadece RAM'de liste)
#  SONRA: Data + Messaging layer burayı değiştirecek.
# ----------------------------------------

FAKE_DB: List[SensorReadingOut] = []
_next_id = 1


def save_reading_to_fake_db(data: SensorReadingIn) -> SensorReadingOut:
    """
    Gerçek DB yokken veriyi RAM'deki listeye kaydettim.
    Sonra burayı kalan layerları yapacak kişiler değiştirecek.
    """
    global _next_id

    ts = data.timestamp or datetime.utcnow()

    record = SensorReadingOut(
        id=_next_id,
        sensor_id=data.sensor_id,
        sensor_type=data.sensor_type,
        value=data.value,
        timestamp=ts
    )
    _next_id += 1
    FAKE_DB.append(record)
    return record


def get_latest_from_fake_db(sensor_id: str) -> Optional[SensorReadingOut]:
    readings = [r for r in FAKE_DB if r.sensor_id == sensor_id]
    if not readings:
        return None
    readings.sort(key=lambda r: r.timestamp, reverse=True)
    return readings[0]


def get_history_from_fake_db(sensor_id: str, limit: int = 50) -> List[SensorReadingOut]:
    readings = [r for r in FAKE_DB if r.sensor_id == sensor_id]
    readings.sort(key=lambda r: r.timestamp, reverse=True)
    return readings[:limit]


def get_average_from_fake_db(sensor_type: str) -> Optional[float]:
    values = [r.value for r in FAKE_DB if r.sensor_type == sensor_type]
    if not values:
        return None
    return sum(values) / len(values)


# -----------------------------
#  REST ENDPOINTLERİ
# -----------------------------

@app.get("/")
def root():
    return {"message": "API layer is running"}


@app.post("/sensor/readings", response_model=SensorReadingOut)
def create_sensor_reading(reading: SensorReadingIn):
    """
    Yeni bir sensör verisi alır ve (şimdilik) fake DB'ye kaydeder.
    İLERDE:
    - Kafka'ya publish
    - Gerçek DB'ye yazma
    buraya eklenecek.
    """
    record = save_reading_to_fake_db(reading)
    return record


@app.get(
    "/sensor/readings/latest/{sensor_id}",
    response_model=SensorReadingOut
)
def get_latest_reading(sensor_id: str):
    """
    Verilen sensor_id için en son kaydı döner.
    """
    record = get_latest_from_fake_db(sensor_id)
    if not record:
        raise HTTPException(status_code=404, detail="No data found for this sensor")
    return record


@app.get(
    "/sensor/readings/{sensor_id}",
    response_model=List[SensorReadingOut]
)
def get_sensor_history(sensor_id: str, limit: int = 50):
    """
    Verilen sensor_id için geçmiş verileri döner.
    """
    return get_history_from_fake_db(sensor_id, limit)


@app.get(
    "/analytics/average",
    response_model=AverageResponse
)
def get_average_value(sensor_type: str):
    """
    Verilen sensor_type (örn. 'temperature') için ortalama değeri hesaplar.
    """
    avg = get_average_from_fake_db(sensor_type)
    return AverageResponse(sensor_type=sensor_type, average=avg)
