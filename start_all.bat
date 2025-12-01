@echo off
REM IoT Platform - Tüm Servisleri Başlatma Script'i (Windows)

echo ================================
echo IoT Platform Servisleri Baslatiliyor...
echo ================================

echo.
echo [1/4] Kafka ve Zookeeper baslatiliyor (Docker)...
docker-compose up -d

echo.
echo [2/4] Kafka'nin hazir olmasini bekliyoruz (5 saniye)...
timeout /t 5 /nobreak > nul

echo.
echo [3/4] FastAPI baslatiliyor (yeni terminal penceresi)...
start cmd /k "uvicorn app.main:app --reload --port 8000"

echo.
echo [4/4] Kafka Consumer baslatiliyor (yeni terminal penceresi)...
timeout /t 2 /nobreak > nul
start cmd /k "python -m app.messaging.consumer_service"

echo.
echo ================================
echo Tum servisler baslatildi!
echo ================================
echo.
echo API: http://localhost:8000
echo Swagger UI: http://localhost:8000/docs
echo.
echo Kafka durumunu kontrol etmek icin:
echo   docker logs kafka
echo.
echo Servisleri durdurmak icin:
echo   docker-compose down
echo.
pause

