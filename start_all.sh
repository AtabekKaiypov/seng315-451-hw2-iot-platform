#!/bin/bash
# IoT Platform - Tüm Servisleri Başlatma Script'i (Linux/Mac)

echo "================================"
echo "IoT Platform Servisleri Başlatılıyor..."
echo "================================"

echo ""
echo "[1/4] Kafka ve Zookeeper başlatılıyor (Docker)..."
docker-compose up -d

echo ""
echo "[2/4] Kafka'nın hazır olmasını bekliyoruz (5 saniye)..."
sleep 5

echo ""
echo "[3/4] FastAPI başlatılıyor (arka planda)..."
uvicorn app.main:app --reload --port 8000 &
API_PID=$!
echo "API PID: $API_PID"

echo ""
echo "[4/4] Kafka Consumer başlatılıyor (arka planda)..."
sleep 2
python -m app.messaging.consumer_service &
CONSUMER_PID=$!
echo "Consumer PID: $CONSUMER_PID"

echo ""
echo "================================"
echo "Tüm servisler başlatıldı!"
echo "================================"
echo ""
echo "API: http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo ""
echo "Process ID'ler:"
echo "  API: $API_PID"
echo "  Consumer: $CONSUMER_PID"
echo ""
echo "Kafka durumunu kontrol etmek için:"
echo "  docker logs kafka"
echo ""
echo "Servisleri durdurmak için:"
echo "  docker-compose down"
echo "  kill $API_PID $CONSUMER_PID"
echo ""

