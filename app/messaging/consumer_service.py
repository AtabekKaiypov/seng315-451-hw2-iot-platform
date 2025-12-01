"""
Kafka Consumer servisi
Kafka topic'inden sensör verilerini okur ve veritabanına kaydeder.

Bu servis, API'den bağımsız ayrı bir process olarak çalışır:
    python -m app.messaging.consumer_service
"""
import asyncio
import json
import logging
from datetime import datetime

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.messaging.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    SENSOR_TOPIC,
    CONSUMER_GROUP_ID
)
from app.database.db import SessionLocal
from app.database.models import SensorReading

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def save_sensor_reading_to_db(data: dict) -> None:
    """
    Sensör verisini veritabanına kaydeder.
    
    Args:
        data (dict): Kafka'dan gelen sensör verisi
            - sensor_id: str
            - sensor_type: str
            - value: float
            - timestamp: str (ISO format)
    """
    db = SessionLocal()
    try:
        # Timestamp'i parse et
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.utcnow()
        
        # SensorReading modeli oluştur
        db_reading = SensorReading(
            sensor_id=data['sensor_id'],
            sensor_type=data['sensor_type'],
            value=float(data['value']),
            timestamp=timestamp
        )
        
        # Veritabanına kaydet
        db.add(db_reading)
        db.commit()
        
        logger.info(f"Veri DB'ye kaydedildi: {data['sensor_id']} ({data['sensor_type']}) = {data['value']}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"DB'ye kaydetme hatası: {e}")
        raise
    finally:
        db.close()


async def consume_sensor_readings():
    """
    Kafka topic'inden sensör verilerini okur ve işler.
    Bu fonksiyon sürekli çalışır (infinite loop).
    """
    consumer = AIOKafkaConsumer(
        SENSOR_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=CONSUMER_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',  # İlk çalıştırmada en baştan oku
        enable_auto_commit=True
    )
    
    try:
        # Consumer'ı başlat
        await consumer.start()
        logger.info(f"Kafka Consumer başlatıldı: {SENSOR_TOPIC}")
        logger.info(f"Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
        logger.info(f"Consumer group: {CONSUMER_GROUP_ID}")
        logger.info("Mesajlar bekleniyor...")
        
        # Mesajları sürekli dinle
        async for message in consumer:
            try:
                # Mesajı işle
                data = message.value
                logger.debug(f"Mesaj alındı: partition={message.partition}, offset={message.offset}")
                
                # Veritabanına kaydet
                save_sensor_reading_to_db(data)
                
            except Exception as e:
                logger.error(f"Mesaj işlenirken hata: {e}")
                # Hata olsa bile devam et (bir mesaj hatalı olsa bile diğerleri işlensin)
                continue
                
    except KafkaError as e:
        logger.error(f"Kafka hatası: {e}")
        raise
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        raise
    finally:
        # Consumer'ı durdur
        await consumer.stop()
        logger.info("Kafka Consumer durduruldu")


async def main():
    """
    Consumer servisini başlatır.
    """
    logger.info("=== Kafka Consumer Servisi Başlatılıyor ===")
    
    try:
        await consume_sensor_readings()
    except KeyboardInterrupt:
        logger.info("Servis kullanıcı tarafından durduruldu (Ctrl+C)")
    except Exception as e:
        logger.error(f"Servis hatası: {e}")
        raise


if __name__ == "__main__":
    # Asyncio event loop'u çalıştır
    asyncio.run(main())

