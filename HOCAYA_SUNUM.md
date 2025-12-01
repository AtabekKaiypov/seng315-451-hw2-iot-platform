# 🎓 Hocaya Sunum Kılavuzu

## IoT Platform - Kafka Messaging Layer Entegrasyonu

---

## 📋 Proje Özeti

**Öğrenci:** Messaging Layer Ekibi  
**Tarih:** Aralık 2025  
**Konu:** SENG315-451 HW2 - IoT Sensor Data Collection Platform

### Tamamlanan Katmanlar

- ✅ **API Layer (FastAPI)** - REST endpoints
- ✅ **Messaging Layer (Kafka)** - Producer & Consumer
- ✅ **Data Layer (SQLAlchemy)** - Database CRUD

---

## 🎯 Gösterim Senaryosu

### Adım 1: Kafka'yı Başlat (1 dakika)

```bash
# Terminal'de
cd C:\Users\hp\VsProjects\seng315-451-hw2-iot-platform
docker-compose up -d

# Kafka'nın başladığını göster
docker ps
docker logs kafka --tail 20
```

**Açıklama:** "Kafka ve Zookeeper Docker container'ları başlatıldı. Kafka localhost:9092'de çalışıyor."

---

### Adım 2: API'yi Başlat (30 saniye)

```bash
# Yeni terminal penceresi
uvicorn app.main:app --reload --port 8000
```

**Terminal çıktısı:**
```
INFO:     Kafka Producer başarıyla başlatıldı
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Açıklama:** "FastAPI başlatıldı ve startup event'inde Kafka Producer otomatik başladı."

---

### Adım 3: Consumer Servisini Başlat (30 saniye)

```bash
# Yeni terminal penceresi
python -m app.messaging.consumer_service
```

**Terminal çıktısı:**
```
INFO - === Kafka Consumer Servisi Başlatılıyor ===
INFO - Kafka Consumer başlatıldı: sensor.readings
INFO - Mesajlar bekleniyor...
```

**Açıklama:** "Consumer servisi Kafka topic'inden mesaj okumaya başladı."

---

### Adım 4: Swagger UI'dan Test (3 dakika)

#### 4.1. Swagger'ı Aç

Tarayıcıda: http://localhost:8000/docs

**Açıklama:** "FastAPI otomatik olarak interaktif API dokümantasyonu oluşturdu."

---

#### 4.2. İlk Veriyi Gönder

**Endpoint:** POST `/sensor/readings`

**Body:**
```json
{
  "sensor_id": "temp_sensor_01",
  "sensor_type": "temperature",
  "value": 23.5
}
```

**"Execute" butonuna tıkla**

**Response (200 OK):**
```json
{
  "id": 1,
  "sensor_id": "temp_sensor_01",
  "sensor_type": "temperature",
  "value": 23.5,
  "timestamp": "2025-12-01T22:15:30.123456"
}
```

**Consumer terminal'ini göster:**
```
INFO - Mesaj alındı: partition=0, offset=0
INFO - Veri DB'ye kaydedildi: temp_sensor_01 (temperature) = 23.5
```

**Açıklama:** 
1. "API veriyi aldı"
2. "Kafka Producer veriyi sensor.readings topic'ine gönderdi"
3. "Consumer Kafka'dan mesajı okudu"
4. "SQLAlchemy ile veritabanına kaydetti"

---

#### 4.3. Daha Fazla Veri Gönder

Swagger'dan 3-4 veri daha gönder:

```json
{"sensor_id": "temp_sensor_01", "sensor_type": "temperature", "value": 24.0}
{"sensor_id": "temp_sensor_02", "sensor_type": "temperature", "value": 22.8}
{"sensor_id": "humidity_sensor_01", "sensor_type": "humidity", "value": 65.0}
{"sensor_id": "humidity_sensor_01", "sensor_type": "humidity", "value": 67.5}
```

Her seferinde Consumer terminal'de log göster.

---

#### 4.4. En Son Veriyi Oku

**Endpoint:** GET `/sensor/readings/latest/temp_sensor_01`

**Response:**
```json
{
  "id": 2,
  "sensor_id": "temp_sensor_01",
  "sensor_type": "temperature",
  "value": 24.0,
  "timestamp": "2025-12-01T22:16:45.654321"
}
```

**Açıklama:** "En son kaydedilen veri veritabanından okundu."

---

#### 4.5. Geçmiş Verileri Oku

**Endpoint:** GET `/sensor/readings/temp_sensor_01?limit=10`

**Response:** Liste olarak tüm veriler

**Açıklama:** "Sensör geçmişi timestamp'e göre sıralanmış şekilde döndü."

---

#### 4.6. Ortalama Hesapla (Analytics)

**Endpoint:** GET `/analytics/average?sensor_type=temperature`

**Response:**
```json
{
  "sensor_type": "temperature",
  "average": 23.433333333333334
}
```

**Açıklama:** "SQLAlchemy aggregate fonksiyonu ile tüm temperature sensörlerinin ortalaması hesaplandı."

---

### Adım 5: Kafka Topic'ini Doğrudan Göster (1 dakika)

```bash
# Terminal'de
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
```

**Çıktı:**
```
sensor.readings
```

**Mesajları oku:**
```bash
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic sensor.readings --from-beginning
```

**Çıktı:**
```json
{"sensor_id":"temp_sensor_01","sensor_type":"temperature","value":23.5,"timestamp":"2025-12-01T22:15:30.123456"}
{"sensor_id":"temp_sensor_01","sensor_type":"temperature","value":24.0,"timestamp":"2025-12-01T22:16:45.654321"}
...
```

**Açıklama:** "Tüm mesajlar Kafka topic'inde saklanıyor. Consumer bu mesajları okuyup DB'ye yazıyor."

---

### Adım 6: Veritabanını Göster (30 saniye)

```bash
# SQLite DB'yi kontrol et
sqlite3 sensor_db.sqlite3
```

**SQL sorgula:**
```sql
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 5;
```

**Açıklama:** "Veriler SQLite veritabanında kalıcı olarak saklanıyor."

---

### Adım 7: Test Script'ini Çalıştır (1 dakika)

```bash
python test_kafka.py
```

**Çıktı:**
```
==================================================
IoT Platform - Kafka Entegrasyon Testi
==================================================
[TEST 1] POST /sensor/readings - Veri gönderme
--------------------------------------------------
✅ POST başarılı!

[TEST 2] GET /sensor/readings/latest/temp_sensor_01
--------------------------------------------------
✅ GET latest başarılı!

[TEST 3] GET /sensor/readings/temp_sensor_01?limit=10
--------------------------------------------------
✅ GET history başarılı!

[TEST 4] GET /analytics/average?sensor_type=temperature
--------------------------------------------------
✅ GET analytics başarılı!

[TEST 5] Çoklu veri gönderme
--------------------------------------------------
✅ Çoklu veri gönderme başarılı!

🎉 TÜM TESTLER BAŞARILI!
```

**Açıklama:** "Otomatik test script'i tüm endpoint'leri ve Kafka entegrasyonunu doğruladı."

---

## 📊 Mimari Diyagram (Tahtaya Çiz)

```
┌─────────────┐
│   Sensör    │
└──────┬──────┘
       │ HTTP POST
       ▼
┌───────────────────────────┐
│  FastAPI (port 8000)      │
│  POST /sensor/readings    │
└──────┬────────────────────┘
       │
       ├──► Kafka Producer ──► [sensor.readings topic]
       │                              │
       └──► DB (geçici, ID için)      │
                                      ▼
                              Kafka Consumer
                              (ayrı process)
                                      │
                                      ▼
                            ┌──────────────────┐
                            │  SQLite Database │
                            │  sensor_readings │
                            └──────────────────┘
                                      │
                                      ▼
                              CRUD Operations
                                      │
                                      ▼
                        GET /sensor/readings/latest/{id}
                        GET /sensor/readings/{id}
                        GET /analytics/average
```

---

## 🛠️ Teknik Detaylar

### Kullanılan Teknolojiler

| Katman | Teknoloji | Versiyon |
|--------|-----------|----------|
| API | FastAPI | 0.104.1 |
| Web Server | Uvicorn | 0.24.0 |
| Messaging | Apache Kafka | 7.5.0 (Confluent) |
| Kafka Client | aiokafka | 0.10.0 |
| Database | SQLite | - |
| ORM | SQLAlchemy | 2.0.23 |
| Validation | Pydantic | 2.5.0 |
| Container | Docker Compose | - |

### Dosya Yapısı

```
app/
├── main.py                    # FastAPI, endpoints, startup/shutdown
├── schemas.py                 # Pydantic models (validation)
├── database/
│   ├── db.py                  # SQLAlchemy engine, session
│   ├── models.py              # SensorReading model
│   └── crud.py                # Database operations
└── messaging/                 # ⭐ KAFKA LAYER
    ├── config.py              # Kafka config
    ├── producer.py            # Async producer
    └── consumer_service.py    # Async consumer (ayrı process)
```

### Kafka Configuration

**Topic:** `sensor.readings`  
**Partitions:** 1 (default)  
**Replication Factor:** 1  
**Consumer Group:** `sensor-consumer-group`  
**Serialization:** JSON

### Database Schema

**Table:** `sensor_readings`

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| sensor_id | VARCHAR | NOT NULL, INDEX |
| sensor_type | VARCHAR | NOT NULL, INDEX |
| value | FLOAT | NOT NULL |
| timestamp | DATETIME | NOT NULL, INDEX, DEFAULT now() |

---

## 🎤 Sunum Sırasında Vurgulanacak Noktalar

### 1. Asenkron Yapı
- "aiokafka kullanarak **async/await** pattern'i ile yüksek performanslı messaging"
- "FastAPI doğal olarak async destekliyor"

### 2. Separation of Concerns
- "Producer API içinde, Consumer ayrı process"
- "API çökse bile Consumer çalışmaya devam eder"
- "Horizontal scaling: Consumer'ları çoğaltabiliriz"

### 3. Error Handling
- "Kafka down olsa bile API çalışır (try-catch)"
- "Consumer'da exception handling: Bir mesaj hatalı olsa bile devam eder"

### 4. Data Flow
- "POST → Kafka → Consumer → DB → GET"
- "Decoupling: API ve DB arasında Kafka buffer görevi görüyor"
- "Message durability: Kafka'da mesajlar saklanıyor"

### 5. Scalability
- "Consumer group ile multiple consumer"
- "Kafka partition'ları artırarak throughput yükseltebiliriz"
- "API stateless: Kubernetes'te scale edebiliriz"

---

## ❓ Olası Sorular ve Cevaplar

### S: Neden Kafka kullandınız?

**C:** "Kafka, high-throughput ve fault-tolerant messaging sağlıyor. IoT senaryolarında sensörlerden gelen yüksek hacimli veri akışını buffer'layarak DB'yi koruyabiliriz. Ayrıca mesajlar Kafka'da saklandığı için data loss riski azalıyor."

### S: Consumer neden ayrı process?

**C:** "Separation of concerns. API sadece veri kabul edip Kafka'ya gönderiyor. Consumer ise Kafka'dan okuyup DB işlemlerini yapıyor. Bu sayede API fast response verebiliyor ve consumer bağımsız scale edilebiliyor."

### S: Duplicate kayıtlar oluşmuyor mu?

**C:** "Şu anda hem API hem Consumer DB'ye yazıyor (demo için). Production'da API sadece Kafka'ya gönderir, ID yerine UUID kullanabiliriz. Ya da API response'unda ID döndürmek yerine 'accepted' statüsü dönebiliriz."

### S: Kafka down olursa ne olur?

**C:** "API'de try-catch var, hata loglayıp devam ediyor. İstenirse fallback olarak direkt DB'ye yazabilir. Consumer tarafında ise Kafka tekrar ayağa kalkınca kaldığı yerden devam eder (offset commit sayesinde)."

### S: Birden fazla consumer çalışabilir mi?

**C:** "Evet! Aynı consumer group ID'si ile birden fazla consumer başlatırsanız, Kafka mesajları aralarında dağıtır (load balancing). Her mesajı sadece bir consumer işler."

### S: Message ordering garantisi var mı?

**C:** "Kafka partition seviyesinde ordering garantisi verir. Aynı sensor_id'li mesajlar key olarak gönderildiği için aynı partition'a düşer, sıralı işlenir."

---

## 📸 Ekran Görüntüleri (İsteğe Bağlı)

1. Swagger UI (POST endpoint)
2. Consumer terminal log'ları
3. Kafka console consumer output
4. SQLite database içeriği
5. Test script başarılı sonuç

---

## 🏆 Sonuç

**Tamamlanan:**
- ✅ Kafka Producer (async, JSON serialization)
- ✅ Kafka Consumer (async, ayrı process, DB entegrasyonu)
- ✅ FastAPI startup/shutdown lifecycle integration
- ✅ Docker Compose ile Kafka kurulumu
- ✅ End-to-end data flow test

**Öğrenilen:**
- Event-driven architecture
- Message queue patterns
- Async Python (asyncio, aiokafka)
- Microservices communication
- Docker containerization

**Demo Süresi:** ~10 dakika

---

**Hazır!** 🚀

