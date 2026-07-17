from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Xizmatlar")],
        [KeyboardButton(text="📦 Buyurtma"), KeyboardButton(text="💰 Balans")],
        [KeyboardButton(text="📋 Buyurtmalarim")],
        [KeyboardButton(text="➕ Hisobni to'ldirish")],
        [KeyboardButton(text="📞 Admin")]
    ],
    resize_keyboard=True
)
