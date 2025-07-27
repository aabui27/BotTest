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
from env_config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE

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

def save_api_debug_info(api_response, processed_data, symbol, date_str):
    """Guarda información de debug de la API y datos procesados"""
    debug_filename = f"debug_api_{symbol}_{date_str}_{datetime.now().strftime('%H%M%S')}.json"
    
    debug_info = {
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol,
        "api_request": {
            "url": "https://www.okx.com/api/v5/market/candles",
            "parameters": {
                "instId": symbol,
                "bar": "5m",
                "limit": 100
            }
        },
        "api_response": {
            "status_code": 200,
            "raw_data": api_response,
            "total_candles_received": len(api_response) if api_response else 0
        },
        "processed_data": {
            "candles_used_for_chart": len(processed_data) if processed_data else 0,
            "data": processed_data
        },
        "dataframe_info": {
            "columns": ["timestamp", "open", "high", "low", "close", "volume", "volume_currency", "volume_currency_2", "trades"],
            "description": "Datos procesados para el gráfico de velas"
        }
    }
    
    try:
        with open(debug_filename, 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False, default=str)
        print(f"Información de debug guardada en: {debug_filename}")
        return debug_filename
    except Exception as e:
        print(f"Error guardando información de debug: {e}")
        return None

def get_candlestick_data(symbol='BTC-USDT', bar='5m', start_time=None, end_time=None):
    """Obtiene datos de velas desde la API de OKX - últimas 81 velas"""
    # Obtener las últimas 81 velas (necesitamos más para asegurar que tenemos suficientes)
    url_path = f'/api/v5/market/candles?instId={symbol}&bar={bar}&limit=100'
    url = 'https://www.okx.com' + url_path
    
    print(f"Consultando API: {url}")
    
    headers = get_headers('GET', url_path)
    response = requests.get(url, headers=headers)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Velas totales obtenidas de la API: {len(data['data']) if 'data' in data else 0}")
        
        if 'data' in data and data['data']:
            # Tomar solo las últimas 81 velas
            candles_to_show = 81
            if len(data['data']) >= candles_to_show:
                filtered_data = data['data'][:candles_to_show]  # Las últimas 81 velas
            else:
                filtered_data = data['data']  # Si hay menos de 81, tomar todas
            
            print(f"Velas que se mostrarán: {len(filtered_data)}")
            return filtered_data, data['data']  # Retornamos tanto los datos filtrados como los completos
        else:
            print("No se encontraron datos en la respuesta")
            return [], []
    else:
        print(f"Error en la API: {response.status_code} - {response.text}")
        return [], []

def get_current_day_range():
    """Esta función ya no se usa, pero la mantenemos por compatibilidad"""
    today = datetime.now().date()
    start_time = datetime.combine(today, datetime.min.time())  # 00:00:00
    end_time = datetime.combine(today, datetime.max.time())    # 23:59:59
    
    # Convertir a timestamp en milisegundos
    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(end_time.timestamp() * 1000)
    
    return start_timestamp, end_timestamp

def create_dataframe(data):
    """Convierte los datos de la API a DataFrame"""
    if not data:
        return pd.DataFrame()
    
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

def load_existing_data(symbol, date_str):
    """Carga datos existentes del día desde archivo"""
    filename = f"candles_{symbol}_{date_str}.json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            df = create_dataframe(data)
            # Tomar solo las últimas 81 velas de los datos existentes
            if len(df) > 81:
                df = df.tail(81)
            return df
        except Exception as e:
            print(f"Error cargando datos existentes: {e}")
    return pd.DataFrame()

def save_data(df, symbol, date_str):
    """Guarda los datos del día en archivo"""
    if not df.empty:
        filename = f"candles_{symbol}_{date_str}.json"
        try:
            # Convertir DataFrame a formato JSON
            data_to_save = []
            for _, row in df.iterrows():
                data_to_save.append([
                    str(int(row['timestamp'].timestamp() * 1000)),
                    str(row['open']),
                    str(row['high']),
                    str(row['low']),
                    str(row['close']),
                    str(row['volume']),
                    str(row['volume_currency']),
                    str(row['volume_currency_2']),
                    str(row['trades'])
                ])
            
            with open(filename, 'w') as f:
                json.dump(data_to_save, f)
            print(f"Datos guardados en {filename}")
        except Exception as e:
            print(f"Error guardando datos: {e}")

def merge_and_deduplicate_data(existing_df, new_df):
    """Combina datos existentes con nuevos y elimina duplicados, manteniendo solo las últimas 81 velas"""
    if existing_df.empty:
        return new_df
    if new_df.empty:
        return existing_df
    
    # Combinar DataFrames
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    # Eliminar duplicados basados en timestamp
    combined_df = combined_df.drop_duplicates(subset=['timestamp'], keep='last')
    
    # Ordenar por timestamp
    combined_df = combined_df.sort_values('timestamp')
    
    # Tomar solo las últimas 81 velas
    if len(combined_df) > 81:
        combined_df = combined_df.tail(81)
    
    return combined_df

def create_candlestick_chart(df, symbol, date_str):
    """Crea gráfico de velas con Plotly"""
    if df.empty:
        print("No hay datos para mostrar")
        return None
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title=f"Candlestick 5m - {symbol} - Últimas 81 velas ({date_str})",
        xaxis_title="Hora",
        yaxis_title="Precio (USDT)",
        xaxis_rangeslider_visible=False
    )
    
    return fig

def main():
    """Función principal"""
    # Configuración
    symbol = 'BTC-USDT'
    bar = '5m'
    
    # Obtener fecha actual
    current_date = datetime.now().date()
    date_str = current_date.strftime('%Y-%m-%d')
    
    print(f"Obteniendo las últimas 81 velas del día: {date_str}")
    
    # Cargar datos existentes del día
    existing_df = load_existing_data(symbol, date_str)
    print(f"Velas existentes cargadas: {len(existing_df)}")
    
    # Obtener datos (últimas 81 velas)
    new_data, raw_api_data = get_candlestick_data(symbol, bar)
    
    if new_data:
        new_df = create_dataframe(new_data)
        print(f"Nuevas velas obtenidas: {len(new_df)}")
        
        # Combinar datos existentes con nuevos
        combined_df = merge_and_deduplicate_data(existing_df, new_df)
        print(f"Total de velas después de combinar: {len(combined_df)}")
        
        # Guardar datos actualizados
        save_data(combined_df, symbol, date_str)
        
        # Guardar información de debug de la API
        debug_file = save_api_debug_info(raw_api_data, new_data, symbol, date_str)
        
        # Crear y mostrar gráfico
        fig = create_candlestick_chart(combined_df, symbol, date_str)
        if fig:
            fig.show()
    else:
        print("No se pudieron obtener nuevos datos")
        if not existing_df.empty:
            fig = create_candlestick_chart(existing_df, symbol, date_str)
            if fig:
                fig.show()

if __name__ == "__main__":
    main()
