from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime

from app.database import models
from app.schemas import SensorReadingIn


def create_sensor_reading(db: Session, reading: SensorReadingIn) -> models.SensorReading:
    """
    Yeni bir sensör verisi oluşturur ve veritabanına kaydeder.
    
    Args:
        db: Database session
        reading: Gelen sensör verisi (SensorReadingIn)
    
    Returns:
        Kaydedilmiş sensör verisi (models.SensorReading)
    """
    # SQLAlchemy modeli oluştur
    db_reading = models.SensorReading(
        sensor_id=reading.sensor_id,
        sensor_type=reading.sensor_type,
        value=reading.value,
        timestamp=reading.timestamp or datetime.utcnow()
    )
    
    # Session'a ekle
    db.add(db_reading)
    
    # Veritabanına kaydet
    db.commit()
    
    # Yeni oluşturulan ID'yi almak için refresh et
    db.refresh(db_reading)
    
    return db_reading


def get_latest_reading(db: Session, sensor_id: str) -> Optional[models.SensorReading]:
    """
    Verilen sensor_id için en son kaydı getirir.
    
    Args:
        db: Database session
        sensor_id: Sensör kimliği
    
    Returns:
        En son kayıt veya None
    """
    return db.query(models.SensorReading)\
        .filter(models.SensorReading.sensor_id == sensor_id)\
        .order_by(desc(models.SensorReading.timestamp))\
        .first()


def get_sensor_history(db: Session, sensor_id: str, limit: int = 50) -> List[models.SensorReading]:
    """
    Verilen sensor_id için geçmiş verileri getirir.
    
    Args:
        db: Database session
        sensor_id: Sensör kimliği
        limit: Maksimum kayıt sayısı
    
    Returns:
        Sensör geçmişi listesi
    """
    return db.query(models.SensorReading)\
        .filter(models.SensorReading.sensor_id == sensor_id)\
        .order_by(desc(models.SensorReading.timestamp))\
        .limit(limit)\
        .all()


def get_average_by_type(db: Session, sensor_type: str) -> Optional[float]:
    """
    Verilen sensor_type için ortalama değeri hesaplar.
    
    Args:
        db: Database session
        sensor_type: Sensör tipi (örn: 'temperature')
    
    Returns:
        Ortalama değer veya None
    """
    result = db.query(func.avg(models.SensorReading.value))\
        .filter(models.SensorReading.sensor_type == sensor_type)\
        .scalar()
    
    # Eğer sonuç None ise (hiç veri yoksa) None döndür
    # Değilse float'a çevir
    return float(result) if result else None
