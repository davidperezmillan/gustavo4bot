# handlers/__init__.py
# Paquete de manejadores del bot

from .command_handler import setup_command_handlers
from .message_handler import setup_message_handlers
from .callback_handler import setup_callback_handlers
from .conversation_handler import setup_conversation_handlers

__all__ = [
    'setup_command_handlers',
    'setup_message_handlers', 
    'setup_callback_handlers',
    'setup_conversation_handlers'
]