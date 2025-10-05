from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, filters, ContextTypes
from config import OWNER_ID, MESSAGES, WAITING_CAPTION, logger
from keyboards import create_cancel_keyboard
from utils.media_utils import send_media_with_spoiler, delete_bot_message, store_multimedia, delete_source_message

async def handle_caption_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la entrada de leyenda personalizada del usuario"""
    
    # Obtener la leyenda ingresada por el usuario
    user_caption = update.message.text
    
    # Obtener el message_id del multimedia asociado
    message_id = context.user_data.get('current_message_id')
    if not message_id:
        await update.message.reply_text("❌ Error: No se encontró el multimedia asociado")
        return ConversationHandler.END
    
    # Obtener datos del multimedia
    multimedia_data = context.bot_data.get('media_messages', {}).get(message_id)
    if not multimedia_data:
        await update.message.reply_text("❌ Error: No se encontraron datos del multimedia")
        return ConversationHandler.END

    try:
        # Almacenar multimedia con la leyenda personalizada y spoiler
        await store_multimedia(
            context,
            multimedia_data['source_chat_id'],
            multimedia_data['message_id'],
            multimedia_data['file_id'],
            multimedia_data['media_type'],
            user_caption,  # Usar la leyenda personalizada
            has_spoiler=True
        )

        # Confirmar al usuario
        await update.message.reply_text(f"✅ Multimedia enviada con leyenda: \"{user_caption}\"")
        
        # Editar el mensaje original del bot para confirmar
        try:
            await context.bot.edit_message_caption(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                caption=f"✅ Multimedia enviada con leyenda personalizada",
                reply_markup=None
            )
        except Exception as e:
            logger.warning(f"No se pudo editar mensaje original: {e}")
        
        # Limpiar datos temporales
        if 'current_message_id' in context.user_data:
            del context.user_data['current_message_id']
        if message_id in context.bot_data.get('media_messages', {}):
            del context.bot_data['media_messages'][message_id]

        logger.info(f"✅ Multimedia enviada con leyenda personalizada: {user_caption}")

    except Exception as e:
        logger.error(f"❌ Error procesando leyenda personalizada: {e}")
        await update.message.reply_text("❌ Error procesando la leyenda")

    return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancela la conversación de leyenda
    """
    try:
        # Obtener el mensaje del bot para editarlo
        bot_message = context.user_data.get('bot_message')
        if bot_message:
            try:
                await bot_message.edit_caption(
                    caption=MESSAGES['cancelled'],
                    reply_markup=bot_message.reply_markup  # Mantener botones
                )
            except:
                await update.message.reply_text(MESSAGES['cancelled'])
        
        # NO limpiar datos pendientes para permitir otras acciones
        # context.user_data.pop('pending_media', None)
        # context.user_data.pop('bot_message', None)
        
        return ConversationHandler.END
        
    except Exception as e:
        logger.error(f"❌ Error cancelando conversación: {e}")
        return ConversationHandler.END

def setup_conversation_handlers(app):
    """Configura el manejador de conversaciones"""
    
    # ConversationHandler para manejar la entrada de leyendas
    caption_conv_handler = ConversationHandler(
        entry_points=[],  # Se inicia desde el callback handler
        states={
            WAITING_CAPTION: [
                MessageHandler(
                    filters.TEXT & filters.User(user_id=OWNER_ID) & ~filters.COMMAND,
                    handle_caption_input
                )
            ]
        },
        fallbacks=[
            MessageHandler(filters.COMMAND, cancel_conversation)
        ],
        allow_reentry=True
    )
    
    app.add_handler(caption_conv_handler)
    logger.info("✅ Manejador de conversaciones configurado")