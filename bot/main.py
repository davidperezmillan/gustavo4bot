#!/usr/bin/env python3
"""
Gustavo4Bot - Bot de Telegram para gestión de multimedia
Recupera imágenes, videos y animaciones de un chat específico
y las envía al propietario para procesamiento con botones de acción.
"""

import asyncio
import logging
import nest_asyncio
from telegram.ext import ApplicationBuilder
from config import TELEGRAM_TOKEN, logger
from handlers.command_handler import setup_command_handlers
from handlers.message_handler import setup_message_handlers
from handlers.callback_handler import setup_callback_handlers
from handlers.conversation_handler import setup_conversation_handlers

# Permitir bucles de eventos anidados
nest_asyncio.apply()

async def main():
    """Función principal del bot"""
    logger.info("🚀 Iniciando Gustavo4Bot...")
    
    try:
        # Crear la aplicación del bot
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        
        # Configurar todos los manejadores
        setup_command_handlers(app)
        setup_message_handlers(app)
        setup_callback_handlers(app)
        setup_conversation_handlers(app)
        
        logger.info("✅ Bot configurado correctamente")
        logger.info("🔄 Iniciando polling...")
        
        # Ejecutar el bot
        await app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"❌ Error crítico en el bot: {e}")
        raise
    finally:
        logger.info("🛑 Bot finalizado")

def run_bot():
    """Función para ejecutar el bot de forma segura"""
    try:
        # Obtener o crear un bucle de eventos
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Si ya hay un bucle ejecutándose, crear una tarea
                task = loop.create_task(main())
                loop.run_until_complete(task)
            else:
                # Si no hay bucle ejecutándose, ejecutar normalmente
                loop.run_until_complete(main())
        except RuntimeError:
            # Si hay problemas con el bucle, crear uno nuevo
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    run_bot()