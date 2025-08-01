# OKX Candlestick Analyzer - Integración con n8n

## 🚀 Endpoints para n8n

### 1. Endpoint Principal para n8n (Datos JSON)
**URL:** `https://tu-app.railway.app/api/n8n`

**Método:** GET

**Parámetros opcionales:**
- `symbol`: Par de trading (default: BTC-USDT)
- `interval`: Intervalo de tiempo (default: 5m)

**Ejemplo de uso:**
```
https://tu-app.railway.app/api/n8n?symbol=BTC-USDT&interval=5m
```

**Respuesta JSON:**
```json
{
    "success": true,
    "timestamp": "2025-07-31T22:14:54.098834",
    "symbol": "BTC-USDT",
    "interval": "5m",
    "current_price": 114671.1,
    "open_price": 114941.8,
    "high_price": 114945.3,
    "low_price": 114575.6,
    "volume": 75.01766958,
    "change": -270.7,
    "change_percent": -0.24,
    "trend": "down",
    "candles_count": 81,
    "last_update": "0"
}
```

### 2. Endpoint de Imagen para n8n (PNG)
**URL:** `https://tu-app.railway.app/api/n8n-image`

**Método:** GET

**Parámetros opcionales:**
- `symbol`: Par de trading (default: BTC-USDT)
- `interval`: Intervalo de tiempo (default: 5m)

**Ejemplo de uso:**
```
https://tu-app.railway.app/api/n8n-image?symbol=BTC-USDT&interval=5m
```

**Respuesta:** Imagen PNG del gráfico de velas

**Características:**
- ✅ No requiere Chrome/Kaleido
- ✅ Generado con matplotlib
- ✅ Fondo negro con velas verdes/rojas
- ✅ Tamaño: 12x8 pulgadas, 100 DPI
- ✅ Formato: PNG

### 2. Endpoint de Datos Completos
**URL:** `https://tu-app.railway.app/api/candles`

**Método:** GET

**Respuesta:** Datos completos de velas con gráfico Plotly

### 3. Endpoint de Estado
**URL:** `https://tu-app.railway.app/health`

**Método:** GET

**Respuesta:** Estado del servicio y configuración

## 🔧 Configuración en n8n

### 1. HTTP Request Node
- **Método:** GET
- **URL:** `https://tu-app.railway.app/api/n8n`
- **Parámetros:** 
  - `symbol`: BTC-USDT
  - `interval`: 5m

### 2. Campos disponibles en la respuesta
- `current_price`: Precio actual
- `change`: Cambio en valor absoluto
- `change_percent`: Cambio en porcentaje
- `trend`: "up" o "down"
- `volume`: Volumen de trading
- `high_price`: Precio máximo
- `low_price`: Precio mínimo

## 🚨 Solución al Error de Chrome/Kaleido

Si recibes el error:
```
Kaleido requires Google Chrome to be installed
```

**Solución:** Usa el endpoint `/api/n8n` en lugar de `/api/chart-image`

### Endpoints disponibles según el entorno:

| Endpoint | Local | Railway | Descripción |
|----------|-------|---------|-------------|
| `/api/n8n` | ✅ | ✅ | Datos JSON para n8n |
| `/api/n8n-image` | ✅ | ✅ | Imagen PNG para n8n (matplotlib) |
| `/api/candles` | ✅ | ✅ | Datos completos |
| `/api/chart-image` | ✅ | ❌ | Imagen PNG (requiere Chrome) |
| `/health` | ✅ | ✅ | Estado del servicio |

## 📊 Ejemplo de Workflow n8n

1. **HTTP Request Node**
   - URL: `https://tu-app.railway.app/api/n8n`
   - Método: GET

2. **IF Node** (Opcional)
   - Condición: `{{ $json.trend === "up" }}`
   - Acción: Enviar notificación

3. **Set Node** (Opcional)
   - Campos:
     - `price`: `{{ $json.current_price }}`
     - `change`: `{{ $json.change_percent }}`
     - `volume`: `{{ $json.volume }}`

## 🔐 Variables de Entorno

Asegúrate de que estas variables estén configuradas en Railway:
- `OKX_API_KEY`
- `OKX_API_SECRET`
- `OKX_PASSPHRASE`

## 📝 Notas Importantes

- El endpoint `/api/n8n` está optimizado para n8n y no requiere Chrome
- Los datos se obtienen en tiempo real de la API de OKX
- El intervalo por defecto es 5 minutos
- La respuesta incluye 81 velas de datos históricos 