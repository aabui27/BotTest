# 🔧 Solución de Problemas - API Segura para n8n

## 🚨 Error: ECONNREFUSED

### Problema
```
Error code: ECONNREFUSED
Full message: connect ECONNREFUSED 127.0.0.1:5003
```

### Soluciones

#### 1. ✅ **Verificar que el servidor esté ejecutándose**

```bash
# Verificar procesos
ps aux | grep n8n_api_server

# Verificar puerto
lsof -i :5004

# Probar conectividad
curl http://localhost:5004/health
```

#### 2. ✅ **Usar la URL correcta**

**URLs disponibles:**
- `http://localhost:5004/generate-chart-image` ⭐ **RECOMENDADO**
- `http://127.0.0.1:5004/generate-chart-image`

#### 3. ✅ **Configuración correcta para n8n**

**HTTP Request Node:**
```
Method: POST
URL: http://localhost:5004/generate-chart-image
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

## 🔍 Diagnóstico Automático

### Ejecutar script de diagnóstico

```bash
python test_network_api.py
```

Este script:
- ✅ Verifica conectividad de red
- ✅ Prueba autenticación
- ✅ Genera configuración para n8n
- ✅ Identifica URLs funcionando

## 🌐 Problemas de Red

### Si n8n está en Docker

**Usar IP local en lugar de localhost:**
```
URL: http://192.168.68.129:5004/generate-chart-image
```

### Si n8n está en otra máquina

**Usar IP de red:**
```
URL: http://[IP_DE_LA_MAQUINA]:5004/generate-chart-image
```

### Verificar firewall

```bash
# macOS
sudo pfctl -s rules

# Linux
sudo iptables -L

# Windows
netsh advfirewall show allprofiles
```

## 🔐 Problemas de Autenticación

### Error 401 - API Key requerida

**Solución:**
- Incluir header `X-API-Key: n8n-secure-key-2025`
- O usar parámetro `?api_key=n8n-secure-key-2025`

### API Keys disponibles

| API Key | Usuario | Propósito |
|---------|---------|-----------|
| `n8n-secure-key-2025` | n8n_user | Para integración con n8n |
| `admin-secure-key-2025` | admin_user | Para administración |

## 🚀 Iniciar Servidor

### Opción 1: Servidor Básico
```bash
python n8n_api_server_secure.py
# Puerto: 5003
```

### Opción 2: Servidor Optimizado para Red ⭐ **RECOMENDADO**
```bash
python n8n_api_server_secure_network.py
# Puerto: 5004
```

## 📊 Verificar Funcionamiento

### 1. Health Check
```bash
curl http://localhost:5004/health
```

### 2. Información de Red
```bash
curl http://localhost:5004/network-info
```

### 3. Probar API con Autenticación
```bash
curl -X POST http://localhost:5004/generate-chart-image \
  -H "Content-Type: application/json" \
  -H "X-API-Key: n8n-secure-key-2025" \
  -d '{"symbol":"BTC-USDT","candles_count":10}' \
  --output test.png
```

## 🔧 Configuración de n8n

### HTTP Request Node

**Configuración básica:**
```
Method: POST
URL: http://localhost:5004/generate-chart-image
```

**Headers:**
```
Content-Type: application/json
X-API-Key: n8n-secure-key-2025
```

**Body (JSON):**
```json
{
  "symbol": "BTC-USDT",
  "bar": "5m",
  "candles_count": 81
}
```

### Configuración Avanzada

**Timeout:**
```
Timeout: 300000 (5 minutos)
```

**Opciones adicionales:**
```
- gzip: true
- rejectUnauthorized: true
- followRedirect: true
- resolveWithFullResponse: true
- followAllRedirects: true
- useStream: true
```

## 📋 Checklist de Solución

### ✅ Verificaciones Básicas

- [ ] Servidor ejecutándose en puerto 5004
- [ ] Health check responde correctamente
- [ ] API key incluida en headers
- [ ] URL correcta (localhost:5004)
- [ ] Método POST
- [ ] Content-Type: application/json

### ✅ Verificaciones Avanzadas

- [ ] Firewall permitiendo puerto 5004
- [ ] n8n puede acceder a la red local
- [ ] No hay conflictos de puertos
- [ ] Servidor con CORS habilitado
- [ ] Autenticación funcionando

## 🆘 Comandos de Emergencia

### Reiniciar Servidor
```bash
# Detener todos los procesos
pkill -f "n8n_api_server"

# Iniciar servidor optimizado
python n8n_api_server_secure_network.py
```

### Verificar Puertos
```bash
# Ver qué está usando el puerto
lsof -i :5004

# Ver todos los puertos en uso
netstat -an | grep LISTEN
```

### Logs del Servidor
```bash
# Ver logs en tiempo real
tail -f /var/log/syslog | grep python

# Ver procesos Python
ps aux | grep python
```

## 📞 Información de Contacto

### Endpoints de Información

- **Health Check:** `GET http://localhost:5004/health`
- **Network Info:** `GET http://localhost:5004/network-info`
- **API Keys:** `GET http://localhost:5004/api-keys`

### Archivos de Debug

El servidor genera automáticamente:
```
debug_api_BTC-USDT_YYYYMMDD_HHMMSS.json
```

### Scripts de Prueba

- `test_network_api.py` - Diagnóstico completo
- `test_secure_api.py` - Pruebas de autenticación

---

## 🎯 Resumen de Solución

**Para resolver ECONNREFUSED:**

1. **Ejecutar servidor optimizado:**
   ```bash
   python n8n_api_server_secure_network.py
   ```

2. **Usar configuración correcta en n8n:**
   ```
   URL: http://localhost:5004/generate-chart-image
   Headers: X-API-Key: n8n-secure-key-2025
   ```

3. **Verificar con script de diagnóstico:**
   ```bash
   python test_network_api.py
   ```

**¡La API está lista para n8n con autenticación segura!** 🚀 