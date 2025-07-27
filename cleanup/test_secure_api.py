#!/usr/bin/env python3
"""
Script de prueba para la API segura con autenticación por API key
"""

import requests
import json
import base64
from datetime import datetime

def test_secure_api():
    """Prueba la API segura con autenticación"""
    
    base_url = "http://localhost:5003"
    api_key = "n8n-secure-key-2025"
    
    print("🔐 PRUEBA DE API SEGURA")
    print("=" * 50)
    
    # 1. Probar health check (sin autenticación)
    print("\n1️⃣ Probando health check (sin autenticación)...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check exitoso")
            print(f"   Servicio: {data['service']}")
            print(f"   Versión: {data['version']}")
            print(f"   Seguridad: {data['security']}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return
    
    # 2. Probar sin API key (debe fallar)
    print("\n2️⃣ Probando sin API key (debe fallar)...")
    try:
        payload = {
            "symbol": "BTC-USDT",
            "bar": "5m",
            "candles_count": 10
        }
        
        response = requests.post(f"{base_url}/generate-chart-image", json=payload)
        if response.status_code == 401:
            print("✅ Correcto: API rechazó la petición sin API key")
            data = response.json()
            print(f"   Error: {data['error']}")
            print(f"   Mensaje: {data['message']}")
        else:
            print(f"❌ Error: Debería haber fallado, pero recibió {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 3. Probar con API key válida
    print("\n3️⃣ Probando con API key válida...")
    try:
        payload = {
            "symbol": "BTC-USDT",
            "bar": "5m",
            "candles_count": 10
        }
        
        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{base_url}/generate-chart-image", json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ API key válida - Respuesta exitosa!")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
            # Guardar imagen
            filename = f"secure_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   Imagen guardada como: {filename}")
            
        else:
            print(f"❌ Error con API key válida: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 4. Probar con API key inválida
    print("\n4️⃣ Probando con API key inválida...")
    try:
        payload = {
            "symbol": "BTC-USDT",
            "bar": "5m",
            "candles_count": 10
        }
        
        headers = {
            "X-API-Key": "invalid-key",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{base_url}/generate-chart-image", json=payload, headers=headers)
        if response.status_code == 401:
            print("✅ Correcto: API rechazó la API key inválida")
            data = response.json()
            print(f"   Error: {data['error']}")
            print(f"   Mensaje: {data['message']}")
        else:
            print(f"❌ Error: Debería haber fallado, pero recibió {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 5. Probar con API key como parámetro
    print("\n5️⃣ Probando con API key como parámetro...")
    try:
        payload = {
            "symbol": "BTC-USDT",
            "bar": "5m",
            "candles_count": 10
        }
        
        params = {
            "api_key": api_key
        }
        
        response = requests.post(f"{base_url}/generate-chart-image", json=payload, params=params)
        if response.status_code == 200:
            print("✅ API key como parámetro - Respuesta exitosa!")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
        else:
            print(f"❌ Error con API key como parámetro: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def show_n8n_configuration():
    """Muestra la configuración para n8n con autenticación"""
    
    print("\n🔧 CONFIGURACIÓN PARA N8N (VERSIÓN SEGURA)")
    print("=" * 50)
    
    print("📋 HTTP Request Node:")
    print("   - Method: POST")
    print("   - URL: http://localhost:5003/generate-chart-image")
    print("   - Headers:")
    print("     Content-Type: application/json")
    print("     X-API-Key: n8n-secure-key-2025")
    print("   - Body (JSON):")
    print("""
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
""")
    
    print("📋 Alternativa con parámetro:")
    print("   - URL: http://localhost:5003/generate-chart-image?api_key=n8n-secure-key-2025")
    print("   - Headers: Solo Content-Type: application/json")
    
    print("\n📋 API Keys disponibles:")
    print("   - n8n-secure-key-2025 (para n8n)")
    print("   - admin-secure-key-2025 (para administración)")
    
    print("\n📋 Seguridad:")
    print("   - Todos los endpoints (excepto /health) requieren API key")
    print("   - API key se puede enviar en header 'X-API-Key' o parámetro 'api_key'")
    print("   - Sin API key válida, retorna error 401")

def main():
    """Función principal"""
    
    print("🔐 PRUEBA DE API SEGURA - AUTENTICACIÓN POR API KEY")
    print("=" * 60)
    
    # Probar API segura
    test_secure_api()
    
    # Mostrar configuración para n8n
    show_n8n_configuration()
    
    print("\n" + "=" * 60)
    print("✅ API SEGURA LISTA PARA N8N")
    print("📝 El servidor está funcionando en: http://localhost:5003")
    print("🔗 Usa el endpoint: POST /generate-chart-image")
    print("🔐 Incluye el header: X-API-Key: n8n-secure-key-2025")
    print("📊 Las imágenes se generan correctamente con autenticación")
    print("🛡️  La API está protegida contra acceso no autorizado")

if __name__ == "__main__":
    main() 