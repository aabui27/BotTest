#!/usr/bin/env python3
"""
Script de prueba simple para n8n - Usa el endpoint que funciona
"""

import requests
import json
import base64
from datetime import datetime

def test_n8n_simple():
    """Prueba la integración usando el endpoint que funciona"""
    
    base_url = "http://localhost:5002"
    
    print("🔗 PRUEBA SIMPLE PARA N8N")
    print("=" * 40)
    
    # Usar el endpoint que sabemos que funciona
    print("\n1️⃣ Probando endpoint de imagen directa...")
    
    payload = {
        "symbol": "BTC-USDT",
        "bar": "5m",
        "candles_count": 81
    }
    
    print(f"📤 Payload enviado:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(f"{base_url}/generate-chart-image", json=payload)
        
        if response.status_code == 200:
            print("✅ Respuesta exitosa!")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
            # Guardar imagen
            filename = f"n8n_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   Imagen guardada como: {filename}")
            
            return True
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def show_n8n_configuration():
    """Muestra la configuración para n8n"""
    
    print("\n🔧 CONFIGURACIÓN PARA N8N")
    print("=" * 40)
    
    print("📋 Opción 1 - Imagen directa (Recomendada):")
    print("   - Method: POST")
    print("   - URL: http://localhost:5002/generate-chart-image")
    print("   - Headers: Content-Type: application/json")
    print("   - Body (JSON):")
    print("""
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
""")
    print("   - Respuesta: Imagen PNG directa")
    
    print("\n📋 Opción 2 - JSON con base64:")
    print("   - Method: POST")
    print("   - URL: http://localhost:5002/generate-chart")
    print("   - Headers: Content-Type: application/json")
    print("   - Body: Mismo JSON que arriba")
    print("   - Respuesta: JSON con imagen en base64")
    
    print("\n📋 Uso en n8n:")
    print("   - Opción 1: Usar directamente como archivo adjunto")
    print("   - Opción 2: Decodificar {{ $json.image_base64 }} y usar como imagen")
    
    print("\n📋 Ejemplos de uso:")
    print("   - Telegram: Adjuntar imagen directamente")
    print("   - Email: Adjuntar imagen como archivo")
    print("   - Discord: Subir imagen al canal")
    print("   - Slack: Enviar imagen al canal")

def main():
    """Función principal"""
    
    print("🚀 PRUEBA SIMPLE N8N - API DE GRÁFICOS DE VELAS")
    print("=" * 50)
    
    # Probar integración
    success = test_n8n_simple()
    
    if success:
        # Mostrar configuración para n8n
        show_n8n_configuration()
        
        print("\n" + "=" * 50)
        print("✅ INTEGRACIÓN LISTA PARA N8N")
        print("📝 El servidor está funcionando en: http://localhost:5002")
        print("🔗 Usa el endpoint: POST /generate-chart-image")
        print("📊 Las imágenes se generan correctamente")
        print("💡 Recomendación: Usa el endpoint de imagen directa para mayor simplicidad")
        
    else:
        print("\n❌ La integración falló. Verifica que el servidor esté ejecutándose.")

if __name__ == "__main__":
    main() 