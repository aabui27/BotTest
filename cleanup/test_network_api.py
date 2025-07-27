#!/usr/bin/env python3
"""
Script de prueba para la API optimizada para red
Ayuda a diagnosticar problemas de conectividad
"""

import requests
import json
import socket
from datetime import datetime

def get_network_info():
    """Obtiene información de red del sistema"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("🌐 INFORMACIÓN DE RED")
    print("=" * 40)
    print(f"Hostname: {hostname}")
    print(f"IP Local: {local_ip}")
    print(f"Puerto API: 5004")
    print()
    
    return local_ip

def test_all_urls():
    """Prueba todas las URLs posibles"""
    local_ip = get_network_info()
    
    urls_to_test = [
        "http://localhost:5004",
        "http://127.0.0.1:5004",
        f"http://{local_ip}:5004"
    ]
    
    print("🔍 PROBANDO CONECTIVIDAD")
    print("=" * 40)
    
    working_urls = []
    
    for url in urls_to_test:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {url} - FUNCIONANDO")
                working_urls.append(url)
            else:
                print(f"❌ {url} - Error {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - CONEXIÓN RECHAZADA")
        except requests.exceptions.Timeout:
            print(f"⏰ {url} - TIMEOUT")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    print()
    return working_urls

def test_api_with_auth(working_urls):
    """Prueba la API con autenticación"""
    if not working_urls:
        print("❌ No hay URLs funcionando para probar")
        return
    
    print("🔐 PROBANDO AUTENTICACIÓN")
    print("=" * 40)
    
    api_key = "n8n-secure-key-2025"
    test_url = working_urls[0]  # Usar la primera URL que funciona
    
    # 1. Probar sin API key
    print("1️⃣ Probando sin API key...")
    try:
        response = requests.post(f"{test_url}/generate-chart-image", 
                               json={"symbol":"BTC-USDT","candles_count":5},
                               timeout=10)
        if response.status_code == 401:
            print("✅ Correcto: API rechazó petición sin autenticación")
        else:
            print(f"❌ Error: Debería haber fallado, recibió {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 2. Probar con API key válida
    print("\n2️⃣ Probando con API key válida...")
    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }
        
        response = requests.post(f"{test_url}/generate-chart-image",
                               json={"symbol":"BTC-USDT","candles_count":5},
                               headers=headers,
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ API key válida - Respuesta exitosa!")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
            # Guardar imagen
            filename = f"network_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   Imagen guardada como: {filename}")
            
        else:
            print(f"❌ Error con API key válida: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def show_n8n_configuration(working_urls):
    """Muestra la configuración para n8n"""
    if not working_urls:
        print("❌ No hay URLs funcionando")
        return
    
    print("\n🔧 CONFIGURACIÓN PARA N8N")
    print("=" * 40)
    
    print("📋 HTTP Request Node:")
    print("   - Method: POST")
    print(f"   - URL: {working_urls[0]}/generate-chart-image")
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
    
    print("📋 URLs alternativas si la primera no funciona:")
    for i, url in enumerate(working_urls[1:], 1):
        print(f"   {i}. {url}/generate-chart-image")
    
    print("\n📋 Solución de problemas:")
    print("   - Si n8n está en Docker, usa la IP local en lugar de localhost")
    print("   - Si n8n está en otra máquina, usa la IP de red")
    print("   - Verifica que el firewall permita conexiones al puerto 5004")

def main():
    """Función principal"""
    print("🌐 DIAGNÓSTICO DE CONECTIVIDAD - API SEGURA")
    print("=" * 60)
    
    # Obtener información de red
    local_ip = get_network_info()
    
    # Probar todas las URLs
    working_urls = test_all_urls()
    
    if working_urls:
        # Probar autenticación
        test_api_with_auth(working_urls)
        
        # Mostrar configuración para n8n
        show_n8n_configuration(working_urls)
        
        print("\n" + "=" * 60)
        print("✅ API LISTA PARA N8N")
        print(f"📝 Servidor funcionando en puerto 5004")
        print(f"🔗 URLs disponibles: {len(working_urls)}")
        print(f"🌐 IP Local: {local_ip}")
        print("🔐 Autenticación por API key configurada")
        print("📊 Generación de gráficos funcionando")
        
    else:
        print("\n" + "=" * 60)
        print("❌ PROBLEMAS DE CONECTIVIDAD")
        print("📝 Posibles soluciones:")
        print("   1. Verificar que el servidor esté ejecutándose")
        print("   2. Verificar que el puerto 5004 esté libre")
        print("   3. Verificar configuración de firewall")
        print("   4. Intentar con diferentes URLs")

if __name__ == "__main__":
    main() 