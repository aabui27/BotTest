# API de Gráficos de Velas OKX para n8n

Este proyecto proporciona una API REST que genera gráficos de velas (candlestick) de la API de OKX, optimizada para integración con n8n.

## 🚀 Características

- ✅ **Genera gráficos de velas** de cualquier par de trading de OKX
- ✅ **Configurable**: Número de velas, intervalo de tiempo, símbolo
- ✅ **Optimizado para n8n**: Endpoints REST simples
- ✅ **Múltiples formatos**: Imagen directa o JSON con base64
- ✅ **Información detallada**: Precios, volúmenes, estadísticas
- ✅ **Debug completo**: Archivos de debug para análisis

## 📋 Requisitos

- Python 3.8+
- Credenciales de API de OKX
- Dependencias: Flask, pandas, matplotlib, mplfinance

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone <tu-repositorio>
cd BotTest
```

2. **Instalar dependencias**:
```bash
pip install flask flask-cors pandas matplotlib mplfinance requests
```

3. **Configurar credenciales**:
Crear archivo `env_config.py` con tus credenciales de OKX:
```python
OKX_API_KEY = "tu-api-key"
OKX_API_SECRET = "tu-api-secret"
OKX_PASSPHRASE = "tu-passphrase"
```

## 🚀 Uso

### Iniciar el servidor

```bash
python n8n_api_server_final.py
```

El servidor estará disponible en: `http://localhost:5002`

### Endpoints disponibles

#### 1. Health Check
```
GET /health
```
Verifica que el servidor esté funcionando.

#### 2. Generar gráfico (Imagen directa) - **RECOMENDADO**
```
POST /generate-chart-image
```
Retorna la imagen PNG directamente.

#### 3. Generar gráfico (JSON con base64)
```
POST /generate-chart
```
Retorna JSON con la imagen en formato base64.

#### 4. Información del gráfico
```
GET /chart-info
```
Retorna información estadística sin generar imagen.

## 🔗 Integración con n8n

### Opción 1: Imagen directa (Recomendada)

**Configuración en n8n:**

1. **HTTP Request Node**:
   - **Method**: POST
   - **URL**: `http://localhost:5002/generate-chart-image`
   - **Headers**: `Content-Type: application/json`
   - **Body** (JSON):
   ```json
   {
     "symbol": "BTC-USDT",
     "bar": "5m",
     "candles_count": 81
   }
   ```

2. **Respuesta**: Imagen PNG directa

3. **Uso en n8n**:
   - **Telegram**: Adjuntar directamente como archivo
   - **Email**: Adjuntar como archivo adjunto
   - **Discord**: Subir imagen al canal
   - **Slack**: Enviar imagen al canal

### Opción 2: JSON con base64

**Configuración en n8n:**

1. **HTTP Request Node**:
   - **Method**: POST
   - **URL**: `http://localhost:5002/generate-chart`
   - **Headers**: `Content-Type: application/json`
   - **Body**: Mismo JSON que arriba

2. **Respuesta**:
```json
{
  "success": true,
  "timestamp": "2025-07-27T17:20:00.000000",
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81,
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "debug_file": "debug_api_BTC-USDT_20250727_172000.json",
  "chart_info": {
    "start_time": "2025-07-27T10:00:00",
    "end_time": "2025-07-27T17:20:00",
    "price_range": {
      "min": 118000.0,
      "max": 119500.0
    },
    "current_price": 118950.0,
    "price_change": 150.0,
    "total_volume": 1500.5
  }
}
```

3. **Uso en n8n**:
   - Decodificar base64: `{{ $json.image_base64 }}`
   - Obtener precio actual: `{{ $json.chart_info.current_price }}`
   - Obtener cambio de precio: `{{ $json.chart_info.price_change }}`

## 📊 Parámetros

### Símbolos disponibles
- `BTC-USDT` (Bitcoin)
- `ETH-USDT` (Ethereum)
- `ADA-USDT` (Cardano)
- Cualquier par disponible en OKX

### Intervalos de tiempo
- `1m` - 1 minuto
- `5m` - 5 minutos (recomendado)
- `15m` - 15 minutos
- `1H` - 1 hora
- `4H` - 4 horas
- `1D` - 1 día

### Número de velas
- Mínimo: 1
- Máximo: 300
- Recomendado: 81 (para mostrar ~6.75 horas de datos)

## 🔧 Ejemplos de uso

### Ejemplo 1: Gráfico de Bitcoin (81 velas de 5 minutos)
```json
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
```

### Ejemplo 2: Gráfico de Ethereum (50 velas de 15 minutos)
```json
{
  "symbol": "ETH-USDT",
  "bar": "15m",
  "candles_count": 50
}
```

### Ejemplo 3: Gráfico de Cardano (100 velas de 1 minuto)
```json
{
  "symbol": "ADA-USDT",
  "bar": "1m",
  "candles_count": 100
}
```

## 📁 Archivos generados

### Imágenes
- `n8n_chart_YYYYMMDD_HHMMSS.png` - Gráficos generados
- `test_chart_*.png` - Imágenes de prueba

### Debug
- `debug_api_SYMBOL_YYYYMMDD_HHMMSS.json` - Información completa de la API
- `candles_SYMBOL_YYYY-MM-DD.json` - Datos de velas guardados

## 🧪 Pruebas

### Probar la API
```bash
python test_n8n_simple.py
```

### Analizar archivos de debug
```bash
python analyze_debug.py
```

## 🔄 Automatización

### Ejecutar cada 5 minutos
En n8n, configura un **Cron Node** para ejecutar cada 5 minutos:

```
*/5 * * * *
```

### Flujo completo en n8n
1. **Cron Node** → Ejecutar cada 5 minutos
2. **HTTP Request Node** → Llamar a la API
3. **Telegram Node** → Enviar imagen
4. **Email Node** → Enviar reporte

## 🚨 Solución de problemas

### Error de conexión
- Verificar que el servidor esté ejecutándose
- Verificar puerto 5002
- Verificar credenciales de OKX

### Error de datos
- Verificar símbolo válido
- Verificar intervalo de tiempo válido
- Revisar archivos de debug

### Error de imagen
- Verificar dependencias de matplotlib
- Verificar permisos de escritura
- Revisar logs del servidor

## 📞 Soporte

Para problemas o preguntas:
1. Revisar archivos de debug generados
2. Verificar logs del servidor
3. Probar con diferentes parámetros

## 📝 Notas importantes

- **Credenciales**: Mantén tus credenciales de OKX seguras
- **Rate Limits**: Respeta los límites de la API de OKX
- **Almacenamiento**: Los archivos de debug pueden crecer, considera limpiarlos periódicamente
- **Rendimiento**: Para uso intensivo, considera optimizar el servidor

## 🔄 Actualizaciones

Para actualizar el servidor:
1. Detener el servidor actual
2. Actualizar el código
3. Reiniciar el servidor

```bash
pkill -f api_server
python n8n_api_server_final.py
```

---

**¡Listo para usar con n8n! 🎉** 