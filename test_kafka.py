"""
Kafka entegrasyonunu test eden basit script
API'ye veri gönderir ve sonuçları kontrol eder
"""
import requests
import time
from datetime import datetime

API_BASE_URL = "http://localhost:8000"


def test_post_sensor_reading():
    """Sensör verisi gönder"""
    print("\n[TEST 1] POST /sensor/readings - Veri gönderme")
    print("-" * 50)
    
    test_data = {
        "sensor_id": "temp_sensor_01",
        "sensor_type": "temperature",
        "value": 23.5
    }
    
    response = requests.post(f"{API_BASE_URL}/sensor/readings", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200, "POST başarısız!"
    print("✅ POST başarılı!")
    
    return response.json()


def test_get_latest(sensor_id):
    """En son veriyi oku"""
    print(f"\n[TEST 2] GET /sensor/readings/latest/{sensor_id}")
    print("-" * 50)
    
    # Consumer'ın Kafka'dan okuyup DB'ye yazması için biraz bekle
    print("Consumer'ın veriyi işlemesi için 2 saniye bekleniyor...")
    time.sleep(2)
    
    response = requests.get(f"{API_BASE_URL}/sensor/readings/latest/{sensor_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200, "GET latest başarısız!"
    print("✅ GET latest başarılı!")


def test_get_history(sensor_id):
    """Geçmiş verileri oku"""
    print(f"\n[TEST 3] GET /sensor/readings/{sensor_id}?limit=10")
    print("-" * 50)
    
    response = requests.get(f"{API_BASE_URL}/sensor/readings/{sensor_id}?limit=10")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Toplam kayıt sayısı: {len(data)}")
    
    if data:
        print(f"İlk kayıt: {data[0]}")
    
    assert response.status_code == 200, "GET history başarısız!"
    print("✅ GET history başarılı!")


def test_analytics(sensor_type):
    """Ortalama hesaplama"""
    print(f"\n[TEST 4] GET /analytics/average?sensor_type={sensor_type}")
    print("-" * 50)
    
    response = requests.get(f"{API_BASE_URL}/analytics/average", params={"sensor_type": sensor_type})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200, "GET analytics başarısız!"
    print("✅ GET analytics başarılı!")


def send_multiple_readings():
    """Birden fazla sensör verisi gönder"""
    print("\n[TEST 5] Çoklu veri gönderme")
    print("-" * 50)
    
    test_data = [
        {"sensor_id": "temp_sensor_01", "sensor_type": "temperature", "value": 23.5},
        {"sensor_id": "temp_sensor_01", "sensor_type": "temperature", "value": 24.0},
        {"sensor_id": "temp_sensor_02", "sensor_type": "temperature", "value": 22.8},
        {"sensor_id": "humidity_sensor_01", "sensor_type": "humidity", "value": 65.0},
        {"sensor_id": "humidity_sensor_01", "sensor_type": "humidity", "value": 67.5},
    ]
    
    for i, data in enumerate(test_data, 1):
        response = requests.post(f"{API_BASE_URL}/sensor/readings", json=data)
        print(f"  [{i}/{len(test_data)}] {data['sensor_id']} = {data['value']} -> {response.status_code}")
        time.sleep(0.5)  # Rate limiting
    
    print("✅ Çoklu veri gönderme başarılı!")


def main():
    """Ana test fonksiyonu"""
    print("=" * 50)
    print("IoT Platform - Kafka Entegrasyon Testi")
    print("=" * 50)
    print(f"API URL: {API_BASE_URL}")
    print(f"Test Zamanı: {datetime.now()}")
    
    try:
        # API'nin çalıştığını kontrol et
        response = requests.get(f"{API_BASE_URL}/")
        print(f"\n✅ API erişilebilir: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("\n❌ HATA: API'ye bağlanılamıyor!")
        print("Lütfen önce API'yi başlatın: uvicorn app.main:app --reload")
        return
    
    try:
        # Testleri çalıştır
        result = test_post_sensor_reading()
        test_get_latest(result['sensor_id'])
        test_get_history(result['sensor_id'])
        test_analytics(result['sensor_type'])
        send_multiple_readings()
        
        print("\n" + "=" * 50)
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("=" * 50)
        print("\nKafka Consumer terminal'ini kontrol edin.")
        print("Mesajların DB'ye kaydedildiğini göreceksiniz.")
        
    except AssertionError as e:
        print(f"\n❌ TEST BAŞARISIZ: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ BAĞLANTI HATASI: {e}")
    except Exception as e:
        print(f"\n❌ BEKLENMEYEN HATA: {e}")


if __name__ == "__main__":
    main()

