"""
Tests para utilidades de media
"""
import pytest
from unittest.mock import MagicMock

class TestMediaUtils:
    """Tests para utilidades de media"""
    
    def test_get_media_type(self):
        """Test de detección de tipo de media"""
        def get_media_type(message):
            """Función para detectar tipo de media"""
            if hasattr(message, 'photo') and message.photo:
                return 'photo'
            elif hasattr(message, 'video') and message.video:
                return 'video'
            elif hasattr(message, 'animation') and message.animation:
                return 'animation'
            elif hasattr(message, 'document') and message.document:
                return 'document'
            else:
                return 'text'
        
        # Test con foto
        photo_message = MagicMock()
        photo_message.photo = [MagicMock()]
        photo_message.video = None
        photo_message.animation = None
        assert get_media_type(photo_message) == 'photo'
        
        # Test con video
        video_message = MagicMock()
        video_message.photo = None
        video_message.video = MagicMock()
        video_message.animation = None
        assert get_media_type(video_message) == 'video'
        
        # Test con animación
        animation_message = MagicMock()
        animation_message.photo = None
        animation_message.video = None
        animation_message.animation = MagicMock()
        assert get_media_type(animation_message) == 'animation'
    
    def test_format_spoiler_text(self):
        """Test de formateo de texto con spoiler"""
        def format_spoiler_text(text, media_type=''):
            """Formatear texto con spoiler para Telegram"""
            if not text:
                text = f"📱 {media_type.title()} compartido"
            
            # Formato MarkdownV2 para spoiler
            return f"||{text}||"
        
        # Test con texto normal
        result = format_spoiler_text("Texto de prueba", "photo")
        assert result == "||Texto de prueba||"
        
        # Test sin texto
        result = format_spoiler_text("", "video")
        assert result == "||📱 Video compartido||"
        
        # Test con texto None
        result = format_spoiler_text(None, "animation")
        assert result == "||📱 Animation compartido||"
    
    def test_get_file_id(self):
        """Test de extracción de file_id"""
        def get_file_id(message):
            """Extraer file_id según el tipo de media"""
            if message.photo:
                # Para fotos, tomar la de mayor resolución
                return message.photo[-1].file_id
            elif message.video:
                return message.video.file_id
            elif message.animation:
                return message.animation.file_id
            elif message.document:
                return message.document.file_id
            return None
        
        # Test con foto (múltiples tamaños)
        photo_message = MagicMock()
        photo_message.photo = [
            MagicMock(file_id="photo_small"),
            MagicMock(file_id="photo_medium"),
            MagicMock(file_id="photo_large")
        ]
        photo_message.video = None
        photo_message.animation = None
        assert get_file_id(photo_message) == "photo_large"
        
        # Test con video
        video_message = MagicMock()
        video_message.photo = None
        video_message.video = MagicMock(file_id="video_id")
        video_message.animation = None
        assert get_file_id(video_message) == "video_id"
    
    def test_validate_chat_id(self):
        """Test de validación de IDs de chat"""
        def validate_chat_id(chat_id):
            """Validar formato de ID de chat"""
            if isinstance(chat_id, str):
                chat_id = chat_id.strip()
                
                # Debe ser numérico (incluyendo negativos)
                if chat_id.startswith('-'):
                    return chat_id[1:].isdigit()
                else:
                    return chat_id.isdigit()
            
            return isinstance(chat_id, int)
        
        # Test con IDs válidos
        valid_ids = ["123456789", "-1001234567890", "-123456789", 123456789, -1001234567890]
        for chat_id in valid_ids:
            assert validate_chat_id(chat_id) == True
        
        # Test con IDs inválidos
        invalid_ids = ["abc123", "123abc", "", "  ", None]
        for chat_id in invalid_ids:
            assert validate_chat_id(chat_id) == False
    
    def test_create_keyboard(self):
        """Test de creación de teclados inline"""
        def create_keyboard(media_type):
            """Crear teclado inline según el tipo de media"""
            buttons = [
                [{"text": f"📤 Enviar {media_type}", "callback_data": f"send_{media_type}"}],
                [{"text": f"📝 Enviar con leyenda", "callback_data": f"caption_{media_type}"}],
                [{"text": f"💾 Almacenar", "callback_data": f"store_{media_type}"}],
                [{"text": f"🗑️ Descartar", "callback_data": f"discard_{media_type}"}]
            ]
            return buttons
        
        # Test para foto
        keyboard = create_keyboard("photo")
        assert len(keyboard) == 4  # 4 filas de botones
        assert keyboard[0][0]["text"] == "📤 Enviar photo"
        assert keyboard[0][0]["callback_data"] == "send_photo"
        
        # Test para video
        keyboard = create_keyboard("video")
        assert keyboard[2][0]["callback_data"] == "store_video"
        
    def test_escape_markdown(self):
        """Test de escape de caracteres especiales para Markdown"""
        def escape_markdown_v2(text):
            """Escapar caracteres especiales para MarkdownV2"""
            if not text:
                return ""
            
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            escaped_text = text
            
            for char in special_chars:
                escaped_text = escaped_text.replace(char, f'\\{char}')
            
            return escaped_text
        
        # Test con texto normal
        result = escape_markdown_v2("Texto normal")
        assert result == "Texto normal"
        
        # Test con caracteres especiales
        result = escape_markdown_v2("Texto con * y _ especiales")
        assert result == "Texto con \\* y \\_ especiales"
        
        # Test con texto vacío/None
        assert escape_markdown_v2("") == ""
        assert escape_markdown_v2(None) == ""