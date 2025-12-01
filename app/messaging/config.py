"""
Kafka konfigürasyon ayarları
"""

# Kafka broker adresi
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# Topic isimleri
SENSOR_TOPIC = "sensor.readings"

# Consumer group ID
CONSUMER_GROUP_ID = "sensor-consumer-group"

# Kafka bağlantı timeout ayarları (ms)
KAFKA_CONNECTION_TIMEOUT = 10000
KAFKA_REQUEST_TIMEOUT = 30000

