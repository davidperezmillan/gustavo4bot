from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from config import CHAT_SOURCE_ID, OWNER_ID, MESSAGES, logger
from keyboards import create_media_action_keyboard
from utils.media_utils import forward_media_to_owner

async def handle_media_from_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja multimedia (imágenes, videos, animaciones) recibida del chat fuente
    """
    try:
        chat_id = update.effective_chat.id
        
        # Verificar que el mensaje viene del chat fuente configurado
        if chat_id != CHAT_SOURCE_ID:
            logger.debug(f"Mensaje ignorado del chat {chat_id} (no es el chat fuente)")
            return
        
        # Determinar el tipo de multimedia
        media_type = None
        file_id = None
        
        if update.message.photo:
            media_type = "photo"
            file_id = update.message.photo[-1].file_id
        elif update.message.video:
            media_type = "video"
            file_id = update.message.video.file_id
        elif update.message.animation:
            media_type = "animation"
            file_id = update.message.animation.file_id
        
        if not media_type:
            return
        
        logger.info(f"📸 Nueva multimedia recibida: {media_type} desde chat {chat_id}")
        
        # Crear estructura de datos del multimedia
        multimedia_data = {
            'type': media_type,
            'file_id': file_id,
            'message_id': update.message.message_id,
            'source_chat_id': chat_id,
            'media_type': media_type  # Alias para compatibilidad
        }
        
        # Enviar multimedia al propietario y guardar la referencia usando message_id
        sent_message = await forward_media_to_owner(context, media_type, file_id, OWNER_ID, multimedia_data)
        
        # Verificar que el mensaje se envió correctamente
        if sent_message:
            logger.info(f"✅ Multimedia {media_type} procesada exitosamente (msg_id: {sent_message.message_id})")
        else:
            logger.error(f"❌ Error enviando multimedia {media_type} al propietario")
        
    except Exception as e:
        logger.error(f"❌ Error procesando multimedia: {e}")

def setup_message_handlers(app):
    """Configura todos los manejadores de mensajes"""
    
    # Manejador para imágenes del chat fuente
    photo_handler = MessageHandler(
        filters.PHOTO & filters.Chat(chat_id=CHAT_SOURCE_ID),
        handle_media_from_source
    )
    
    # Manejador para videos del chat fuente
    video_handler = MessageHandler(
        filters.VIDEO & filters.Chat(chat_id=CHAT_SOURCE_ID),
        handle_media_from_source
    )
    
    # Manejador para animaciones del chat fuente
    animation_handler = MessageHandler(
        filters.ANIMATION & filters.Chat(chat_id=CHAT_SOURCE_ID),
        handle_media_from_source
    )
    
    # Agregar manejadores a la aplicación
    app.add_handler(photo_handler)
    app.add_handler(video_handler)
    app.add_handler(animation_handler)
    
    logger.info("✅ Manejadores de mensajes configurados")