from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ContextTypes
from config import OWNER_ID, MESSAGES, logger
from utils.media_utils import send_media_with_spoiler, send_media_to_storage, delete_bot_message, store_multimedia, delete_source_message

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja todas las respuestas a botones inline
    """
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
        # Verificar que el usuario es el propietario
        if user_id != OWNER_ID:
            await query.answer(MESSAGES['unauthorized'], show_alert=True)
            return
        
        # Obtener datos del multimedia usando message_id
        message_id = query.message.message_id
        multimedia_data = context.bot_data.get('media_messages', {}).get(message_id)
        
        if not multimedia_data:
            await query.answer("❌ No hay multimedia pendiente", show_alert=True)
            logger.error(f"❌ No se encontraron datos de multimedia para el mensaje {message_id}")
            return
        
        await query.answer()  # Confirmar recepción del callback
        
        # Procesar según la acción seleccionada
        action = query.data
        
        if action == "action_send":
            await handle_send_action(update, context)
            
        elif action == "action_send_caption":
            await handle_caption_action(update, context)
            
        elif action == "action_store":
            await handle_store_action(update, context)
            
        elif action == "action_discard":
            await handle_discard_action(update, context)
            
        elif action == "cancel_caption":
            await handle_cancel_action(update, context)
        
    except Exception as e:
        logger.error(f"❌ Error en callback query: {e}")
        try:
            await query.message.edit_caption(
                caption=MESSAGES['error'],
                reply_markup=None
            )
        except:
            try:
                await query.message.reply_text(MESSAGES['error'])
            except:
                logger.error("❌ No se pudo enviar mensaje de error")

async def handle_store_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la acción de almacenar multimedia sin leyenda"""
    query = update.callback_query
    
    # Obtener datos del multimedia usando message_id
    message_id = query.message.message_id
    multimedia_data = context.bot_data.get('media_messages', {}).get(message_id)
    
    if not multimedia_data:
        logger.error(f"❌ No se encontraron datos de multimedia para el mensaje {message_id}")
        await query.edit_message_caption(
            caption="❌ Error: No se encontraron datos del multimedia",
            reply_markup=None
        )
        return

    try:
        # Almacenar multimedia sin spoiler
        await store_multimedia(
            context,
            multimedia_data['source_chat_id'],
            multimedia_data['message_id'],
            multimedia_data['file_id'],
            multimedia_data['media_type'],
            multimedia_data.get('caption', ''),
            has_spoiler=False
        )

        # Actualizar mensaje de confirmación
        await query.edit_message_caption(
            caption="✅ Multimedia almacenada exitosamente",
            reply_markup=None
        )
        
        # Limpiar datos del mensaje
        if message_id in context.bot_data.get('media_messages', {}):
            del context.bot_data['media_messages'][message_id]

        logger.info(f"✅ Multimedia almacenada sin spoiler para mensaje {message_id}")

    except Exception as e:
        logger.error(f"❌ Error almacenando multimedia: {e}")
        await query.edit_message_caption(
            caption="❌ Error almacenando multimedia",
            reply_markup=None
        )


async def handle_send_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la acción de enviar multimedia con spoiler"""
    query = update.callback_query
    
    # Obtener datos del multimedia usando message_id  
    message_id = query.message.message_id
    multimedia_data = context.bot_data.get('media_messages', {}).get(message_id)
    
    if not multimedia_data:
        logger.error(f"❌ No se encontraron datos de multimedia para el mensaje {message_id}")
        await query.edit_message_caption(
            caption="❌ Error: No se encontraron datos del multimedia",
            reply_markup=None
        )
        return

    try:
        # Almacenar multimedia con spoiler
        await store_multimedia(
            context,
            multimedia_data['source_chat_id'],
            multimedia_data['message_id'],
            multimedia_data['file_id'],
            multimedia_data['media_type'],
            multimedia_data.get('caption', ''),
            has_spoiler=True
        )

        # Actualizar mensaje de confirmación
        await query.edit_message_caption(
            caption="✅ Multimedia enviada con spoiler",
            reply_markup=None
        )
        
        # Limpiar datos del mensaje
        if message_id in context.bot_data.get('media_messages', {}):
            del context.bot_data['media_messages'][message_id]

        logger.info(f"✅ Multimedia enviada con spoiler para mensaje {message_id}")

    except Exception as e:
        logger.error(f"❌ Error enviando multimedia: {e}")
        await query.edit_message_caption(
            caption="❌ Error enviando multimedia",
            reply_markup=None
        )


async def handle_caption_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la acción de enviar multimedia con leyenda personalizada"""
    query = update.callback_query
    
    # Obtener datos del multimedia usando message_id
    message_id = query.message.message_id
    multimedia_data = context.bot_data.get('media_messages', {}).get(message_id)
    
    if not multimedia_data:
        logger.error(f"❌ No se encontraron datos de multimedia para el mensaje {message_id}")
        await query.edit_message_caption(
            caption="❌ Error: No se encontraron datos del multimedia",
            reply_markup=None
        )
        return

    try:
        # Guardar referencia del mensaje para el conversation handler
        context.user_data['current_message_id'] = message_id
        
        # Actualizar mensaje para solicitar leyenda
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("❌ Cancelar", callback_data="cancel_caption")
        ]])
        
        await query.edit_message_caption(
            caption="📝 Envía la leyenda que quieres agregar al multimedia:",
            reply_markup=keyboard
        )

        logger.info(f"✅ Solicitando leyenda personalizada para mensaje {message_id}")

    except Exception as e:
        logger.error(f"❌ Error solicitando leyenda: {e}")
        await query.edit_message_caption(
            caption="❌ Error procesando solicitud",
            reply_markup=None
        )


async def handle_cancel_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la cancelación de la entrada de leyenda"""
    query = update.callback_query
    
    # Limpiar datos temporales
    if 'current_message_id' in context.user_data:
        del context.user_data['current_message_id']
    
    # Restaurar botones originales
    from keyboards import create_media_action_keyboard
    keyboard = create_media_action_keyboard()
    await query.edit_message_caption(
        caption=f"{MESSAGES['new_media']}\n\n{MESSAGES['choose_action']}",
        reply_markup=keyboard
    )
    
    logger.info("✅ Entrada de leyenda cancelada")


async def handle_discard_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la acción de descartar multimedia"""
    query = update.callback_query
    
    # Obtener datos del multimedia usando message_id
    message_id = query.message.message_id
    multimedia_data = context.bot_data.get('media_messages', {}).get(message_id)
    
    try:
        await query.edit_message_caption(
            caption=MESSAGES['discarded'],
            reply_markup=None
        )
        
        # Si tenemos datos del multimedia, eliminar también el mensaje original
        if multimedia_data:
            await delete_source_message(
                context,
                multimedia_data['source_chat_id'],
                multimedia_data['message_id']
            )
        
        # Limpiar datos del mensaje
        if message_id in context.bot_data.get('media_messages', {}):
            del context.bot_data['media_messages'][message_id]
        
        logger.info(f"🗑️ Multimedia descartado por el usuario (mensaje {message_id})")
        
    except Exception as e:
        logger.error(f"❌ Error descartando multimedia: {e}")
        await query.edit_message_caption(
            caption=MESSAGES['error'],
            reply_markup=None
        )


def setup_callback_handlers(app):
    """Configura el manejador de callbacks"""
    
    callback_handler = CallbackQueryHandler(handle_callback_query)
    app.add_handler(callback_handler)
    
    logger.info("✅ Manejador de callbacks configurado")