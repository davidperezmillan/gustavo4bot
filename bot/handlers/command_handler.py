from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import OWNER_ID, logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /start - Muestra información básica del bot
    """
    try:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        if user_id == OWNER_ID:
            message = (
                "🤖 **Gustavo4Bot - Panel de Propietario**\n\n"
                "**Comandos disponibles:**\n"
                "• `/start` - Mostrar este mensaje\n"
                "• `/id` - Obtener ID de este chat\n"
                "• `/status` - Ver estado del bot\n\n"
                "📋 **Funcionamiento:**\n"
                "El bot monitorea el chat fuente configurado y te reenviará "
                "automáticamente las imágenes, videos y animaciones para que "
                "puedas decidir qué hacer con ellos."
            )
        else:
            message = (
                "🤖 **Gustavo4Bot**\n\n"
                "Bot privado para gestión de multimedia.\n"
                "Usa `/id` para obtener el ID de este chat."
            )
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"👋 Comando /start ejecutado por usuario {user_id} en chat {chat_id}")
        
    except Exception as e:
        logger.error(f"❌ Error en comando /start: {e}")

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /id - Devuelve información del chat actual
    """
    try:
        chat = update.effective_chat
        user = update.effective_user
        
        # Información básica del chat
        chat_info = f"🆔 **ID del Chat:** `{chat.id}`\n"
        chat_info += f"👤 **Tu ID:** `{user.id}`\n"
        
        # Información adicional según el tipo de chat
        if chat.type == 'private':
            chat_info += "📱 **Tipo:** Chat privado\n"
            chat_info += f"👤 **Usuario:** {user.first_name}"
            if user.last_name:
                chat_info += f" {user.last_name}"
            if user.username:
                chat_info += f" (@{user.username})"
                
        elif chat.type == 'group':
            chat_info += "👥 **Tipo:** Grupo\n"
            chat_info += f"📝 **Nombre:** {chat.title}\n"
            member_count = await context.bot.get_chat_member_count(chat.id)
            chat_info += f"👥 **Miembros:** {member_count}"
            
        elif chat.type == 'supergroup':
            chat_info += "👥 **Tipo:** Supergrupo\n"
            chat_info += f"📝 **Nombre:** {chat.title}\n"
            if chat.username:
                chat_info += f"🔗 **Username:** @{chat.username}\n"
            try:
                member_count = await context.bot.get_chat_member_count(chat.id)
                chat_info += f"👥 **Miembros:** {member_count}"
            except:
                chat_info += "👥 **Miembros:** No disponible"
                
        elif chat.type == 'channel':
            chat_info += "📢 **Tipo:** Canal\n"
            chat_info += f"📝 **Nombre:** {chat.title}\n"
            if chat.username:
                chat_info += f"🔗 **Username:** @{chat.username}\n"
            try:
                member_count = await context.bot.get_chat_member_count(chat.id)
                chat_info += f"👥 **Suscriptores:** {member_count}"
            except:
                chat_info += "👥 **Suscriptores:** No disponible"
        
        # Información adicional para el propietario
        if user.id == OWNER_ID:
            chat_info += "\n\n🔧 **Para configurar el bot:**\n"
            chat_info += f"Usa este ID `{chat.id}` en las variables de entorno:\n"
            if chat.type == 'private':
                chat_info += "• `OWNER_ID` (ya configurado)\n"
            else:
                chat_info += "• `CHAT_SOURCE_ID` (chat fuente)\n"
                chat_info += "• `PUBLISH_CHANNEL_ID` (canal publicación)\n"
                chat_info += "• `STORAGE_CHANNEL_ID` (canal almacenamiento)"
        
        await update.message.reply_text(chat_info, parse_mode='Markdown')
        logger.info(f"🆔 Comando /id ejecutado por usuario {user.id} en chat {chat.id} ({chat.type})")
        
    except Exception as e:
        logger.error(f"❌ Error en comando /id: {e}")
        await update.message.reply_text(
            "❌ Error al obtener información del chat.",
            parse_mode='Markdown'
        )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /status - Muestra el estado del bot (solo para el propietario)
    """
    try:
        user_id = update.effective_user.id
        
        if user_id != OWNER_ID:
            await update.message.reply_text("❌ Este comando solo está disponible para el propietario.")
            return
        
        # Información de configuración
        from config import CHAT_SOURCE_ID, PUBLISH_CHANNEL_ID, STORAGE_CHANNEL_ID
        
        status_info = "🤖 **Estado de Gustavo4Bot**\n\n"
        status_info += "⚙️ **Configuración:**\n"
        status_info += f"• Chat fuente: `{CHAT_SOURCE_ID}`\n"
        status_info += f"• Canal publicación: `{PUBLISH_CHANNEL_ID}`\n"
        status_info += f"• Canal almacenamiento: `{STORAGE_CHANNEL_ID}`\n"
        status_info += f"• Propietario: `{OWNER_ID}`\n\n"
        status_info += "✅ **Estado:** Bot funcionando correctamente\n"
        status_info += "🔄 **Monitoreo:** Activo en chat fuente"
        
        await update.message.reply_text(status_info, parse_mode='Markdown')
        logger.info(f"📊 Comando /status ejecutado por propietario {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Error en comando /status: {e}")

def setup_command_handlers(app):
    """Configura todos los manejadores de comandos"""
    
    # Comando /start
    start_handler = CommandHandler('start', start_command)
    app.add_handler(start_handler)
    
    # Comando /id
    id_handler = CommandHandler('id', id_command)
    app.add_handler(id_handler)
    
    # Comando /status (solo propietario)
    status_handler = CommandHandler('status', status_command)
    app.add_handler(status_handler)
    
    logger.info("✅ Manejadores de comandos configurados")