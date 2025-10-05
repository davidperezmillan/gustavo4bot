from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_media_action_keyboard():
    """
    Crea el teclado inline con las opciones para procesar multimedia
    
    Returns:
        InlineKeyboardMarkup: Teclado con los botones de acción
    """
    keyboard = [
        [
            InlineKeyboardButton("📤 Enviar", callback_data="action_send"),
            InlineKeyboardButton("📝 Enviar con leyenda", callback_data="action_send_caption")
        ],
        [
            InlineKeyboardButton("📁 Almacenar", callback_data="action_store"),
            InlineKeyboardButton("🗑️ Descartar", callback_data="action_discard")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def create_cancel_keyboard():
    """
    Crea un teclado simple con botón de cancelar
    
    Returns:
        InlineKeyboardMarkup: Teclado con botón cancelar
    """
    keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data="action_cancel")]]
    return InlineKeyboardMarkup(keyboard)