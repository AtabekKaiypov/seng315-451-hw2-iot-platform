"""
Kafka Producer modülü
Sensör verilerini Kafka topic'ine gönderir.
"""
import json
import logging
from typing import Dict, Any, Optional

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from .config import KAFKA_BOOTSTRAP_SERVERS, SENSOR_TOPIC

logger = logging.getLogger(__name__)

# Global producer instance
_producer: Optional[AIOKafkaProducer] = None


async def start_producer():
    """
    Kafka producer'ı başlatır.
    Uygulama startup'ında çağrılmalı.
    """
    global _producer
    
    try:
        _producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        await _producer.start()
        logger.info(f"Kafka Producer başlatıldı: {KAFKA_BOOTSTRAP_SERVERS}")
    except Exception as e:
        logger.error(f"Kafka Producer başlatılamadı: {e}")
        raise


async def stop_producer():
    """
    Kafka producer'ı durdurur.
    Uygulama shutdown'ında çağrılmalı.
    """
    global _producer
    
    if _producer:
        try:
            await _producer.stop()
            logger.info("Kafka Producer durduruldu")
        except Exception as e:
            logger.error(f"Kafka Producer durdurulurken hata: {e}")
        finally:
            _producer = None


async def publish_sensor_reading(reading: Dict[str, Any]) -> None:
    """
    Sensör verisini Kafka topic'ine gönderir.
    
    Args:
        reading (Dict[str, Any]): Sensör verisi
            - sensor_id: str
            - sensor_type: str
            - value: float
            - timestamp: datetime (string formatında gönderilecek)
    
    Raises:
        RuntimeError: Producer başlatılmamışsa
        KafkaError: Kafka'ya gönderim başarısız olursa
    """
    global _producer
    
    if not _producer:
        raise RuntimeError("Kafka Producer başlatılmamış. Önce start_producer() çağrılmalı.")
    
    try:
        # Sensör ID'yi key olarak kullan (aynı sensörden gelen veriler aynı partition'a gider)
        key = reading.get('sensor_id')
        
        # Timestamp'i string'e çevir (JSON serialization için)
        if 'timestamp' in reading and hasattr(reading['timestamp'], 'isoformat'):
            reading = reading.copy()
            reading['timestamp'] = reading['timestamp'].isoformat()
        
        # Kafka'ya gönder
        await _producer.send_and_wait(SENSOR_TOPIC, value=reading, key=key)
        
        logger.debug(f"Sensör verisi Kafka'ya gönderildi: {key} -> {SENSOR_TOPIC}")
        
    except KafkaError as e:
        logger.error(f"Kafka'ya gönderim hatası: {e}")
        raise
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        raise


async def get_producer_status() -> Dict[str, Any]:
    """
    Producer'ın durumunu döner.
    
    Returns:
        Dict[str, Any]: Producer durumu
    """
    global _producer
    
    return {
        "is_running": _producer is not None,
        "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
        "topic": SENSOR_TOPIC
    }

