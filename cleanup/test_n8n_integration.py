#!/usr/bin/env python3
"""
Script de prueba para integración con n8n
Demuestra cómo usar la API de gráficos de velas desde n8n
"""

import requests
import json
import base64
from datetime import datetime

def test_n8n_integration():
    """Prueba la integración específica para n8n"""
    
    base_url = "http://localhost:5002"
    
    print("🔗 PRUEBA DE INTEGRACIÓN CON N8N")
    print("=" * 50)
    
    # 1. Probar el endpoint principal que usará n8n
    print("\n1️⃣ Probando endpoint principal para n8n...")
    
    # Payload exacto que usarías en n8n
    n8n_payload = {
        "symbol": "BTC-USDT",
        "bar": "5m",
        "candles_count": 81
    }
    
    print(f"📤 Payload enviado:")
    print(json.dumps(n8n_payload, indent=2))
    
    try:
        response = requests.post(f"{base_url}/generate-chart", json=n8n_payload)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa!")
            print(f"   Success: {data['success']}")
            print(f"   Símbolo: {data['symbol']}")
            print(f"   Velas generadas: {data['candles_count']}")
            print(f"   Imagen base64: {len(data['image_base64'])} caracteres")
            print(f"   Archivo debug: {data['debug_file']}")
            
            # Información del gráfico
            chart_info = data['chart_info']
            print(f"   Rango de precios: ${chart_info['price_range']['min']:,.2f} - ${chart_info['price_range']['max']:,.2f}")
            print(f"   Precio actual: ${chart_info['current_price']:,.2f}")
            print(f"   Cambio de precio: ${chart_info['price_change']:,.2f}")
            print(f"   Volumen total: {chart_info['total_volume']:,.2f} BTC")
            
            # Guardar imagen
            img_data = base64.b64decode(data['image_base64'])
            filename = f"n8n_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"   Imagen guardada como: {filename}")
            
            return data
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def show_n8n_configuration():
    """Muestra la configuración exacta para n8n"""
    
    print("\n🔧 CONFIGURACIÓN PARA N8N")
    print("=" * 40)
    
    print("📋 1. HTTP Request Node:")
    print("   - Method: POST")
    print("   - URL: http://localhost:5002/generate-chart")
    print("   - Headers: Content-Type: application/json")
    print("   - Body (JSON):")
    print("""
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
""")
    
    print("📋 2. Respuesta esperada:")
    print("""
{
  "success": true,
  "timestamp": "2025-07-27T17:20:00.000000",
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81,
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "debug_file": "debug_api_BTC-USDT_20250727_172000.json",
  "chart_info": {
    "start_time": "2025-07-27T10:00:00",
    "end_time": "2025-07-27T17:20:00",
    "price_range": {
      "min": 118000.0,
      "max": 119500.0
    },
    "current_price": 118950.0,
    "price_change": 150.0,
    "total_volume": 1500.5
  }
}
""")
    
    print("📋 3. Uso en n8n:")
    print("   - Para obtener la imagen: {{ $json.image_base64 }}")
    print("   - Para obtener el precio actual: {{ $json.chart_info.current_price }}")
    print("   - Para obtener el cambio de precio: {{ $json.chart_info.price_change }}")
    print("   - Para obtener el volumen: {{ $json.chart_info.total_volume }}")
    
    print("📋 4. Ejemplos de uso:")
    print("   - Enviar imagen por Telegram: Usar {{ $json.image_base64 }} como archivo")
    print("   - Enviar por email: Adjuntar {{ $json.image_base64 }} como imagen")
    print("   - Guardar en disco: Decodificar base64 y guardar como PNG")
    print("   - Mostrar alertas: Usar {{ $json.chart_info.current_price }} para notificaciones")

def test_different_symbols():
    """Prueba diferentes símbolos"""
    
    base_url = "http://localhost:5002"
    
    print("\n🔄 PROBANDO DIFERENTES SÍMBOLOS")
    print("=" * 40)
    
    symbols = ["BTC-USDT", "ETH-USDT", "ADA-USDT"]
    
    for symbol in symbols:
        print(f"\n📊 Probando {symbol}...")
        
        payload = {
            "symbol": symbol,
            "bar": "5m",
            "candles_count": 20
        }
        
        try:
            response = requests.post(f"{base_url}/generate-chart", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                chart_info = data['chart_info']
                print(f"   ✅ {symbol}: ${chart_info['current_price']:,.2f} (${chart_info['price_change']:,.2f})")
            else:
                print(f"   ❌ {symbol}: Error {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {symbol}: Error de conexión")

def main():
    """Función principal"""
    
    print("🚀 PRUEBA DE INTEGRACIÓN N8N - API DE GRÁFICOS DE VELAS")
    print("=" * 60)
    
    # Probar integración principal
    result = test_n8n_integration()
    
    if result:
        # Mostrar configuración para n8n
        show_n8n_configuration()
        
        # Probar diferentes símbolos
        test_different_symbols()
        
        print("\n" + "=" * 60)
        print("✅ INTEGRACIÓN LISTA PARA N8N")
        print("📝 El servidor está funcionando en: http://localhost:5002")
        print("🔗 Usa el endpoint: POST /generate-chart")
        print("📊 Las imágenes se generan correctamente en formato base64")
        
    else:
        print("\n❌ La integración falló. Verifica que el servidor esté ejecutándose.")

if __name__ == "__main__":
    main() 