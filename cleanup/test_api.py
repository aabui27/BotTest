#!/usr/bin/env python3
"""
Script de prueba para la API de gráficos de velas
"""

import requests
import json
import base64
from datetime import datetime

def test_api():
    """Prueba todos los endpoints de la API"""
    
    base_url = "http://localhost:5002"
    
    print("🧪 PROBANDO API DE GRÁFICOS DE VELAS")
    print("=" * 50)
    
    # 1. Probar health check
    print("\n1️⃣ Probando health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check exitoso")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return
    
    # 2. Probar chart info
    print("\n2️⃣ Probando chart info...")
    try:
        response = requests.get(f"{base_url}/chart-info?symbol=BTC-USDT&candles_count=10")
        if response.status_code == 200:
            data = response.json()
            print("✅ Chart info exitoso")
            print(f"   Símbolo: {data['symbol']}")
            print(f"   Velas: {data['candles_count']}")
            print(f"   Precio actual: ${data['price_stats']['current_price']:,.2f}")
            print(f"   Rango de tiempo: {data['time_range']['start']} a {data['time_range']['end']}")
        else:
            print(f"❌ Chart info falló: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error en chart info: {e}")
    
    # 3. Probar generate chart (JSON con base64)
    print("\n3️⃣ Probando generate chart (JSON)...")
    try:
        payload = {
            "symbol": "BTC-USDT",
            "bar": "5m",
            "candles_count": 20
        }
        
        response = requests.post(f"{base_url}/generate-chart", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Generate chart exitoso")
            print(f"   Success: {data['success']}")
            print(f"   Símbolo: {data['symbol']}")
            print(f"   Velas generadas: {data['candles_count']}")
            print(f"   Imagen base64: {len(data['image_base64'])} caracteres")
            print(f"   Archivo debug: {data['debug_file']}")
            
            # Guardar imagen
            img_data = base64.b64decode(data['image_base64'])
            filename = f"test_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"   Imagen guardada como: {filename}")
            
        else:
            print(f"❌ Generate chart falló: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error en generate chart: {e}")
    
    # 4. Probar generate chart image (imagen directa)
    print("\n4️⃣ Probando generate chart image...")
    try:
        payload = {
            "symbol": "BTC-USDT",
            "bar": "5m",
            "candles_count": 15
        }
        
        response = requests.post(f"{base_url}/generate-chart-image", json=payload)
        if response.status_code == 200:
            print("✅ Generate chart image exitoso")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
            # Guardar imagen
            filename = f"test_chart_direct_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   Imagen guardada como: {filename}")
            
        else:
            print(f"❌ Generate chart image falló: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error en generate chart image: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")

def test_n8n_format():
    """Prueba el formato específico para n8n"""
    
    print("\n🔗 FORMATO PARA N8N")
    print("=" * 30)
    
    base_url = "http://localhost:5002"
    
    # Ejemplo de payload para n8n
    n8n_payload = {
        "symbol": "BTC-USDT",
        "bar": "5m",
        "candles_count": 81
    }
    
    print("📤 Payload para n8n:")
    print(json.dumps(n8n_payload, indent=2))
    
    print("\n📥 Respuesta esperada:")
    print("""
{
  "success": true,
  "timestamp": "2025-07-27T16:30:00.000000",
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81,
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "debug_file": "debug_api_BTC-USDT_20250727_163000.json",
  "chart_info": {
    "start_time": "2025-07-27T10:00:00",
    "end_time": "2025-07-27T16:30:00",
    "price_range": {
      "min": 118000.0,
      "max": 119500.0
    },
    "total_volume": 1500.5
  }
}
""")
    
    print("🔧 Configuración en n8n:")
    print("""
1. HTTP Request Node:
   - Method: POST
   - URL: http://localhost:5000/generate-chart
   - Headers: Content-Type: application/json
   - Body: JSON con el payload

2. Para usar la imagen:
   - Decodificar base64: {{ $json.image_base64 }}
   - Guardar como archivo o enviar por email/telegram
""")

if __name__ == "__main__":
    test_api()
    test_n8n_format() 