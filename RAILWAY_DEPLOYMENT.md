# 🚂 Guía de Despliegue en Railway

Esta guía te ayudará a desplegar tu aplicación OKX Candlestick Analyzer en Railway.

## 📋 Prerrequisitos

- Cuenta en [Railway.app](https://railway.app)
- Repositorio de GitHub con tu código
- Credenciales de OKX API

## 🚀 Paso 1: Preparar el Repositorio

Asegúrate de que tu repositorio contenga estos archivos:

```
BotTest/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias de Python
├── Procfile              # Comando de inicio
├── railway.json          # Configuración de Railway
├── env_config.py         # Credenciales (NO subir a Git)
└── README.md             # Documentación
```

## 🔐 Paso 2: Configurar Variables de Entorno

### En Railway Dashboard:

1. Ve a tu proyecto en Railway
2. Haz clic en la pestaña "Variables"
3. Agrega estas variables de entorno:

```bash
OKX_API_KEY=tu_api_key_aqui
OKX_API_SECRET=tu_api_secret_aqui
OKX_PASSPHRASE=tu_passphrase_aqui
```

### O usando Railway CLI:

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Configurar variables
railway variables set OKX_API_KEY=tu_api_key_aqui
railway variables set OKX_API_SECRET=tu_api_secret_aqui
railway variables set OKX_PASSPHRASE=tu_passphrase_aqui
```

## 🚂 Paso 3: Desplegar en Railway

### Opción 1: Desde GitHub (Recomendado)

1. Ve a [Railway.app](https://railway.app)
2. Haz clic en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Conecta tu cuenta de GitHub
5. Selecciona tu repositorio `BotTest`
6. Railway detectará automáticamente que es una aplicación Python
7. Haz clic en "Deploy Now"

### Opción 2: Usando Railway CLI

```bash
# En tu directorio del proyecto
railway init
railway link
railway up
```

## ⚙️ Paso 4: Configuración del Dominio

1. En Railway Dashboard, ve a la pestaña "Settings"
2. En "Domains", Railway te asignará un dominio automáticamente
3. Opcional: Configura un dominio personalizado

## 🔍 Paso 5: Verificar el Despliegue

### Endpoints disponibles:

- **Página principal**: `https://tu-app.railway.app/`
- **API de velas**: `https://tu-app.railway.app/api/candles?symbol=BTC-USDT&interval=5m`
- **Health check**: `https://tu-app.railway.app/health`

### Verificar que funciona:

```bash
# Health check
curl https://tu-app.railway.app/health

# Obtener datos de velas
curl https://tu-app.railway.app/api/candles?symbol=BTC-USDT
```

## 📊 Funcionalidades de la Aplicación

### Interfaz Web:
- 📈 Gráficos de velas interactivos
- 🔄 Múltiples pares de trading (BTC, ETH, ADA, DOT, LINK)
- ⏱️ Diferentes intervalos (5m, 15m, 1H, 4H)
- 📊 Estadísticas en tiempo real
- 🎨 Diseño responsive

### API Endpoints:
- `GET /` - Página principal
- `GET /api/candles` - Datos de velas
- `GET /health` - Estado de la aplicación

## 🔧 Configuración Avanzada

### Personalizar intervalos de velas:

En `app.py`, modifica la función `get_candlestick_data`:

```python
def get_candlestick_data(symbol='BTC-USDT', bar='5m'):
    # Cambiar el número de velas
    candles_to_show = 100  # En lugar de 81
```

### Agregar más pares de trading:

En el HTML template, agrega más opciones:

```html
<select id="symbol">
    <option value="BTC-USDT">BTC-USDT</option>
    <option value="ETH-USDT">ETH-USDT</option>
    <option value="ADA-USDT">ADA-USDT</option>
    <option value="DOT-USDT">DOT-USDT</option>
    <option value="LINK-USDT">LINK-USDT</option>
    <option value="SOL-USDT">SOL-USDT</option>  <!-- Nuevo -->
    <option value="MATIC-USDT">MATIC-USDT</option>  <!-- Nuevo -->
</select>
```

## 🆘 Solución de Problemas

### Error: "Module not found"
```bash
# Verificar que requirements.txt esté correcto
pip install -r requirements.txt
```

### Error: "Environment variables not found"
- Verifica que las variables estén configuradas en Railway
- Asegúrate de que los nombres coincidan exactamente

### Error: "Port already in use"
- Railway maneja automáticamente el puerto
- No necesitas configurar PORT manualmente

### Error: "API authentication failed"
- Verifica que las credenciales de OKX sean correctas
- Asegúrate de que la API key tenga permisos de lectura

## 📈 Monitoreo

### Logs en Railway:
1. Ve a tu proyecto en Railway Dashboard
2. Pestaña "Deployments"
3. Haz clic en el deployment más reciente
4. Revisa los logs para debugging

### Métricas:
- Railway proporciona métricas básicas de uso
- Monitorea el uso de CPU y memoria
- Revisa el tiempo de respuesta

## 🔄 Actualizaciones

Para actualizar tu aplicación:

1. Haz push de los cambios a GitHub
2. Railway detectará automáticamente los cambios
3. Desplegará la nueva versión automáticamente

O manualmente:
```bash
railway up
```

## 💰 Costos

- Railway ofrece un plan gratuito generoso
- Monitorea el uso en la pestaña "Usage"
- Considera actualizar si excedes los límites gratuitos

---

¡Tu aplicación estará disponible en Railway una vez completado el despliegue! 🎉

**URL de ejemplo**: `https://okx-candlestick-analyzer.railway.app` 