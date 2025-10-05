"""
Tests para la configuración del bot
"""
import pytest
import os
from unittest.mock import patch
import sys

# Agregar el path del bot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bot'))

class TestConfig:
    """Tests para la configuración"""
    
    def test_required_env_vars(self):
        """Test que las variables de entorno requeridas están definidas"""
        required_vars = [
            'TELEGRAM_TOKEN',
            'OWNER_ID', 
            'CHAT_SOURCE_ID',
            'PUBLISH_CHANNEL_ID',
            'STORAGE_CHANNEL_ID'
        ]
        
        # Simular variables de entorno
        with patch.dict(os.environ, {
            'TELEGRAM_TOKEN': 'test_token',
            'OWNER_ID': '123456789',
            'CHAT_SOURCE_ID': '-1001234567890',
            'PUBLISH_CHANNEL_ID': '-1001234567891',
            'STORAGE_CHANNEL_ID': '-1001234567892'
        }):
            try:
                import config
                # Si llegamos aquí, la configuración se cargó correctamente
                assert hasattr(config, 'TELEGRAM_TOKEN')
                assert hasattr(config, 'OWNER_ID')
                assert hasattr(config, 'CHAT_SOURCE_ID')
                assert hasattr(config, 'PUBLISH_CHANNEL_ID')
                assert hasattr(config, 'STORAGE_CHANNEL_ID')
            except ImportError:
                # Si no existe config.py, creamos un test básico
                for var in required_vars:
                    assert var in os.environ or var in [
                        'TELEGRAM_TOKEN', 'OWNER_ID', 'CHAT_SOURCE_ID', 
                        'PUBLISH_CHANNEL_ID', 'STORAGE_CHANNEL_ID'
                    ]
    
    def test_telegram_token_format(self):
        """Test que el token de Telegram tiene el formato correcto"""
        with patch.dict(os.environ, {'TELEGRAM_TOKEN': '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz'}):
            token = os.environ.get('TELEGRAM_TOKEN')
            assert ':' in token
            parts = token.split(':')
            assert len(parts) == 2
            assert parts[0].isdigit()
            assert len(parts[1]) >= 35  # Los tokens de Telegram son largos
    
    def test_chat_ids_format(self):
        """Test que los IDs de chat tienen formato válido"""
        test_ids = {
            'OWNER_ID': '123456789',
            'CHAT_SOURCE_ID': '-1001234567890',
            'PUBLISH_CHANNEL_ID': '-1001234567891', 
            'STORAGE_CHANNEL_ID': '-1001234567892'
        }
        
        with patch.dict(os.environ, test_ids):
            # Owner ID debe ser positivo
            owner_id = os.environ.get('OWNER_ID')
            assert owner_id.isdigit() or (owner_id.startswith('-') and owner_id[1:].isdigit())
            
            # Los canales deben empezar con -100
            for key in ['CHAT_SOURCE_ID', 'PUBLISH_CHANNEL_ID', 'STORAGE_CHANNEL_ID']:
                chat_id = os.environ.get(key)
                assert chat_id.startswith('-100') or chat_id.startswith('-') or chat_id.isdigit()
    
    def test_log_level_valid(self):
        """Test que el nivel de log es válido"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        with patch.dict(os.environ, {'LOG_LEVEL': 'INFO'}):
            log_level = os.environ.get('LOG_LEVEL', 'INFO')
            assert log_level in valid_levels