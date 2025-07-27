# 🔐 API Segura para Gráficos de Velas OKX - n8n Integration

## 📋 Descripción

API REST segura para generar gráficos de velas de criptomonedas desde OKX, optimizada para integración con n8n. Incluye autenticación por API key para mayor seguridad.

## 🚀 Características

- ✅ **Autenticación por API Key** - Protección contra acceso no autorizado
- ✅ **Generación de gráficos de velas** - Usando Matplotlib y mplfinance
- ✅ **Múltiples endpoints** - JSON con base64, imagen directa, información
- ✅ **Optimizado para n8n** - Respuestas compatibles con workflows
- ✅ **Debug automático** - Archivos de debug para troubleshooting
- ✅ **CORS habilitado** - Compatible con aplicaciones web
- ✅ **Validación de datos** - Limpieza y validación robusta de datos

## 🔧 Instalación

### 1. Dependencias

```bash
pip install flask flask-cors requests pandas matplotlib mplfinance
```

### 2. Configuración de API Keys de OKX

Crear archivo `env_config.py`:

```python
# Credenciales de OKX API
OKX_API_KEY = "tu_api_key_de_okx"
OKX_API_SECRET = "tu_api_secret_de_okx"
OKX_PASSPHRASE = "tu_passphrase_de_okx"
```

### 3. Ejecutar el servidor

```bash
python n8n_api_server_secure.py
```

## 🔑 API Keys Disponibles

El servidor incluye las siguientes API keys predefinidas:

| API Key | Usuario | Propósito |
|---------|---------|-----------|
| `n8n-secure-key-2025` | n8n_user | Para integración con n8n |
| `admin-secure-key-2025` | admin_user | Para administración |

## 📡 Endpoints

### 🔓 Health Check (Sin autenticación)

```http
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-27T17:32:13.801380",
  "service": "OKX Candlestick Chart API for n8n (Secure)",
  "version": "2.0.0",
  "security": "API Key authentication required"
}
```

### 🔐 Generar Gráfico (JSON con base64)

```http
POST /generate-chart
Headers: X-API-Key: n8n-secure-key-2025
Content-Type: application/json
```

**Body:**
```json
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
```

**Respuesta:**
```json
{
  "success": true,
  "timestamp": "2025-07-27T17:32:13.801380",
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81,
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "debug_file": "debug_api_BTC-USDT_20250727_173213.json",
  "chart_info": {
    "start_time": "2025-07-27T10:00:00",
    "end_time": "2025-07-27T17:30:00",
    "price_range": {
      "min": 45000.0,
      "max": 46000.0
    },
    "current_price": 45500.0,
    "price_change": 500.0,
    "total_volume": 1234.56
  }
}
```

### 🔐 Generar Gráfico (Imagen Directa) ⭐ **RECOMENDADO**

```http
POST /generate-chart-image
Headers: X-API-Key: n8n-secure-key-2025
Content-Type: application/json
```

**Body:**
```json
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
```

**Respuesta:** Archivo PNG directo

### 🔐 Información del Gráfico

```http
GET /chart-info?symbol=BTC-USDT&bar=5m&candles_count=81&api_key=n8n-secure-key-2025
```

**Respuesta:**
```json
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81,
  "timestamp": "2025-07-27T17:32:13.801380",
  "time_range": {
    "start": "2025-07-27T10:00:00",
    "end": "2025-07-27T17:30:00"
  },
  "price_stats": {
    "current_price": 45500.0,
    "min_price": 45000.0,
    "max_price": 46000.0,
    "price_change": 500.0
  },
  "volume_stats": {
    "total_volume": 1234.56,
    "avg_volume": 15.24
  },
  "latest_candles": [...]
}
```

## 🔧 Configuración para n8n

### Opción 1: Header X-API-Key (Recomendado)

**HTTP Request Node:**
- **Method:** POST
- **URL:** `http://localhost:5003/generate-chart-image`
- **Headers:**
  ```
  Content-Type: application/json
  X-API-Key: n8n-secure-key-2025
  ```
- **Body (JSON):**
  ```json
  {
    "symbol": "BTC-USDT",
    "bar": "5m",
    "candles_count": 81
  }
  ```

### Opción 2: Parámetro api_key

**HTTP Request Node:**
- **Method:** POST
- **URL:** `http://localhost:5003/generate-chart-image?api_key=n8n-secure-key-2025`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (JSON):**
  ```json
  {
    "symbol": "BTC-USDT",
    "bar": "5m",
    "candles_count": 81
  }
  ```

## 📊 Parámetros

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `symbol` | string | No | BTC-USDT | Par de trading (ej: BTC-USDT, ETH-USDT) |
| `bar` | string | No | 5m | Intervalo de tiempo (1m, 5m, 15m, 1H, 4H, 1D) |
| `candles_count` | integer | No | 81 | Número de velas (1-300) |

## 🛡️ Seguridad

### Autenticación

- **Todos los endpoints** (excepto `/health`) requieren API key
- **API key** se puede enviar en:
  - Header: `X-API-Key: n8n-secure-key-2025`
  - Parámetro: `?api_key=n8n-secure-key-2025`
- **Sin API key válida** retorna error 401

### Validación

- **Parámetros** son validados antes del procesamiento
- **Datos de API** son limpiados y validados
- **Límites** en candles_count (1-300)
- **Manejo de errores** robusto

## 🔍 Debug y Troubleshooting

### Archivos de Debug

El servidor genera automáticamente archivos de debug:
```
debug_api_BTC-USDT_20250727_173213.json
```

Contiene:
- Respuesta raw de la API de OKX
- Datos procesados
- Información de timestamps
- Estadísticas de datos

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `401 Unauthorized` | API key faltante o inválida | Incluir header `X-API-Key` válido |
| `400 Bad Request` | Parámetros inválidos | Verificar `candles_count` (1-300) |
| `500 Internal Server Error` | Error en procesamiento | Revisar archivos de debug |

### Logs del Servidor

El servidor muestra logs detallados:
```
🔐 Iniciando API Server Seguro para n8n - Gráficos de Velas OKX
============================================================
📊 Endpoints disponibles:
   POST /generate-chart - Genera gráfico y retorna JSON con imagen en base64
   POST /generate-chart-image - Genera gráfico y retorna imagen directamente
   GET  /chart-info - Obtiene información del gráfico
   GET  /health - Verificación de salud del servidor
🔗 El servidor estará disponible en: http://0.0.0.0:5003
```

## 🧪 Testing

### Script de Prueba

Ejecutar el script de prueba incluido:

```bash
python test_secure_api.py
```

Prueba:
- ✅ Health check sin autenticación
- ✅ Rechazo de peticiones sin API key
- ✅ Aceptación con API key válida
- ✅ Rechazo con API key inválida
- ✅ API key como parámetro

### Prueba Manual

```bash
# Health check
curl http://localhost:5003/health

# Sin API key (debe fallar)
curl -X POST http://localhost:5003/generate-chart-image \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC-USDT","candles_count":10}'

# Con API key válida
curl -X POST http://localhost:5003/generate-chart-image \
  -H "Content-Type: application/json" \
  -H "X-API-Key: n8n-secure-key-2025" \
  -d '{"symbol":"BTC-USDT","candles_count":10}' \
  --output chart.png
```

## 📁 Estructura de Archivos

```
BotTest/
├── n8n_api_server_secure.py    # Servidor API seguro
├── test_secure_api.py          # Script de prueba
├── env_config.py               # Configuración de OKX API
├── README_N8N_SECURE.md        # Esta documentación
├── debug_api_*.json            # Archivos de debug
└── secure_chart_*.png          # Imágenes generadas
```

## 🔄 Workflow de n8n

### Ejemplo de Workflow

1. **HTTP Request Node** → Llama a la API
2. **IF Node** → Verifica si la respuesta es exitosa
3. **Write Binary File Node** → Guarda la imagen
4. **Send Email Node** → Envía la imagen por email

### Configuración del Nodo HTTP Request

```
Method: POST
URL: http://localhost:5003/generate-chart-image
Headers:
  Content-Type: application/json
  X-API-Key: n8n-secure-key-2025
Body (JSON):
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
```

## 🚀 Producción

### Consideraciones de Seguridad

1. **Cambiar API keys** por defecto
2. **Usar HTTPS** en producción
3. **Limitar acceso** por IP si es necesario
4. **Monitorear logs** regularmente
5. **Backup** de configuraciones

### Configuración de Producción

```python
# En n8n_api_server_secure.py
API_KEYS = {
    "tu-api-key-produccion": "usuario_produccion",
    "tu-api-key-backup": "usuario_backup"
}

# Usar servidor WSGI
# gunicorn -w 4 -b 0.0.0.0:5003 n8n_api_server_secure:app
```

## 📞 Soporte

### Información de Contacto

- **Servidor:** http://localhost:5003
- **Health Check:** http://localhost:5003/health
- **API Keys Info:** http://localhost:5003/api-keys

### Logs y Debug

- Revisar archivos `debug_api_*.json`
- Verificar logs del servidor
- Probar con `test_secure_api.py`

---

**✅ API Segura lista para n8n con autenticación por API key** 