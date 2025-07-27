# BotTest - OKX API Candlestick Data Analyzer

Un sistema completo para obtener, analizar y visualizar datos de velas (candlesticks) de la API de OKX, con funcionalidades de acumulación de datos y debug.

## 🚀 Características

- **Obtención de datos en tiempo real**: Conecta con la API de OKX para obtener datos de velas de 5 minutos
- **Acumulación inteligente**: Mantiene las últimas 81 velas, actualizándose cada 5 minutos
- **Persistencia de datos**: Guarda los datos en archivos JSON para análisis posterior
- **Sistema de debug completo**: Genera archivos de debug con toda la información de la API
- **Visualización interactiva**: Gráficos de velas con Plotly
- **Análisis de datos**: Script para analizar y mostrar estadísticas de los datos

## 📁 Estructura del Proyecto

```
BotTest/
├── test.py                 # Script principal para obtener datos y generar gráficos
├── analyze_debug.py        # Script para analizar archivos de debug
├── env_config.py          # Configuración de credenciales (no incluido en Git)
├── README.md              # Este archivo
├── .gitignore            # Archivos ignorados por Git
├── candles_*.json         # Datos de velas guardados por fecha
└── debug_api_*.json       # Archivos de debug con información de la API
```

## 🛠️ Instalación

1. **Clona el repositorio**:
   ```bash
   git clone <tu-repositorio>
   cd BotTest
   ```

2. **Instala las dependencias**:
   ```bash
   pip install requests pandas plotly
   ```

3. **Configura las credenciales**:
   Crea un archivo `env_config.py` con tus credenciales de OKX:
   ```python
   OKX_API_KEY = "tu-api-key"
   OKX_API_SECRET = "tu-api-secret"
   OKX_PASSPHRASE = "tu-passphrase"
   ```

## 📊 Uso

### Ejecutar el script principal

```bash
python test.py
```

Este comando:
- Obtiene las últimas 81 velas de 5 minutos de BTC-USDT
- Acumula los datos con ejecuciones anteriores
- Genera un gráfico interactivo
- Guarda los datos en `candles_BTC-USDT_YYYY-MM-DD.json`
- Crea un archivo de debug con toda la información

### Analizar archivos de debug

```bash
python analyze_debug.py
```

Este comando:
- Lista todos los archivos de debug disponibles
- Muestra estadísticas detalladas de los datos
- Presenta las primeras y últimas velas
- Calcula rangos de precios y volúmenes

## 🔍 Funcionalidades de Debug

### Archivo de Debug (`debug_api_*.json`)

Cada ejecución genera un archivo con:
- **Timestamp de ejecución**
- **Información de la petición API**:
  - URL y parámetros
  - Status code
  - Datos completos recibidos (100 velas)
- **Datos procesados**:
  - Velas utilizadas para el gráfico (81 velas)
  - Datos filtrados
- **Información de estructura**:
  - Columnas del DataFrame
  - Descripción de los datos

### Script de Análisis

El script `analyze_debug.py` proporciona:
- 📅 Timestamp de ejecución
- 🌐 Información de la API
- 📊 Estadísticas de datos procesados
- 🕯️ Primeras y últimas 5 velas
- 📈 Estadísticas básicas (precios, volúmenes)

## ⚙️ Configuración

### Parámetros del Script

En `test.py` puedes modificar:
- `symbol`: Par de trading (por defecto: 'BTC-USDT')
- `bar`: Intervalo de tiempo (por defecto: '5m')
- `candles_to_show`: Número de velas a mostrar (por defecto: 81)

### Ejecución Automática

Para ejecutar cada 5 minutos, puedes usar cron:

```bash
# Editar crontab
crontab -e

# Agregar esta línea para ejecutar cada 5 minutos
*/5 * * * * cd /ruta/a/BotTest && python test.py
```

## 📈 Datos Generados

### Archivo de Velas (`candles_*.json`)

Contiene las últimas 81 velas con:
- Timestamp en milisegundos
- Precios OHLC (Open, High, Low, Close)
- Volumen en BTC y USDT
- Número de trades

### Archivo de Debug (`debug_api_*.json`)

Contiene información completa de:
- Respuesta completa de la API
- Datos procesados
- Metadatos de la petición
- Estadísticas de procesamiento

## 🔐 Seguridad

- El archivo `env_config.py` está excluido del control de versiones
- Las credenciales nunca se suben a GitHub
- Usa autenticación HMAC SHA256 para la API

## 📝 Logs y Debug

El sistema genera logs detallados:
- Estado de la conexión API
- Número de velas obtenidas
- Proceso de acumulación de datos
- Errores y advertencias

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema:
1. Revisa los archivos de debug generados
2. Verifica la conectividad con la API de OKX
3. Asegúrate de que las credenciales sean correctas
4. Revisa los logs de ejecución

---

**Nota**: Este proyecto es para fines educativos y de análisis. Asegúrate de cumplir con los términos de servicio de OKX. 