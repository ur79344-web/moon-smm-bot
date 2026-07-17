from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import main_menu
from database import add_user, create_db

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await create_db()

    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🌙 MOON SMM\n\n"
        "Xush kelibsiz!\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )
