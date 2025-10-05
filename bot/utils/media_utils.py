import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config import PUBLISH_CHANNEL_ID, STORAGE_CHANNEL_ID, OWNER_ID, MESSAGES, logger
from keyboards import create_media_action_keyboard

async def forward_media_to_owner(context, media_type: str, file_id: str, owner_id: int, media_data: dict):
    """
    Reenvía multimedia al propietario con botones de acción
    
    Args:
        context: Contexto de Telegram
        media_type: Tipo de multimedia (photo, video, animation)
        file_id: ID del archivo
        owner_id: ID del propietario
        media_data: Datos del multimedia para asociar con el mensaje
    
    Returns:
        Message: El mensaje enviado o None si hay error
    """
    try:
        bot = context.bot
        keyboard = create_media_action_keyboard()
        
        # Enviar multimedia según el tipo
        if media_type == "photo":
            sent_message = await bot.send_photo(
                chat_id=owner_id,
                photo=file_id,
                caption=f"{MESSAGES['new_media']}\n\n{MESSAGES['choose_action']}",
                reply_markup=keyboard
            )
        elif media_type == "video":
            sent_message = await bot.send_video(
                chat_id=owner_id,
                video=file_id,
                caption=f"{MESSAGES['new_media']}\n\n{MESSAGES['choose_action']}",
                reply_markup=keyboard
            )
        elif media_type == "animation":
            sent_message = await bot.send_animation(
                chat_id=owner_id,
                animation=file_id,
                caption=f"{MESSAGES['new_media']}\n\n{MESSAGES['choose_action']}",
                reply_markup=keyboard
            )
        else:
            return None
        
        # Asociar este mensaje con su multimedia específica
        if not hasattr(context, 'bot_data'):
            context.bot_data = {}
        if 'media_messages' not in context.bot_data:
            context.bot_data['media_messages'] = {}
            
        context.bot_data['media_messages'][sent_message.message_id] = media_data
        
        logger.info(f"✅ Multimedia {media_type} reenviada al propietario (msg_id: {sent_message.message_id})")
        return sent_message
        
    except TelegramError as e:
        logger.error(f"❌ Error reenviando multimedia al propietario: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Error inesperado reenviando multimedia: {e}")
        return None

async def send_media_with_spoiler(context, media_data: dict, caption: str = None):
    """
    Envía multimedia al canal con spoiler
    
    Args:
        context: Contexto de Telegram
        media_data: Datos del multimedia
        caption: Leyenda opcional
    
    Returns:
        bool: True si se envió correctamente
    """
    try:
        bot = context.bot
        media_type = media_data['type']
        file_id = media_data['file_id']
        
        # Preparar caption con spoiler si se proporciona
        spoiler_caption = f"||{caption}||" if caption else None
        
        # Enviar según el tipo de multimedia
        if media_type == "photo":
            await bot.send_photo(
                chat_id=PUBLISH_CHANNEL_ID,
                photo=file_id,
                caption=spoiler_caption,
                has_spoiler=True
            )
        elif media_type == "video":
            await bot.send_video(
                chat_id=PUBLISH_CHANNEL_ID,
                video=file_id,
                caption=spoiler_caption,
                has_spoiler=True
            )
        elif media_type == "animation":
            await bot.send_animation(
                chat_id=PUBLISH_CHANNEL_ID,
                animation=file_id,
                caption=spoiler_caption,
                has_spoiler=True
            )
        
        logger.info(f"✅ {media_type} enviado al canal con spoiler")
        return True
        
    except TelegramError as e:
        logger.error(f"❌ Error enviando multimedia al canal: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado enviando multimedia: {e}")
        return False

async def send_media_to_storage(context, media_data: dict):
    """
    Envía multimedia al canal de almacenamiento
    
    Args:
        context: Contexto de Telegram
        media_data: Datos del multimedia
    
    Returns:
        bool: True si se almacenó correctamente
    """
    try:
        bot = context.bot
        media_type = media_data['type']
        file_id = media_data['file_id']
        
        # Enviar según el tipo de multimedia (sin caption)
        if media_type == "photo":
            await bot.send_photo(
                chat_id=STORAGE_CHANNEL_ID,
                photo=file_id
            )
        elif media_type == "video":
            await bot.send_video(
                chat_id=STORAGE_CHANNEL_ID,
                video=file_id
            )
        elif media_type == "animation":
            await bot.send_animation(
                chat_id=STORAGE_CHANNEL_ID,
                animation=file_id
            )
        
        logger.info(f"✅ {media_type} almacenado en el canal de archivos")
        return True
        
    except TelegramError as e:
        logger.error(f"❌ Error almacenando multimedia: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado almacenando multimedia: {e}")
        return False

async def store_multimedia(context, source_chat_id: int, message_id: int, file_id: str, media_type: str, caption: str = '', has_spoiler: bool = False):
    """
    Almacena multimedia en el canal correspondiente según el parámetro has_spoiler
    y elimina el mensaje original del chat fuente
    
    Args:
        context: Contexto de Telegram
        source_chat_id: ID del chat fuente
        message_id: ID del mensaje original
        file_id: ID del archivo de multimedia
        media_type: Tipo de multimedia (photo, video, animation)
        caption: Caption del multimedia
        has_spoiler: Si debe enviarse con spoiler al canal de publicación
    
    Returns:
        bool: True si se procesó correctamente
    """
    try:
        # Crear estructura de datos
        media_data = {
            'type': media_type,
            'file_id': file_id,
            'original_message_id': message_id,
            'source_chat_id': source_chat_id,
            'caption': caption
        }
        
        success = False
        if has_spoiler:
            # Enviar con spoiler al canal de publicación
            success = await send_media_with_spoiler(context, media_data, caption)
        else:
            # Almacenar en el canal de archivos
            success = await send_media_to_storage(context, media_data)
        
        # Si se procesó correctamente, eliminar el mensaje original del chat fuente
        if success:
            await delete_source_message(context, source_chat_id, message_id)
            
        return success
            
    except Exception as e:
        logger.error(f"❌ Error en store_multimedia: {e}")
        return False

async def delete_bot_message(context, message_id: int, delay: int = 3):
    """
    Elimina un mensaje del bot después de un delay
    
    Args:
        context: Contexto de Telegram
        message_id: ID del mensaje a eliminar
        delay: Segundos de delay antes de eliminar
    """
    try:
        await asyncio.sleep(delay)
        await context.bot.delete_message(
            chat_id=OWNER_ID,
            message_id=message_id
        )
        logger.debug(f"🗑️ Mensaje {message_id} eliminado")
        
    except TelegramError as e:
        logger.warning(f"⚠️ No se pudo eliminar el mensaje {message_id}: {e}")
    except Exception as e:
        logger.error(f"❌ Error eliminando mensaje: {e}")


async def delete_source_message(context, source_chat_id: int, message_id: int):
    """
    Elimina un mensaje del chat fuente después de procesarlo
    
    Args:
        context: Contexto de Telegram
        source_chat_id: ID del chat fuente
        message_id: ID del mensaje a eliminar
    """
    try:
        await context.bot.delete_message(
            chat_id=source_chat_id,
            message_id=message_id
        )
        logger.info(f"🗑️ Mensaje original eliminado del chat fuente (chat: {source_chat_id}, msg: {message_id})")
        
    except TelegramError as e:
        logger.warning(f"⚠️ No se pudo eliminar el mensaje original del chat fuente: {e}")
    except Exception as e:
        logger.error(f"❌ Error eliminando mensaje del chat fuente: {e}")