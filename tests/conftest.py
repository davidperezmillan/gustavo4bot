"""
Configuración global para pytest
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
import os

@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_telegram_bot():
    """Mock del bot de Telegram"""
    bot = AsyncMock()
    bot.send_message = AsyncMock()
    bot.send_photo = AsyncMock()
    bot.send_video = AsyncMock()
    bot.send_animation = AsyncMock()
    bot.edit_message_text = AsyncMock()
    bot.edit_message_reply_markup = AsyncMock()
    bot.delete_message = AsyncMock()
    return bot

@pytest.fixture
def mock_telegram_update():
    """Mock de un update de Telegram"""
    update = MagicMock()
    update.message = MagicMock()
    update.message.message_id = 123
    update.message.chat = MagicMock()
    update.message.chat.id = 456
    update.message.from_user = MagicMock()
    update.message.from_user.id = 789
    update.message.text = "test message"
    update.callback_query = None
    return update

@pytest.fixture
def mock_callback_query():
    """Mock de callback query"""
    callback = MagicMock()
    callback.id = "test_callback_id"
    callback.from_user = MagicMock()
    callback.from_user.id = 789
    callback.message = MagicMock()
    callback.message.message_id = 123
    callback.message.chat = MagicMock()
    callback.message.chat.id = 456
    callback.data = "test_data"
    callback.answer = AsyncMock()
    return callback

@pytest.fixture
def test_config():
    """Configuración de test desde variables de entorno"""
    return {
        'TELEGRAM_TOKEN': os.environ.get('TELEGRAM_TOKEN', 'test_token'),
        'OWNER_ID': os.environ.get('OWNER_ID', '123456789'),
        'CHAT_SOURCE_ID': os.environ.get('CHAT_SOURCE_ID', '-1001234567890'),
        'PUBLISH_CHANNEL_ID': os.environ.get('PUBLISH_CHANNEL_ID', '-1001234567891'),
        'STORAGE_CHANNEL_ID': os.environ.get('STORAGE_CHANNEL_ID', '-1001234567892'),
        'LOG_LEVEL': os.environ.get('LOG_LEVEL', 'DEBUG')
    }