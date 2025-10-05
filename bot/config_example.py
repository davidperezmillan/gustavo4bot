# Configuración de ejemplo para Gustavo4Bot
# Copia este archivo a config.py y configura los valores

# Token del bot de Telegram
TELEGRAM_TOKEN = "7850932225:AAF5ACUWuvwI0Av8tt9Q4_yRXBWPFlxbxa0"

# IDs de configuración - CAMBIAR ESTOS VALORES
OWNER_ID = None  # Tu ID de usuario de Telegram (ej: 123456789)
CHAT_SOURCE_ID = None  # ID del chat del que recuperar multimedia (ej: -100123456789)
PUBLISH_CHANNEL_ID = None  # ID del canal para enviar con spoiler (ej: -100123456789)
STORAGE_CHANNEL_ID = None  # ID del canal para almacenar (ej: -100987654321)

# Instrucciones para obtener IDs:
# 
# Para tu ID de usuario:
# 1. Envía /start a @userinfobot
# 2. El bot te responderá con tu ID
# 
# Para IDs de canales/grupos:
# 1. Agrega @userinfobot al canal/grupo
# 2. El bot mostrará el ID del chat
# 3. Los IDs de canales/grupos empiezan con -100
# 
# Ejemplo de configuración:
# OWNER_ID = 123456789
# CHAT_SOURCE_ID = -1001234567890
# PUBLISH_CHANNEL_ID = -1001234567891
# STORAGE_CHANNEL_ID = -1001234567892