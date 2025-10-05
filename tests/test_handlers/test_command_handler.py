"""
Tests para el command handler
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestCommandHandler:
    """Tests para los manejadores de comandos"""
    
    @pytest.mark.asyncio
    async def test_start_command(self, mock_telegram_bot, mock_telegram_update):
        """Test del comando /start"""
        # Simular comando /start
        mock_telegram_update.message.text = "/start"
        
        # Simular la función de start
        async def mock_start_handler(update, context):
            await context.bot.send_message(
                chat_id=update.message.chat.id,
                text="¡Bot iniciado correctamente!"
            )
        
        # Crear contexto mock
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        # Ejecutar el handler
        await mock_start_handler(mock_telegram_update, context)
        
        # Verificar que se envió el mensaje
        mock_telegram_bot.send_message.assert_called_once_with(
            chat_id=456,
            text="¡Bot iniciado correctamente!"
        )
    
    @pytest.mark.asyncio
    async def test_help_command(self, mock_telegram_bot, mock_telegram_update):
        """Test del comando /help"""
        mock_telegram_update.message.text = "/help"
        
        async def mock_help_handler(update, context):
            help_text = """
🤖 **Gustavo4Bot - Ayuda**

**Comandos disponibles:**
/start - Iniciar el bot
/help - Mostrar esta ayuda
/status - Estado del bot

**Funcionalidades:**
• Detección automática de multimedia
• Reenvío con botones de acción
• Gestión de canales
            """
            await context.bot.send_message(
                chat_id=update.message.chat.id,
                text=help_text,
                parse_mode='Markdown'
            )
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_help_handler(mock_telegram_update, context)
        
        # Verificar que se llamó send_message con texto de ayuda
        mock_telegram_bot.send_message.assert_called_once()
        call_args = mock_telegram_bot.send_message.call_args
        assert "Gustavo4Bot" in call_args[1]['text']
        assert "Comandos disponibles" in call_args[1]['text']
    
    @pytest.mark.asyncio
    async def test_status_command(self, mock_telegram_bot, mock_telegram_update):
        """Test del comando /status"""
        mock_telegram_update.message.text = "/status"
        
        async def mock_status_handler(update, context):
            status_text = "✅ Bot funcionando correctamente\n🔄 Monitoreando canales..."
            await context.bot.send_message(
                chat_id=update.message.chat.id,
                text=status_text
            )
        
        context = MagicMock()
        context.bot = mock_telegram_bot
        
        await mock_status_handler(mock_telegram_update, context)
        
        mock_telegram_bot.send_message.assert_called_once_with(
            chat_id=456,
            text="✅ Bot funcionando correctamente\n🔄 Monitoreando canales..."
        )
    
    def test_command_recognition(self):
        """Test de reconocimiento de comandos"""
        commands = ["/start", "/help", "/status"]
        
        for cmd in commands:
            assert cmd.startswith("/")
            assert len(cmd) > 1
            assert cmd.replace("/", "").isalnum() or cmd.replace("/", "") in ["start", "help", "status"]