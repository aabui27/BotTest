from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal simple"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OKX Candlestick Analyzer</title>
    </head>
    <body>
        <h1>🚀 OKX Candlestick Analyzer</h1>
        <p>La aplicación está funcionando correctamente!</p>
        <p>Timestamp: {}</p>
        <p>Port: {}</p>
        <p>Environment: {}</p>
    </body>
    </html>
    """.format(datetime.now().isoformat(), os.environ.get('PORT', '8080'), os.environ.get('RAILWAY_ENVIRONMENT', 'production'))

@app.route('/ping')
def ping():
    """Endpoint simple para healthcheck"""
    return "pong"

@app.route('/health')
def health():
    """Endpoint de salud"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'port': os.environ.get('PORT', '8080'),
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'production')
    })

@app.route('/test')
def test():
    """Endpoint de prueba"""
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
        'all_env_vars': dict(os.environ)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False) 