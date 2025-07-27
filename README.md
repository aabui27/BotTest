# 📊 Bot de Análisis de Criptomonedas OKX

Este proyecto obtiene datos de velas de Bitcoin desde la API de OKX y genera gráficos interactivos usando Plotly.

## 🚀 Instalación

1. Instala las dependencias:
```bash
pip install requests pandas plotly
```

2. Configura tus credenciales:
   - Renombra `env_config.py` a `.env` (opcional, para mayor seguridad)
   - Actualiza las credenciales de tu API de OKX en el archivo

## 🔐 Configuración de Credenciales

Edita el archivo `env_config.py` con tus credenciales de OKX:

```python
OKX_API_KEY = 'tu_api_key_aqui'
OKX_API_SECRET = 'tu_api_secret_aqui'
OKX_PASSPHRASE = 'tu_passphrase_aqui'
```

## 📈 Uso

Ejecuta el script principal:

```bash
python test.py
```

El script:
- Se conecta a la API de OKX
- Obtiene las últimas 100 velas de 5 minutos de Bitcoin-USDT
- Genera un gráfico de velas interactivo
- Abre automáticamente el gráfico en tu navegador

## 🔧 Personalización

Puedes modificar estos parámetros en `test.py`:

- `symbol`: Par de trading (ej: 'BTC-USDT', 'ETH-USDT')
- `bar`: Intervalo de tiempo (ej: '1m', '5m', '15m', '1H', '4H', '1D')
- `limit`: Número de velas a obtener (máximo 300)

## ⚠️ Seguridad

- Nunca subas tus credenciales a un repositorio público
- El archivo `.gitignore` ya está configurado para proteger las credenciales
- Considera usar variables de entorno del sistema para mayor seguridad

## 📋 Dependencias

- `requests`: Para llamadas HTTP a la API
- `pandas`: Para procesamiento de datos
- `plotly`: Para generar gráficos interactivos 