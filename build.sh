#!/bin/bash

# Script para construir y preparar Gustavo4Bot para Portainer

echo "🏗️  Construyendo imagen de Gustavo4Bot..."

# Construir la imagen
docker build -t gustavo4bot:latest .

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
    echo ""
    echo "📋 Pasos para desplegar en Portainer:"
    echo ""
    echo "1. Ir a Portainer > Stacks > Add Stack"
    echo "2. Nombre del stack: gustavo4bot"
    echo "3. Copiar el contenido de 'portainer-stack.yml'"
    echo "4. Configurar las variables de entorno:"
    echo "   - TELEGRAM_TOKEN: 7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0"
    echo "   - OWNER_ID: [TU_ID_DE_USUARIO]"
    echo "   - CHAT_SOURCE_ID: [ID_DEL_CHAT_FUENTE]"
    echo "   - PUBLISH_CHANNEL_ID: [ID_DEL_CANAL_PUBLICACION]"
    echo "   - STORAGE_CHANNEL_ID: [ID_DEL_CANAL_ALMACENAMIENTO]"
    echo "   - LOG_LEVEL: INFO (opcional)"
    echo "   - TZ: Europe/Madrid (opcional)"
    echo "5. Deploy the stack"
    echo ""
    echo "🔍 Para obtener los IDs:"
    echo "   - Tu ID: Envía /start a @userinfobot"
    echo "   - Chat/Canal IDs: Agrega @userinfobot al chat/canal"
    echo ""
else
    echo "❌ Error construyendo la imagen"
    exit 1
fi