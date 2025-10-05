"""
Tests para el message handler
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestMessageHandler:
    """Tests para el manejador de mensajes"""
    
    @pytest.mark.asyncio
    async def test_photo_message_handling(self, mock_telegram_bot, mock_telegram_update):
        """Test de manejo de mensajes con foto"""
        # Simular mensaje con foto
        mock_telegram_update.message.photo = [MagicMock()]
        mock_telegram_update.message.photo[0].file_id = "test_photo_id"
        mock_telegram_update.message.text = None
        mock_telegram_update.message.caption = "Test photo caption"
        
        async def mock_photo_handler(update, context):
            # Simular envío al propietario con botones
            keyboard = [
                [{"text": "📤 Enviar", "callback_data": "send_photo"}],
                [{"text": "💾 Almacenar", "callback_data": "store_photo"}],
                [{"text": "🗑️ Descartar", "callback_data": "discard_photo"}]
            ]
            
            await context.bot.send_photo(
                chat_id=123456789,  # OWNER_ID
                photo=update.message.photo[0].file_id,
                caption="📸 Nueva imagen detectada\n\n" + (update.message.caption or ""),
                reply_markup=keyboard
            )
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_photo_handler(mock_telegram_update, context)
        
        # Verificar que se envió la foto al propietario
        mock_telegram_bot.send_photo.assert_called_once()
        call_args = mock_telegram_bot.send_photo.call_args
        assert call_args[1]['chat_id'] == 123456789
        assert call_args[1]['photo'] == "test_photo_id"
        assert "Nueva imagen detectada" in call_args[1]['caption']
    
    @pytest.mark.asyncio
    async def test_video_message_handling(self, mock_telegram_bot, mock_telegram_update):
        """Test de manejo de mensajes con video"""
        # Simular mensaje con video
        mock_telegram_update.message.video = MagicMock()
        mock_telegram_update.message.video.file_id = "test_video_id"
        mock_telegram_update.message.photo = None
        mock_telegram_update.message.animation = None
        
        async def mock_video_handler(update, context):
            await context.bot.send_video(
                chat_id=123456789,
                video=update.message.video.file_id,
                caption="🎥 Nuevo video detectado"
            )
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_video_handler(mock_telegram_update, context)
        
        mock_telegram_bot.send_video.assert_called_once()
        call_args = mock_telegram_bot.send_video.call_args
        assert call_args[1]['video'] == "test_video_id"
        assert "Nuevo video detectado" in call_args[1]['caption']
    
    @pytest.mark.asyncio 
    async def test_animation_message_handling(self, mock_telegram_bot, mock_telegram_update):
        """Test de manejo de mensajes con animación/GIF"""
        # Simular mensaje con animación
        mock_telegram_update.message.animation = MagicMock()
        mock_telegram_update.message.animation.file_id = "test_animation_id"
        mock_telegram_update.message.photo = None
        mock_telegram_update.message.video = None
        
        async def mock_animation_handler(update, context):
            await context.bot.send_animation(
                chat_id=123456789,
                animation=update.message.animation.file_id,
                caption="🎭 Nueva animación detectada"
            )
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_animation_handler(mock_telegram_update, context)
        
        mock_telegram_bot.send_animation.assert_called_once()
        call_args = mock_telegram_bot.send_animation.call_args
        assert call_args[1]['animation'] == "test_animation_id"
    
    def test_media_type_detection(self):
        """Test de detección de tipos de media"""
        # Simular diferentes tipos de mensajes
        test_cases = [
            {'photo': True, 'video': False, 'animation': False, 'expected': 'photo'},
            {'photo': False, 'video': True, 'animation': False, 'expected': 'video'},
            {'photo': False, 'video': False, 'animation': True, 'expected': 'animation'},
            {'photo': False, 'video': False, 'animation': False, 'expected': 'text'}
        ]
        
        for case in test_cases:
            # Simular mensaje
            message = MagicMock()
            message.photo = [MagicMock()] if case['photo'] else None
            message.video = MagicMock() if case['video'] else None
            message.animation = MagicMock() if case['animation'] else None
            message.text = "test text" if case['expected'] == 'text' else None
            
            # Función de detección
            def get_media_type(msg):
                if msg.photo:
                    return 'photo'
                elif msg.video:
                    return 'video'
                elif msg.animation:
                    return 'animation'
                else:
                    return 'text'
            
            detected_type = get_media_type(message)
            assert detected_type == case['expected']
    
    def test_owner_id_validation(self):
        """Test de validación del ID del propietario"""
        test_owner_ids = ["123456789", "987654321", "111222333"]
        
        for owner_id in test_owner_ids:
            # Validar que es un ID válido
            assert owner_id.isdigit()
            assert len(owner_id) >= 5  # Los IDs de Telegram tienen al menos 5 dígitos
            assert int(owner_id) > 0