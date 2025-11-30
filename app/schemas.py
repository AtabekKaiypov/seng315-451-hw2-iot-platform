from datetime import datetime
from typing import Optional
from pydantic import BaseModel


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

