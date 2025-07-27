#!/usr/bin/env python3
"""
Script para analizar y mostrar la información de debug de la API de OKX
"""

import json
import os
from datetime import datetime
import pandas as pd

def analyze_debug_file(filename):
    """Analiza un archivo de debug y muestra información resumida"""
    
    if not os.path.exists(filename):
        print(f"Error: El archivo {filename} no existe")
        return
    
    print(f"=== ANÁLISIS DEL ARCHIVO DE DEBUG: {filename} ===\n")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Información básica
    print(f"📅 Timestamp de ejecución: {data['timestamp']}")
    print(f"💰 Símbolo: {data['symbol']}")
    print()
    
    # Información de la API
    print("🌐 INFORMACIÓN DE LA API:")
    print(f"   URL: {data['api_request']['url']}")
    print(f"   Parámetros: {data['api_request']['parameters']}")
    print(f"   Status Code: {data['api_response']['status_code']}")
    print(f"   Total de velas recibidas: {data['api_response']['total_candles_received']}")
    print()
    
    # Información de datos procesados
    print("📊 DATOS PROCESADOS:")
    print(f"   Velas utilizadas para el gráfico: {data['processed_data']['candles_used_for_chart']}")
    print()
    
    # Mostrar las primeras y últimas velas
    raw_data = data['api_response']['raw_data']
    processed_data = data['processed_data']['data']
    
    print("🕯️  PRIMERAS 5 VELAS (más recientes):")
    for i, candle in enumerate(processed_data[:5]):
        timestamp = datetime.fromtimestamp(int(candle[0]) / 1000)
        print(f"   {i+1}. {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Open: {candle[1]}, High: {candle[2]}, Low: {candle[3]}, Close: {candle[4]}")
    
    print()
    print("🕯️  ÚLTIMAS 5 VELAS (más antiguas):")
    for i, candle in enumerate(processed_data[-5:]):
        timestamp = datetime.fromtimestamp(int(candle[0]) / 1000)
        print(f"   {len(processed_data)-4+i}. {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Open: {candle[1]}, High: {candle[2]}, Low: {candle[3]}, Close: {candle[4]}")
    
    print()
    
    # Estadísticas básicas
    print("📈 ESTADÍSTICAS BÁSICAS:")
    if processed_data:
        prices = [float(candle[4]) for candle in processed_data]  # Precios de cierre
        volumes = [float(candle[5]) for candle in processed_data]  # Volúmenes
        
        print(f"   Precio más alto: ${max(prices):,.2f}")
        print(f"   Precio más bajo: ${min(prices):,.2f}")
        print(f"   Rango de precios: ${max(prices) - min(prices):,.2f}")
        print(f"   Volumen total: {sum(volumes):,.2f} BTC")
        print(f"   Volumen promedio por vela: {sum(volumes)/len(volumes):,.2f} BTC")
    
    print()
    print("=" * 60)

def list_debug_files():
    """Lista todos los archivos de debug disponibles"""
    debug_files = [f for f in os.listdir('.') if f.startswith('debug_api_') and f.endswith('.json')]
    
    if not debug_files:
        print("No se encontraron archivos de debug.")
        return []
    
    print("📁 ARCHIVOS DE DEBUG DISPONIBLES:")
    for i, filename in enumerate(sorted(debug_files, reverse=True)):
        file_size = os.path.getsize(filename)
        print(f"   {i+1}. {filename} ({file_size:,} bytes)")
    
    return debug_files

def main():
    """Función principal"""
    print("🔍 ANALIZADOR DE ARCHIVOS DE DEBUG - API OKX\n")
    
    # Listar archivos disponibles
    debug_files = list_debug_files()
    
    if not debug_files:
        return
    
    print()
    
    # Analizar el archivo más reciente por defecto
    latest_file = debug_files[0]
    print(f"Analizando el archivo más reciente: {latest_file}")
    print()
    
    analyze_debug_file(latest_file)
    
    # Preguntar si quiere analizar otro archivo
    if len(debug_files) > 1:
        print("\n¿Deseas analizar otro archivo? (s/n): ", end="")
        response = input().lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            print("\nArchivos disponibles:")
            for i, filename in enumerate(debug_files):
                print(f"   {i+1}. {filename}")
            
            try:
                choice = int(input("\nSelecciona el número del archivo: ")) - 1
                if 0 <= choice < len(debug_files):
                    print()
                    analyze_debug_file(debug_files[choice])
                else:
                    print("Selección inválida.")
            except ValueError:
                print("Entrada inválida.")

if __name__ == "__main__":
    main() 