#!/usr/bin/env python3
"""
API Server seguro para n8n - Genera gráficos de velas de OKX
Con autenticación por API key para mayor seguridad
"""

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import time
import hmac
import base64
import hashlib
from datetime import datetime, timedelta
import os
import json
import io
import base64
import re
from functools import wraps
from env_config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE

app = Flask(__name__)
CORS(app)  # Permitir CORS para n8n

# Configuración de seguridad
API_KEYS = {
    "n8n-secure-key-2025": "n8n_user",
    "admin-secure-key-2025": "admin_user"
}

def require_api_key(f):
    """Decorador para requerir API key en los endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                "error": "API key requerida",
                "message": "Incluye 'X-API-Key' en los headers o 'api_key' como parámetro"
            }), 401
        
        if api_key not in API_KEYS:
            return jsonify({
                "error": "API key inválida",
                "message": "La API key proporcionada no es válida"
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def get_timestamp():
    """Genera timestamp en formato ISO8601 UTC"""
    return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())

def generate_signature(timestamp, method, request_path, body=''):
    """Genera firma HMAC SHA256 para autenticación"""
    message = f"{timestamp}{method}{request_path}{body}"
    mac = hmac.new(OKX_API_SECRET.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

def get_headers(method, request_path, body=''):
    """Genera headers con autenticación para la API"""
    timestamp = get_timestamp()
    signature = generate_signature(timestamp, method, request_path, body)
    return {
        'OK-ACCESS-KEY': OKX_API_KEY,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': OKX_PASSPHRASE,
        'Content-Type': 'application/json'
    }

def get_candlestick_data(symbol='BTC-USDT', bar='5m', candles_count=81):
    """Obtiene datos de velas desde la API de OKX"""
    # Obtener más velas de las necesarias para asegurar que tenemos suficientes
    limit = max(candles_count + 20, 100)
    url_path = f'/api/v5/market/candles?instId={symbol}&bar={bar}&limit={limit}'
    url = 'https://www.okx.com' + url_path
    
    headers = get_headers('GET', url_path)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']:
            # Tomar solo las últimas N velas
            if len(data['data']) >= candles_count:
                filtered_data = data['data'][:candles_count]
            else:
                filtered_data = data['data']
            return filtered_data, data['data']
        else:
            return [], []
    else:
        return [], []

def clean_numeric_value(value):
    """Limpia y convierte un valor numérico de manera segura"""
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # Si es una cadena muy larga, puede contener múltiples números concatenados
        if len(value) > 20:
            # Buscar el primer número válido
            numbers = re.findall(r'\d+\.?\d*', value)
            if numbers:
                try:
                    return float(numbers[0])
                except (ValueError, IndexError):
                    return None
        else:
            # Intentar convertir directamente
            try:
                return float(value)
            except ValueError:
                return None
    
    return None

def create_dataframe(data):
    """Convierte los datos de la API a DataFrame de manera segura"""
    if not data:
        return pd.DataFrame()
    
    # Crear DataFrame con los datos
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close',
        'volume', 'volume_currency', 'volume_currency_2', 'trades'
    ])
    
    # Convertir timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    
    # Convertir precios de manera segura
    numeric_columns = ['open', 'high', 'low', 'close']
    for col in numeric_columns:
        df[col] = df[col].apply(clean_numeric_value)
    
    # Filtrar filas con datos inválidos
    df = df.dropna(subset=['open', 'high', 'low', 'close'])
    
    # Ordenar por timestamp
    df = df.sort_values('timestamp')
    
    return df

def create_candlestick_chart(df, symbol, candles_count):
    """Crea gráfico de velas con matplotlib y retorna como imagen"""
    if df.empty:
        return None
    
    # Configurar matplotlib para no mostrar la ventana
    plt.switch_backend('Agg')
    
    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Preparar datos para candlestick
    df_plot = df.copy()
    df_plot['date_num'] = mdates.date2num(df_plot['timestamp'])
    
    # Crear datos OHLC
    ohlc_data = df_plot[['date_num', 'open', 'high', 'low', 'close']].values
    
    # Crear gráfico de velas
    candlestick_ohlc(ax, ohlc_data, width=0.6, colorup='green', colordown='red', alpha=0.8)
    
    # Configurar formato de fecha
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
    
    # Rotar etiquetas de fecha
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Configurar título y etiquetas
    ax.set_title(f'Candlestick {symbol} - Últimas {candles_count} velas', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hora', fontsize=12)
    ax.set_ylabel('Precio (USDT)', fontsize=12)
    
    # Configurar grid
    ax.grid(True, alpha=0.3)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Convertir a bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    img_bytes = img_buffer.getvalue()
    
    # Cerrar figura para liberar memoria
    plt.close(fig)
    
    return img_bytes

def save_debug_info(api_response, processed_data, symbol, candles_count):
    """Guarda información de debug"""
    debug_filename = f"debug_api_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    debug_info = {
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol,
        "candles_count": candles_count,
        "api_response": {
            "total_candles_received": len(api_response) if api_response else 0,
            "raw_data": api_response
        },
        "processed_data": {
            "candles_used_for_chart": len(processed_data) if processed_data else 0,
            "data": processed_data
        }
    }
    
    try:
        with open(debug_filename, 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False, default=str)
        return debug_filename
    except Exception as e:
        print(f"Error guardando debug: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "OKX Candlestick Chart API for n8n (Secure)",
        "version": "2.0.0",
        "security": "API Key authentication required",
        "endpoints": {
            "health": "GET /health (no auth required)",
            "generate_chart": "POST /generate-chart (auth required)",
            "generate_chart_image": "POST /generate-chart-image (auth required)",
            "chart_info": "GET /chart-info (auth required)"
        }
    })

@app.route('/generate-chart', methods=['POST'])
@require_api_key
def generate_chart():
    """Endpoint principal para generar el gráfico de velas - optimizado para n8n"""
    try:
        # Obtener parámetros del request
        data = request.get_json() or {}
        
        symbol = data.get('symbol', 'BTC-USDT')
        bar = data.get('bar', '5m')
        candles_count = data.get('candles_count', 81)
        
        # Validar parámetros
        if candles_count <= 0 or candles_count > 300:
            return jsonify({
                "error": "candles_count debe estar entre 1 y 300"
            }), 400
        
        # Obtener datos de la API
        new_data, raw_api_data = get_candlestick_data(symbol, bar, candles_count)
        
        if not new_data:
            return jsonify({
                "error": "No se pudieron obtener datos de la API"
            }), 500
        
        # Procesar datos
        df = create_dataframe(new_data)
        
        if df.empty:
            return jsonify({
                "error": "No hay datos válidos para generar el gráfico"
            }), 500
        
        # Generar gráfico
        img_bytes = create_candlestick_chart(df, symbol, candles_count)
        
        if img_bytes is None:
            return jsonify({
                "error": "Error al generar el gráfico"
            }), 500
        
        # Guardar información de debug
        debug_file = save_debug_info(raw_api_data, new_data, symbol, candles_count)
        
        # Convertir imagen a base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        # Preparar respuesta optimizada para n8n
        response_data = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "bar": bar,
            "candles_count": len(df),
            "image_base64": img_base64,
            "debug_file": debug_file,
            "chart_info": {
                "start_time": df['timestamp'].min().isoformat(),
                "end_time": df['timestamp'].max().isoformat(),
                "price_range": {
                    "min": float(df['low'].min()),
                    "max": float(df['high'].max())
                },
                "current_price": float(df['close'].iloc[-1]),
                "price_change": float(df['close'].iloc[-1] - df['open'].iloc[0]),
                "total_volume": float(df['volume'].sum()) if 'volume' in df.columns else 0.0
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

@app.route('/generate-chart-image', methods=['POST'])
@require_api_key
def generate_chart_image():
    """Endpoint que retorna directamente la imagen (sin base64)"""
    try:
        # Obtener parámetros del request
        data = request.get_json() or {}
        
        symbol = data.get('symbol', 'BTC-USDT')
        bar = data.get('bar', '5m')
        candles_count = data.get('candles_count', 81)
        
        # Validar parámetros
        if candles_count <= 0 or candles_count > 300:
            return jsonify({
                "error": "candles_count debe estar entre 1 y 300"
            }), 400
        
        # Obtener datos de la API
        new_data, raw_api_data = get_candlestick_data(symbol, bar, candles_count)
        
        if not new_data:
            return jsonify({
                "error": "No se pudieron obtener datos de la API"
            }), 500
        
        # Procesar datos
        df = create_dataframe(new_data)
        
        if df.empty:
            return jsonify({
                "error": "No hay datos válidos para generar el gráfico"
            }), 500
        
        # Generar gráfico
        img_bytes = create_candlestick_chart(df, symbol, candles_count)
        
        if img_bytes is None:
            return jsonify({
                "error": "Error al generar el gráfico"
            }), 500
        
        # Guardar información de debug
        debug_file = save_debug_info(raw_api_data, new_data, symbol, candles_count)
        
        # Retornar imagen directamente
        return send_file(
            io.BytesIO(img_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name=f'candlestick_{symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        )
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

@app.route('/chart-info', methods=['GET'])
@require_api_key
def get_chart_info():
    """Endpoint para obtener información sobre el gráfico"""
    try:
        # Obtener parámetros de query
        symbol = request.args.get('symbol', 'BTC-USDT')
        bar = request.args.get('bar', '5m')
        candles_count = int(request.args.get('candles_count', 81))
        
        # Obtener datos de la API
        new_data, raw_api_data = get_candlestick_data(symbol, bar, candles_count)
        
        if not new_data:
            return jsonify({
                "error": "No se pudieron obtener datos de la API"
            }), 500
        
        # Procesar datos
        df = create_dataframe(new_data)
        
        if df.empty:
            return jsonify({
                "error": "No hay datos válidos"
            }), 500
        
        # Preparar información
        info = {
            "symbol": symbol,
            "bar": bar,
            "candles_count": len(df),
            "timestamp": datetime.now().isoformat(),
            "time_range": {
                "start": df['timestamp'].min().isoformat(),
                "end": df['timestamp'].max().isoformat()
            },
            "price_stats": {
                "current_price": float(df['close'].iloc[-1]),
                "min_price": float(df['low'].min()),
                "max_price": float(df['high'].max()),
                "price_change": float(df['close'].iloc[-1] - df['open'].iloc[0])
            },
            "volume_stats": {
                "total_volume": float(df['volume'].sum()) if 'volume' in df.columns else 0.0,
                "avg_volume": float(df['volume'].mean()) if 'volume' in df.columns else 0.0
            },
            "latest_candles": []
        }
        
        # Agregar las últimas 5 velas
        for _, row in df.tail(5).iterrows():
            info["latest_candles"].append({
                "timestamp": row['timestamp'].isoformat(),
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close']),
                "volume": float(row['volume']) if 'volume' in df.columns else 0.0
            })
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

@app.route('/api-keys', methods=['GET'])
def get_api_keys_info():
    """Endpoint para obtener información sobre las API keys (solo para desarrollo)"""
    return jsonify({
        "message": "API Keys disponibles",
        "keys": list(API_KEYS.keys()),
        "note": "Usa 'X-API-Key' header o 'api_key' parameter"
    })

if __name__ == '__main__':
    print("🔐 Iniciando API Server Seguro para n8n - Gráficos de Velas OKX")
    print("=" * 70)
    print("📊 Endpoints disponibles:")
    print("   POST /generate-chart - Genera gráfico y retorna JSON con imagen en base64")
    print("   POST /generate-chart-image - Genera gráfico y retorna imagen directamente")
    print("   GET  /chart-info - Obtiene información del gráfico")
    print("   GET  /health - Verificación de salud del servidor")
    print("   GET  /api-keys - Información sobre API keys")
    print()
    print("🔗 El servidor estará disponible en: http://0.0.0.0:5003")
    print("📝 Para n8n, usa: http://localhost:5003/generate-chart-image")
    print()
    print("🔑 API Keys disponibles:")
    for key, user in API_KEYS.items():
        print(f"   {key} ({user})")
    print()
    print("📋 Ejemplo de payload para n8n:")
    print("""
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
""")
    print("🔐 Headers requeridos:")
    print("   X-API-Key: n8n-secure-key-2025")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5003, debug=True) 