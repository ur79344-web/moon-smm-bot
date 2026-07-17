from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from api import get_services
from database import add_user, create_db, get_balance
from keyboards import main_menu, services_menu
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
    "Assalomu alaykum! 👋\n\n"
    "Botdan foydalanishingiz mumkin.\n\n"
    "Kerakli bo‘limni tanlang:",
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


@router.message(lambda message: message.text == "💰 Balans")
async def balance(message: Message):

    balance = await get_balance(
        message.from_user.id
    )

    await message.answer(
        f"💰 Sizning balansingiz:\n\n{balance} so'm"
    )


@router.message(lambda message: message.text == "🛒 Xizmatlar")
async def services(message: Message):

    services = await get_services()

    if not services:
        await message.answer(
            "⚠️ Hozircha xizmatlar mavjud emas yoki API ulanmagan."
        )
        return

    text = "🛒 Xizmatlar:\n\n"

    for service in services[:20]:
        text += (
            f"🆔 {service['service']}\n"
            f"📌 {service['name']}\n"
            f"💵 {service['rate']}$\n\n"
        )

    await message.answer(text)


@router.message(lambda message: message.text == "📦 Buyurtma")
async def order(message: Message):

    services = await get_services()

    if not services:
        await message.answer(
            "⚠️ API ulanmagan yoki xizmatlar topilmadi."
        )
        return

    text = "📦 Buyurtma berish\n\n"
    text += "Quyidagi xizmat ID raqamini yuboring:\n\n"

    for service in services[:15]:
        text += f"{service['service']} - {service['name']}\n"

    await message.answer(text)


@router.message(lambda message: message.text == "📋 Buyurtmalarim")
async def my_orders(message: Message):

    await message.answer(
        "📋 Hozircha sizda buyurtmalar mavjud emas."
    )


@router.message(lambda message: message.text == "📞 Admin")
async def admin(message: Message):

    await message.answer(
        "👨‍💻 Admin: @KHOSIMOV_ABU"
    )


@router.message(lambda message: message.text == "➕ Hisobni to'ldirish")
async def deposit(message: Message):

    await message.answer(
        "💳 Hisobni to'ldirish uchun admin bilan bog'laning.\n\n"
        "👨‍💻 @KHOSIMOV_ABU"
    )