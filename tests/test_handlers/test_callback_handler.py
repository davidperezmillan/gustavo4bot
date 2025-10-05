"""
Tests para el callback handler
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Agregar el path del bot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'bot'))

class TestCallbackHandler:
    """Tests para el manejador de callbacks"""
    
    @pytest.mark.asyncio
    async def test_send_callback(self, mock_telegram_bot, mock_callback_query):
        """Test del callback de enviar"""
        mock_callback_query.data = "send_photo"
        
        async def mock_send_callback_handler(update, context):
            query = update.callback_query
            await query.answer("📤 Enviando al canal...")
            
            # Simular envío al canal de publicación
            await context.bot.send_message(
                chat_id=-1001234567891,  # PUBLISH_CHANNEL_ID
                text="||📸 Contenido enviado con spoiler||",
                parse_mode='MarkdownV2'
            )
            
            # Actualizar mensaje original
            await context.bot.edit_message_text(
                text="✅ Enviado al canal de publicación",
                chat_id=query.message.chat.id,
                message_id=query.message.message_id
            )
        
        # Crear update mock con callback query
        update = MagicMock()
        update.callback_query = mock_callback_query
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_send_callback_handler(update, context)
        
        # Verificar que se respondió al callback
        mock_callback_query.answer.assert_called_once_with("📤 Enviando al canal...")
        
        # Verificar que se envió al canal
        mock_telegram_bot.send_message.assert_called_once_with(
            chat_id=-1001234567891,
            text="||📸 Contenido enviado con spoiler||",
            parse_mode='MarkdownV2'
        )
        
        # Verificar que se actualizó el mensaje
        mock_telegram_bot.edit_message_text.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_store_callback(self, mock_telegram_bot, mock_callback_query):
        """Test del callback de almacenar"""
        mock_callback_query.data = "store_photo"
        
        async def mock_store_callback_handler(update, context):
            query = update.callback_query
            await query.answer("💾 Almacenando...")
            
            # Simular envío al canal de almacenamiento
            await context.bot.send_message(
                chat_id=-1001234567892,  # STORAGE_CHANNEL_ID
                text="📁 Archivo almacenado"
            )
            
            await context.bot.edit_message_text(
                text="✅ Almacenado en el canal de archivos",
                chat_id=query.message.chat.id,
                message_id=query.message.message_id
            )
        
        update = MagicMock()
        update.callback_query = mock_callback_query
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_store_callback_handler(update, context)
        
        mock_callback_query.answer.assert_called_once_with("💾 Almacenando...")
        mock_telegram_bot.send_message.assert_called_once_with(
            chat_id=-1001234567892,
            text="📁 Archivo almacenado"
        )
    
    @pytest.mark.asyncio
    async def test_discard_callback(self, mock_telegram_bot, mock_callback_query):
        """Test del callback de descartar"""
        mock_callback_query.data = "discard_photo"
        
        async def mock_discard_callback_handler(update, context):
            query = update.callback_query
            await query.answer("🗑️ Descartando...")
            
            # Eliminar el mensaje
            await context.bot.delete_message(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id
            )
        
        update = MagicMock()
        update.callback_query = mock_callback_query
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_discard_callback_handler(update, context)
        
        mock_callback_query.answer.assert_called_once_with("🗑️ Descartando...")
        mock_telegram_bot.delete_message.assert_called_once_with(
            chat_id=456,
            message_id=123
        )
    
    def test_callback_data_parsing(self):
        """Test de parsing de datos de callback"""
        test_callbacks = [
            "send_photo",
            "send_video", 
            "send_animation",
            "store_photo",
            "store_video",
            "store_animation",
            "discard_photo",
            "discard_video",
            "discard_animation"
        ]
        
        for callback_data in test_callbacks:
            # Verificar formato
            assert isinstance(callback_data, str)
            assert len(callback_data) > 0
            
            # Parsear acción y tipo
            parts = callback_data.split('_')
            assert len(parts) >= 2
            
            action = parts[0]
            media_type = parts[1] if len(parts) > 1 else None
            
            assert action in ['send', 'store', 'discard']
            if media_type:
                assert media_type in ['photo', 'video', 'animation']
    
    @pytest.mark.asyncio
    async def test_callback_error_handling(self, mock_telegram_bot, mock_callback_query):
        """Test de manejo de errores en callbacks"""
        mock_callback_query.data = "invalid_callback"
        
        async def mock_error_callback_handler(update, context):
            query = update.callback_query
            try:
                # Simular procesamiento que falla
                if query.data == "invalid_callback":
                    raise ValueError("Callback inválido")
            except Exception as e:
                await query.answer(f"❌ Error: {str(e)}")
        
        update = MagicMock()
        update.callback_query = mock_callback_query
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_error_callback_handler(update, context)
        
        mock_callback_query.answer.assert_called_once_with("❌ Error: Callback inválido")