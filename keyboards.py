from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import CHANNEL_1, CHANNEL_2


# ==========================
# ASOSIY MENU
# ==========================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💡 Xizmatlar"),
            KeyboardButton(text="🛒 Buyurtmalar"),
        ],
        [
            KeyboardButton(text="💰 Balans"),
            KeyboardButton(text="🗣️ Referal"),
        ],
        [
            KeyboardButton(text="💳 To'lov"),
            KeyboardButton(text="📔 Qo'llanma"),
        ],
        [
            KeyboardButton(text="☎️ Qo'llab Quvvatlash"),
        ],
    ],
    resize_keyboard=True,
)


# ==========================
# OBUNA TEKSHIRISH
# ==========================

subscribe_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Moon - SMM | News",
                url=f"https://t.me/{CHANNEL_1.replace('@','')}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Shaxsiy Kanal",
                url=f"https://t.me/{CHANNEL_2.replace('@','')}"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Tekshirish",
                callback_data="check_sub"
            )
        ],
    ]
)


# ==========================
# XIZMATLAR
# ==========================

services_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔵 Telegram",
                callback_data="telegram"
            ),
            InlineKeyboardButton(
                text="🟣 Instagram",
                callback_data="instagram"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔴 YouTube",
                callback_data="youtube"
            ),
            InlineKeyboardButton(
                text="⚫️ TikTok",
                callback_data="tiktok"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⭐️ Stars or Premium",
                callback_data="stars"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back_menu"
            ),
        ],
    ]
)


# ==========================
# BALANS
# ==========================

balance_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎁 Chegirma olish",
                callback_data="discount"
            ),
        ],
    ]
)


# ==========================
# TO'LOV
# ==========================

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🟡 HumoCard",
                callback_data="humocard"
            ),
        ],
        [
            InlineKeyboardButton(
                text="☎️ Adminga murojaat",
                url="https://t.me/khosimov_abu"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back_menu"
            ),
        ],
    ]
)


# ==========================
# HUMOCARD
# ==========================

humocard_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ To'lov qildim",
                callback_data="payment_done"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="payment_back"
            ),
        ],
    ]
)


# ==========================
# REFERAL
# ==========================

referal_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📤 Referal havolani ulash",
                switch_inline_query=""
            ),
        ],
    ]
)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


payment_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash",
                callback_data="approve_payment"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Rad etish",
                callback_data="reject_payment"
            )
        ]
    ]
)