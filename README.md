# IoT Sensor Data Collection Platform

This project is a simple IoT sensor data collection platform designed as a 3-layer architecture:

1. API Layer (FastAPI + REST) — implemented
2. Messaging Layer (Kafka) — to be implemented
3. Data Layer (SQLAlchemy + Database) — to be implemented

Currently, only the API layer is implemented. Sensor data is stored in a temporary in-memory list (“Fake DB”) until the Kafka and Database layers are added.

---

## ▶ How to Run the API Layer (Local)

### 1. Clone the repository
git clone https://github.com/<your-username>/seng315-451-hw2-iot-platform.git  
cd seng315-451-hw2-iot-platform

### 2. Create and activate virtual environment (Windows CMD)
python -m venv venv  
venv\Scripts\activate.bat

### 3. Install dependencies
pip install fastapi uvicorn

### 4. Start the server
uvicorn app.main:app --reload

### 5. Swagger UI (API Docs)
Open your browser and go to the `/docs` endpoint of the running server.

(You can test all endpoints using “Try it out → Execute”.)

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

## 🔮 Future Work
- Kafka Messaging Layer
- SQLAlchemy Database Layer
- Replace Fake DB with real queries
- More analytics (min/max, time-window stats, aggregations)

---

## Notes
This project is part of the SENG315 / SENG451 homework.
