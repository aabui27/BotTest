# 🚀 Guía de Despliegue a GitHub

Esta guía te ayudará a subir tu proyecto BotTest a GitHub.

## 📋 Prerrequisitos

- Tener GitHub CLI instalado (`gh`)
- Tener una cuenta de GitHub
- Tener Git configurado localmente

## 🔐 Paso 1: Autenticación con GitHub

Ejecuta el siguiente comando y sigue las instrucciones:

```bash
gh auth login
```

**Opciones recomendadas:**
- **Where do you use GitHub?** → `GitHub.com`
- **What is your preferred protocol for Git operations?** → `HTTPS`
- **Authenticate Git with your GitHub credentials?** → `Y`
- **How would you like to authenticate GitHub CLI?** → `Login with a web browser`

## 🚀 Paso 2: Desplegar el Proyecto

Una vez autenticado, ejecuta el script de despliegue:

```bash
./deploy_to_github.sh
```

Este script:
- ✅ Verifica la autenticación
- 📋 Revisa el estado del repositorio
- 🔄 Agrega cambios pendientes
- 🆕 Crea el repositorio en GitHub (si no existe)
- 📤 Hace push del código

## 🔧 Despliegue Manual (Alternativo)

Si prefieres hacerlo manualmente:

### 1. Crear el repositorio en GitHub
```bash
gh repo create BotTest \
    --public \
    --description "OKX API candlestick data analyzer with debug functionality" \
    --source=. \
    --remote=origin \
    --push
```

### 2. O usar la interfaz web de GitHub
1. Ve a [GitHub.com](https://github.com)
2. Haz clic en "New repository"
3. Nombre: `BotTest`
4. Descripción: `OKX API candlestick data analyzer with debug functionality`
5. Público
6. **NO** inicialices con README (ya tienes uno)
7. Haz clic en "Create repository"

### 3. Conectar tu repositorio local
```bash
git remote add origin https://github.com/TU_USUARIO/BotTest.git
git branch -M main
git push -u origin main
```

## 📁 Estructura del Repositorio

Una vez desplegado, tu repositorio contendrá:

```
BotTest/
├── test.py                 # Script principal
├── analyze_debug.py        # Analizador de debug
├── deploy_to_github.sh     # Script de despliegue
├── README.md              # Documentación
├── DEPLOYMENT.md          # Esta guía
├── .gitignore            # Archivos ignorados
├── .gitattributes        # Atributos de Git
└── candles_*.json         # Datos de ejemplo
```

## 🔒 Seguridad

- ✅ `env_config.py` está excluido del repositorio
- ✅ Las credenciales nunca se subirán
- ✅ El `.gitignore` protege información sensible

## 🌐 Verificar el Despliegue

Una vez completado, podrás acceder a tu repositorio en:
```
https://github.com/TU_USUARIO/BotTest
```

## 🆘 Solución de Problemas

### Error: "GitHub CLI no está autenticado"
```bash
gh auth login
```

### Error: "Repository already exists"
```bash
git remote set-url origin https://github.com/TU_USUARIO/BotTest.git
git push origin main
```

### Error: "Permission denied"
- Verifica que tu token de GitHub tenga permisos de repositorio
- Ejecuta `gh auth refresh` para renovar la autenticación

## 📞 Soporte

Si encuentras problemas:
1. Verifica que GitHub CLI esté actualizado: `gh --version`
2. Revisa el estado de autenticación: `gh auth status`
3. Consulta la documentación: `gh help`

---

¡Tu proyecto estará disponible públicamente en GitHub una vez completado el despliegue! 🎉 