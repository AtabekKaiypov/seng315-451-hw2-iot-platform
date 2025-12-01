# Kafka Messaging Layer - Kurulum ve Çalıştırma Kılavuzu

## 🎯 Proje Mimarisi

```
Sensör → POST API → Kafka Producer → sensor.readings topic
                                          ↓
                                   Kafka Consumer → SQLite/PostgreSQL DB
                                          ↓
                            GET API ← DB ← CRUD Layer
```

## 📦 Gereksinimler

- Python 3.8+
- Docker & Docker Compose (Kafka için)
- pip

## 🚀 Kurulum Adımları

### 1. Python Bağımlılıklarını Yükle

```bash
pip install -r requirements.txt
```

### 2. Kafka'yı Başlat (Docker ile)

```bash
# Docker Compose ile Kafka ve Zookeeper'ı başlat
docker-compose up -d

# Kafka'nın hazır olduğunu kontrol et
docker logs kafka
```

Kafka `localhost:9092` adresinde çalışacak.

### 3. Veritabanını Hazırla

Veritabanı SQLite kullanıyor ve otomatik oluşturulacak. İlk çalıştırmada `sensor_db.sqlite3` dosyası oluşturulur.

## 🎮 Servisleri Çalıştırma

### Terminal 1: FastAPI (API Layer)

```bash
uvicorn app.main:app --reload --port 8000
```

API: http://localhost:8000
Swagger UI: http://localhost:8000/docs

### Terminal 2: Kafka Consumer

```bash
python -m app.messaging.consumer_service
```

Consumer, Kafka'dan mesajları okuyup veritabanına kaydeder.

## 🧪 Test Senaryosu

### 1. Veri Gönder (POST)

Swagger UI'da veya curl ile:

```bash
curl -X POST "http://localhost:8000/sensor/readings" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "temp_sensor_01",
    "sensor_type": "temperature",
    "value": 23.5
  }'
```

**Ne olur?**
- ✅ API veriyi alır
- ✅ Kafka'ya `sensor.readings` topic'ine gönderir
- ✅ Geçici olarak DB'ye de yazar (hemen response dönmek için)
- ✅ Consumer Kafka'dan okuyup DB'ye kaydeder

### 2. Son Veriyi Oku (GET Latest)

```bash
curl "http://localhost:8000/sensor/readings/latest/temp_sensor_01"
```

### 3. Geçmiş Verileri Oku (GET History)

```bash
curl "http://localhost:8000/sensor/readings/temp_sensor_01?limit=10"
```

### 4. Ortalama Hesapla (Analytics)

```bash
curl "http://localhost:8000/analytics/average?sensor_type=temperature"
```

## 📊 Kafka Topic Yönetimi

### Topic'leri Listele

```bash
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
```

### Topic Detaylarını Gör

```bash
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic sensor.readings
```

### Topic'e Manuel Mesaj Gönder (Test için)

```bash
docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic sensor.readings
```

### Topic'ten Mesaj Oku (Test için)

```bash
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic sensor.readings --from-beginning
```

## 🏗️ Dosya Yapısı

```
app/
├── main.py                      # FastAPI app, endpoints
├── schemas.py                   # Pydantic models
├── database/
│   ├── db.py                    # SQLAlchemy setup
│   ├── models.py                # DB models
│   └── crud.py                  # DB operations
└── messaging/
    ├── config.py                # Kafka config (SENIN İŞİN)
    ├── producer.py              # Kafka producer (SENIN İŞİN)
    └── consumer_service.py      # Kafka consumer (SENIN İŞİN)
```

## 🎓 Hocaya Gösterim Senaryosu

1. **Kafka'yı başlat:**
   ```bash
   docker-compose up -d
   ```

2. **API'yi başlat (Terminal 1):**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Consumer'ı başlat (Terminal 2):**
   ```bash
   python -m app.messaging.consumer_service
   ```

4. **Swagger UI'da test et:**
   - http://localhost:8000/docs
   - POST `/sensor/readings` ile 3-4 farklı sensör verisi gönder
   - Consumer terminal'de logları göster (mesajlar DB'ye kaydediliyor)
   - GET endpoint'leri ile verileri göster

5. **Kafka'yı göster:**
   ```bash
   docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic sensor.readings --from-beginning
   ```

## 🔧 Konfigürasyon

### Kafka Ayarları (app/messaging/config.py)

```python
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
SENSOR_TOPIC = "sensor.readings"
CONSUMER_GROUP_ID = "sensor-consumer-group"
```

### Veritabanı (app/database/db.py)

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./sensor_db.sqlite3"
```

PostgreSQL için değiştir:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/sensor_db"
```

## 🐛 Sorun Giderme

### Kafka bağlanamıyor

```bash
# Kafka container'ını kontrol et
docker ps
docker logs kafka

# Kafka'yı yeniden başlat
docker-compose restart kafka
```

### Consumer çalışmıyor

```bash
# Topic'in oluştuğunu kontrol et
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Consumer log seviyesini artır
# consumer_service.py'de logging.INFO -> logging.DEBUG
```

### DB hatası

```bash
# DB dosyasını sil ve yeniden oluştur
rm sensor_db.sqlite3
# API'yi tekrar başlat (otomatik oluşturur)
```

## 📝 Notlar

- **Duplicate kayıtlar:** Şu an hem API hem Consumer DB'ye yazıyor (response için gerekli). Production'da sadece Kafka'ya gönderip UUID kullanabilirsiniz.
- **Error handling:** Kafka down olsa bile API çalışır (try-catch var).
- **Scalability:** Consumer'ı çoğaltabilirsiniz (consumer group sayesinde).
- **Monitoring:** Production'da Kafka monitoring araçları kullanın (Kafka UI, Prometheus, vb.).

## 🎉 Başarı Kriterleri

✅ POST endpoint Kafka'ya veri gönderiyor
✅ Consumer Kafka'dan veri okuyup DB'ye yazıyor
✅ GET endpoint'leri DB'den veri okuyor
✅ Analytics endpoint çalışıyor
✅ Docker ile Kafka çalışıyor

---

**Hazırlayan:** Messaging Layer Ekibi
**Tarih:** Aralık 2025
**Proje:** SENG315-451 HW2 - IoT Platform

