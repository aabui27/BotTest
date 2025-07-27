#!/bin/bash

# Script para desplegar el código a GitHub
# Uso: ./deploy_to_github.sh

echo "🚀 Desplegando BotTest a GitHub..."

# Verificar si gh está autenticado
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ Error: GitHub CLI no está autenticado"
    echo "Por favor ejecuta: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI autenticado correctamente"

# Verificar el estado del repositorio
echo "📋 Verificando estado del repositorio..."
git status

# Verificar si hay cambios pendientes
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Hay cambios pendientes. Agregando todos los archivos..."
    git add .
    git commit -m "feat: Update project with latest changes"
fi

# Verificar si ya existe un repositorio remoto
if git remote get-url origin >/dev/null 2>&1; then
    echo "📤 Haciendo push al repositorio existente..."
    git push origin main
else
    echo "🆕 Creando nuevo repositorio en GitHub..."
    gh repo create BotTest \
        --public \
        --description "OKX API candlestick data analyzer with debug functionality" \
        --source=. \
        --remote=origin \
        --push
fi

echo "✅ ¡Despliegue completado!"
echo "🌐 Tu repositorio está disponible en: https://github.com/$(gh api user --jq .login)/BotTest" 