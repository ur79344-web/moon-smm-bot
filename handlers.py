from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards import main_menu
from database import add_user, create_db
from config import CHANNEL_1, CHANNEL_2

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


def check_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanal 1",
                    url=f"https://t.me/{CHANNEL_1.replace('@','')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Kanal 2",
                    url=f"https://t.me/{CHANNEL_2.replace('@','')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Tekshirish",
                    callback_data="check_sub"
                )
            ]
        ]
    )


async def subscribed(message):
    for channel in [CHANNEL_1, CHANNEL_2]:
        try:
            member = await message.bot.get_chat_member(
                channel,
                message.from_user.id
            )
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False

    return True


@router.message(CommandStart())
async def start(message: Message):
    await create_db()

    if not await subscribed(message):
        await message.answer(
            "Botdan foydalanish uchun 2 ta kanalga a'zo bo'ling:",
            reply_markup=check_button()
        )
        return

    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🌙 MOON SMM\n\nXush kelibsiz!",
        reply_markup=main_menu
    )


@router.callback_query(lambda c: c.data == "check_sub")
async def check(call: CallbackQuery):
    if await subscribed(call.message):
        await call.message.edit_text(
            "✅ Obuna tasdiqlandi.\nBotdan foydalanishingiz mumkin."
        )
        await call.message.answer(
            "🌙 MOON SMM",
            reply_markup=main_menu
        )
    else:
        await call.answer(
            "Hali obuna bo'lmagansiz!",
            show_alert=True
        )