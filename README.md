# IoT Sensor Data Collection Platform

This project is a simple IoT sensor data collection platform designed as a 3-layer architecture:

1. ✅ **API Layer (FastAPI + REST)** — TAMAMLANDI
2. ✅ **Messaging Layer (Kafka)** — TAMAMLANDI
3. ✅ **Data Layer (SQLAlchemy + Database)** — TAMAMLANDI

## 📊 Mimari

```
┌─────────────┐
│   Sensör    │
└──────┬──────┘
       │ HTTP POST
       ▼
┌─────────────────────────────┐
│      FastAPI (API Layer)    │
│  • POST /sensor/readings    │
│  • GET endpoints            │
└──────┬──────────────────────┘
       │
       ├─────► Kafka Producer ──► [sensor.readings topic]
       │                                    │
       └─────► DB (geçici)                  │
                                            ▼
                                    Kafka Consumer
                                            │
                                            ▼
                                  ┌─────────────────┐
                                  │  SQLite/Postgres│
                                  │   (Data Layer)  │
                                  └─────────────────┘
                                            │
                                            ▼
                                    CRUD Operations
                                            │
                                            ▼
                                      GET Endpoints
```

---

## 🚀 Hızlı Başlangıç

### Otomatik Kurulum (Önerilen)

**Windows:**
```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Tüm servisleri başlat (Kafka + API + Consumer)
start_all.bat
```

**Linux/Mac:**
```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Tüm servisleri başlat
chmod +x start_all.sh
./start_all.sh
```

### Manuel Kurulum

#### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/seng315-451-hw2-iot-platform.git  
cd seng315-451-hw2-iot-platform
```

#### 2. Create and activate virtual environment
**Windows:**
```bash
python -m venv venv  
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Kafka'yı başlat (Docker)
```bash
docker-compose up -d
```

#### 5. API'yi başlat (Terminal 1)
```bash
uvicorn app.main:app --reload --port 8000
```

#### 6. Consumer'ı başlat (Terminal 2)
```bash
python -m app.messaging.consumer_service
```

#### 7. Test et
```bash
python test_kafka.py
```

veya Swagger UI: http://localhost:8000/docs

---

## 🔌 API Endpoints

### 1. Health Check — GET /
Returns:
{ "message": "API layer is running" }

---

### 2. Create Sensor Reading — POST /sensor/readings
Request example:
{
  "sensor_id": "s1",
  "sensor_type": "temperature",
  "value": 23.5
}

Response:
{
  "id": 1,
  "sensor_id": "s1",
  "sensor_type": "temperature",
  "value": 23.5,
  "timestamp": "2025-11-28T13:50:12.123Z"
}

---

### 3. Get Latest Reading — GET /sensor/readings/latest/{sensor_id}

### 4. Get Sensor History — GET /sensor/readings/{sensor_id}?limit=50

### 5. Get Average By Sensor Type — GET /analytics/average?sensor_type=temperature
Example:
{
  "sensor_type": "temperature",
  "average": 23.8
}

---

## 📁 Proje Yapısı

```
seng315-451-hw2-iot-platform/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, endpoints
│   ├── schemas.py                 # Pydantic models
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                  # SQLAlchemy setup & session
│   │   ├── models.py              # SensorReading model
│   │   └── crud.py                # CRUD operations
│   └── messaging/
│       ├── __init__.py
│       ├── config.py              # Kafka config ⭐ KAFKA LAYER
│       ├── producer.py            # Kafka producer ⭐ KAFKA LAYER
│       └── consumer_service.py    # Kafka consumer ⭐ KAFKA LAYER
├── docker-compose.yml             # Kafka + Zookeeper
├── requirements.txt               # Python dependencies
├── test_kafka.py                  # Integration test
├── start_all.bat                  # Windows auto-start
├── start_all.sh                   # Linux/Mac auto-start
├── KAFKA_SETUP.md                 # Detaylı Kafka kurulum kılavuzu
└── README.md
```

## 🧪 Test Etme

### 1. Otomatik Test Script'i
```bash
python test_kafka.py
```

### 2. Manuel Test (Swagger UI)
1. http://localhost:8000/docs adresine git
2. POST `/sensor/readings` ile veri gönder:
```json
{
  "sensor_id": "temp_sensor_01",
  "sensor_type": "temperature",
  "value": 23.5
}
```
3. Consumer terminal'inde log'ları izle
4. GET endpoint'leri ile verileri sorgula

### 3. Kafka'yı Doğrudan Test Et
```bash
# Kafka topic'ini kontrol et
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Mesajları oku
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic sensor.readings --from-beginning
```

## 📚 Detaylı Dokümantasyon

Kafka entegrasyonu hakkında detaylı bilgi için: **[KAFKA_SETUP.md](KAFKA_SETUP.md)**

## 🎯 Tamamlanan Özellikler

- ✅ FastAPI REST API
- ✅ Pydantic şema validasyonu
- ✅ SQLAlchemy ORM + SQLite database
- ✅ Kafka Producer (async)
- ✅ Kafka Consumer (async, ayrı process)
- ✅ Docker Compose ile Kafka kurulumu
- ✅ CRUD operasyonları
- ✅ Analytics endpoint (ortalama hesaplama)
- ✅ Otomatik başlatma script'leri
- ✅ Integration test script'i

## 🔮 Potansiyel İyileştirmeler

- [ ] PostgreSQL desteği (şu an SQLite)
- [ ] Multiple partition support
- [ ] Error handling & retry logic
- [ ] Monitoring dashboard (Kafka UI, Prometheus)
- [ ] Authentication & authorization
- [ ] Rate limiting
- [ ] Daha fazla analytics (min/max, time-window stats)
- [ ] Kafka Streams ile real-time analytics
- [ ] Message validation & schema registry

## 👥 Ekip

- **API Layer:** Tamamlandı
- **Messaging Layer (Kafka):** Tamamlandı ⭐
- **Data Layer (SQLAlchemy):** Fatih (tamamlandı)

## 📝 Notlar

- Duplicate kayıtlar: Şu an hem API hem Consumer DB'ye yazıyor. Production'da sadece Kafka'ya gönderip UUID kullanabilirsiniz.
- Error handling: Kafka down olsa bile API çalışır.
- Consumer group: Scalability için consumer'ı çoğaltabilirsiniz.

---

**Proje:** SENG315 / SENG451 Homework 2
**Tarım:** Aralık 2025
