#!/usr/bin/env python3
"""
API Server para generar gráficos de velas desde n8n
"""

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import requests
import pandas as pd
import plotly.graph_objects as go
import time
import hmac
import base64
import hashlib
from datetime import datetime, timedelta
import os
import json
import io
import base64
from env_config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE

app = Flask(__name__)
CORS(app)  # Permitir CORS para n8n

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

def create_dataframe(data):
    """Convierte los datos de la API a DataFrame"""
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close',
        'volume', 'volume_currency', 'volume_currency_2', 'trades'
    ])
    
    # Convertir tipos de datos de manera más segura
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    
    # Convertir precios de manera segura
    for col in ['open', 'high', 'low', 'close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filtrar filas con datos inválidos
    df = df.dropna(subset=['open', 'high', 'low', 'close'])
    
    # Ordenar por timestamp
    df = df.sort_values('timestamp')
    
    return df

def create_candlestick_chart(df, symbol, candles_count):
    """Crea gráfico de velas con Plotly y retorna como imagen"""
    if df.empty:
        return None
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title=f"Candlestick {symbol} - Últimas {candles_count} velas",
        xaxis_title="Hora",
        yaxis_title="Precio (USDT)",
        xaxis_rangeslider_visible=False,
        width=1200,
        height=600,
        template="plotly_white"
    )
    
    # Convertir a imagen usando orca (alternativa a kaleido)
    try:
        # Intentar con kaleido primero
        img_bytes = fig.to_image(format="png", engine="kaleido")
    except Exception as e:
        try:
            # Si falla kaleido, usar orca
            img_bytes = fig.to_image(format="png", engine="orca")
        except Exception as e2:
            # Si ambos fallan, usar el método de escritura HTML y convertir
            print(f"Error con kaleido: {e}")
            print(f"Error con orca: {e2}")
            print("Usando método alternativo...")
            
            # Crear un archivo HTML temporal y convertirlo
            import tempfile
            import subprocess
            
            # Guardar como HTML
            html_content = fig.to_html(include_plotlyjs='cdn')
            
            # Usar wkhtmltopdf o similar para convertir HTML a imagen
            # Por ahora, retornamos None y manejamos el error
            return None
    
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
        "service": "OKX Candlestick Chart API"
    })

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    """Endpoint principal para generar el gráfico de velas"""
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
        
        # Preparar respuesta
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
                "total_volume": float(df['volume'].sum())
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

@app.route('/generate-chart-image', methods=['POST'])
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
def get_chart_info():
    """Endpoint para obtener información sobre el último gráfico generado"""
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
                "total_volume": float(df['volume'].sum()),
                "avg_volume": float(df['volume'].mean())
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
                "volume": float(row['volume'])
            })
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor API para gráficos de velas...")
    print("📊 Endpoints disponibles:")
    print("   POST /generate-chart - Genera gráfico y retorna JSON con imagen en base64")
    print("   POST /generate-chart-image - Genera gráfico y retorna imagen directamente")
    print("   GET  /chart-info - Obtiene información del gráfico")
    print("   GET  /health - Verificación de salud del servidor")
    print()
    print("🔗 El servidor estará disponible en: http://localhost:5001")
    print("📝 Para n8n, usa: http://localhost:5001/generate-chart")
    print()
    
    app.run(host='0.0.0.0', port=5001, debug=True) 