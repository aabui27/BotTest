from flask import Flask, render_template_string, jsonify, request
import requests
import pandas as pd
import plotly.graph_objects as go
import time
import hmac
import base64
import hashlib
from datetime import datetime
import os
import json

app = Flask(__name__)

# Obtener credenciales desde variables de entorno
OKX_API_KEY = os.environ.get('OKX_API_KEY')
OKX_API_SECRET = os.environ.get('OKX_API_SECRET')
OKX_PASSPHRASE = os.environ.get('OKX_PASSPHRASE')

def get_timestamp():
    """Genera timestamp en formato ISO8601 UTC"""
    return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())

def generate_signature(timestamp, method, request_path, body=''):
    """Genera firma HMAC SHA256 para autenticación"""
    if not OKX_API_SECRET:
        return ""
    message = f"{timestamp}{method}{request_path}{body}"
    mac = hmac.new(OKX_API_SECRET.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

def get_headers(method, request_path, body=''):
    """Genera headers con autenticación para la API"""
    timestamp = get_timestamp()
    signature = generate_signature(timestamp, method, request_path, body)
    return {
        'OK-ACCESS-KEY': OKX_API_KEY or '',
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': OKX_PASSPHRASE or '',
        'Content-Type': 'application/json'
    }

def get_candlestick_data(symbol='BTC-USDT', bar='5m'):
    """Obtiene datos de velas desde la API de OKX - últimas 81 velas"""
    try:
        # Verificar que las credenciales estén configuradas
        if not all([OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE]):
            return []
        
        # Obtener las últimas 81 velas (necesitamos más para asegurar que tenemos suficientes)
        url_path = f'/api/v5/market/candles?instId={symbol}&bar={bar}&limit=100'
        url = 'https://www.okx.com' + url_path
        
        headers = get_headers('GET', url_path)
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                # Tomar solo las últimas 81 velas
                candles_to_show = 81
                if len(data['data']) >= candles_to_show:
                    filtered_data = data['data'][:candles_to_show]  # Las últimas 81 velas
                else:
                    filtered_data = data['data']  # Si hay menos de 81, tomar todas
                return filtered_data
        return []
    except Exception as e:
        print(f"Error getting candlestick data: {e}")
        return []

def create_dataframe(data):
    """Convierte los datos de la API a DataFrame"""
    if not data:
        return pd.DataFrame()
    
    try:
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close',
            'volume', 'volume_currency', 'volume_currency_2', 'trades'
        ])
        
        # Convertir tipos de datos
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
        df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
        
        # Ordenar por timestamp (más reciente primero en la API, pero queremos cronológico)
        df = df.sort_values('timestamp')
        
        return df
    except Exception as e:
        print(f"Error creating dataframe: {e}")
        return pd.DataFrame()

def create_candlestick_chart(df, symbol):
    """Crea gráfico de velas con Plotly"""
    if df.empty:
        return None
    
    try:
        fig = go.Figure(data=[go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )])
        
        fig.update_layout(
            title=f"Candlestick 5m - {symbol} - Últimas 81 velas",
            xaxis_title="Hora",
            yaxis_title="Precio (USDT)",
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        return fig
    except Exception as e:
        print(f"Error creating chart: {e}")
        return None

# HTML template para la página web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OKX Candlestick Analyzer</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .controls {
            text-align: center;
            margin-bottom: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .controls select, .controls button {
            padding: 10px 15px;
            margin: 0 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .controls button {
            background: #007bff;
            color: white;
            cursor: pointer;
            border: none;
        }
        .controls button:hover {
            background: #0056b3;
        }
        .chart-container {
            margin-top: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .error {
            text-align: center;
            padding: 40px;
            color: #dc3545;
            background: #f8d7da;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 OKX Candlestick Analyzer</h1>
        
        <div class="controls">
            <select id="symbol">
                <option value="BTC-USDT">BTC-USDT</option>
                <option value="ETH-USDT">ETH-USDT</option>
                <option value="ADA-USDT">ADA-USDT</option>
                <option value="DOT-USDT">DOT-USDT</option>
                <option value="LINK-USDT">LINK-USDT</option>
            </select>
            <select id="interval">
                <option value="5m">5 minutos</option>
                <option value="15m">15 minutos</option>
                <option value="1H">1 hora</option>
                <option value="4H">4 horas</option>
            </select>
            <button onclick="loadData()">🔄 Actualizar Datos</button>
        </div>
        
        <div id="stats" class="stats" style="display: none;">
            <div class="stat-card">
                <div class="stat-value" id="price-high">-</div>
                <div class="stat-label">Precio Más Alto</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="price-low">-</div>
                <div class="stat-label">Precio Más Bajo</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="price-change">-</div>
                <div class="stat-label">Cambio %</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="volume-total">-</div>
                <div class="stat-label">Volumen Total</div>
            </div>
        </div>
        
        <div id="loading" class="loading" style="display: none;">
            <h3>🔄 Cargando datos...</h3>
        </div>
        
        <div id="error" class="error" style="display: none;">
            <h3>❌ Error de configuración</h3>
            <p>Las credenciales de la API no están configuradas correctamente.</p>
            <p>Verifica las variables de entorno en Railway.</p>
        </div>
        
        <div id="chart-container" class="chart-container"></div>
    </div>

    <script>
        function loadData() {
            const symbol = document.getElementById('symbol').value;
            const interval = document.getElementById('interval').value;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('chart-container').innerHTML = '';
            document.getElementById('stats').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            fetch(`/api/candles?symbol=${symbol}&interval=${interval}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    
                    if (data.success) {
                        // Mostrar estadísticas
                        document.getElementById('price-high').textContent = '$' + data.stats.high.toLocaleString();
                        document.getElementById('price-low').textContent = '$' + data.stats.low.toLocaleString();
                        document.getElementById('price-change').textContent = data.stats.change + '%';
                        document.getElementById('volume-total').textContent = data.stats.volume.toLocaleString();
                        document.getElementById('stats').style.display = 'grid';
                        
                        // Mostrar gráfico
                        Plotly.newPlot('chart-container', data.chart.data, data.chart.layout);
                    } else {
                        if (data.error.includes('credenciales') || data.error.includes('configuradas')) {
                            document.getElementById('error').style.display = 'block';
                        } else {
                            document.getElementById('chart-container').innerHTML = 
                                '<div style="text-align: center; color: red; padding: 40px;"><h3>❌ Error al cargar datos</h3><p>' + data.error + '</p></div>';
                        }
                    }
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('chart-container').innerHTML = 
                        '<div style="text-align: center; color: red; padding: 40px;"><h3>❌ Error de conexión</h3><p>' + error.message + '</p></div>';
                });
        }
        
        // Cargar datos al iniciar la página
        window.onload = function() {
            loadData();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/candles')
def api_candles():
    """API endpoint para obtener datos de velas"""
    try:
        # Verificar que las credenciales estén configuradas
        if not all([OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE]):
            return jsonify({
                'success': False,
                'error': 'Las credenciales de la API no están configuradas correctamente'
            })
        
        symbol = request.args.get('symbol', 'BTC-USDT')
        interval = request.args.get('interval', '5m')
        
        # Obtener datos
        data = get_candlestick_data(symbol, interval)
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se pudieron obtener datos de la API'
            })
        
        # Crear DataFrame
        df = create_dataframe(data)
        
        if df.empty:
            return jsonify({
                'success': False,
                'error': 'No hay datos disponibles'
            })
        
        # Crear gráfico
        fig = create_candlestick_chart(df, symbol)
        
        if fig is None:
            return jsonify({
                'success': False,
                'error': 'Error al crear el gráfico'
            })
        
        # Calcular estadísticas
        prices = df['close'].values
        volumes = df['volume'].values
        
        stats = {
            'high': float(prices.max()),
            'low': float(prices.min()),
            'change': round(((prices[-1] - prices[0]) / prices[0]) * 100, 2),
            'volume': float(volumes.sum())
        }
        
        # Convertir gráfico a JSON
        chart_json = json.loads(fig.to_json())
        
        return jsonify({
            'success': True,
            'chart': chart_json,
            'stats': stats,
            'candles_count': len(df)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/ping')
def ping():
    """Endpoint simple para healthcheck"""
    return "pong"

@app.route('/health')
def health():
    """Endpoint de salud para Railway"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'OKX Candlestick Analyzer',
            'credentials_configured': all([OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE]),
            'python_version': '3.11.5',
            'port': os.environ.get('PORT', '8080')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/test')
def test():
    """Endpoint de prueba simple"""
    return jsonify({
        'message': 'OKX Candlestick Analyzer is running!',
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    })

@app.route('/debug')
def debug():
    """Endpoint de debug con información del sistema"""
    return jsonify({
        'status': 'debug',
        'timestamp': datetime.now().isoformat(),
        'port': os.environ.get('PORT', '8080'),
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'production'),
        'python_version': '3.11.5',
        'flask_version': '2.3.3',
        'credentials_configured': all([OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE])
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False) 