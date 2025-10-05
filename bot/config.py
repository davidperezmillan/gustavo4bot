import os
import logging
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN DEL BOT - Variables de entorno
# =============================================================================

# Token del bot
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# IDs de configuración
OWNER_ID = int(os.getenv('OWNER_ID')) if os.getenv('OWNER_ID') else None
CHAT_SOURCE_ID = int(os.getenv('CHAT_SOURCE_ID')) if os.getenv('CHAT_SOURCE_ID') else None
PUBLISH_CHANNEL_ID = int(os.getenv('PUBLISH_CHANNEL_ID')) if os.getenv('PUBLISH_CHANNEL_ID') else None
STORAGE_CHANNEL_ID = int(os.getenv('STORAGE_CHANNEL_ID')) if os.getenv('STORAGE_CHANNEL_ID') else None

# Configuración de logs
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

# Convertir nivel de log de string a constante
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log_level,
    handlers=[
        logging.FileHandler('/app/logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# =============================================================================
# ESTADOS DE CONVERSACIÓN
# =============================================================================

# Estados para el ConversationHandler
WAITING_CAPTION = 1

# =============================================================================
# MENSAJES DEL BOT
# =============================================================================

MESSAGES = {
    'new_media': '📸 Nueva multimedia recibida desde el chat fuente:',
    'choose_action': 'Elige una acción:',
    'request_caption': '✏️ Escribe la leyenda para enviar con la imagen:',
    'sent_with_spoiler': '✅ Enviado al canal con spoiler',
    'sent_with_caption': '✅ Enviado al canal con leyenda y spoiler',
    'stored': '📁 Almacenado en el canal de archivos',
    'discarded': '🗑️ Multimedia descartado',
    'cancelled': '❌ Operación cancelada',
    'error': '⚠️ Error al procesar la solicitud',
    'unauthorized': '🚫 No tienes permisos para usar este bot'
}

# =============================================================================
# VALIDACIONES
# =============================================================================

def validate_config():
    """Valida que la configuración esté completa"""
    missing = []
    
    if not TELEGRAM_TOKEN:
        missing.append("TELEGRAM_TOKEN")
    if not OWNER_ID:
        missing.append("OWNER_ID")
    if not CHAT_SOURCE_ID:
        missing.append("CHAT_SOURCE_ID")
    if not PUBLISH_CHANNEL_ID:
        missing.append("PUBLISH_CHANNEL_ID")
    if not STORAGE_CHANNEL_ID:
        missing.append("STORAGE_CHANNEL_ID")
    
    if missing:
        logger.error(f"❌ Configuración incompleta. Faltan: {', '.join(missing)}")
        logger.error("📝 Por favor, configura estos valores en config.py")
        return False
    
    return True

# Crear directorio de logs si no existe
Path('/app/logs').mkdir(parents=True, exist_ok=True)