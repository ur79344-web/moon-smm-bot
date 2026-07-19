from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from states import PaymentState

from keyboards import (
    main_menu,
    subscribe_keyboard,
    payment_admin_keyboard,
    referal_keyboard,
    top_referrals_keyboard,
)

from database import (
    create_db,
    add_user,
    get_top_referrals,
)

from config import CHANNEL_1, CHANNEL_2, ADMIN_ID


router = Router()


async def subscribed(message: Message):

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

    user = message.from_user

    if not await subscribed(message):

        from keyboards import subscribe_keyboard

        await message.answer(
            "⛔ <b>Botdan foydalanish uchun, quyidagi kanallarga obuna bo'ling:</b>",
            reply_markup=subscribe_keyboard,
            parse_mode="HTML"
        )

        return


    await add_user(
        user.id,
        user.username
    )


    await message.answer(
        "🖥️ <b>Asosiy menyudasiz.</b>",
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    
    
@router.callback_query(lambda c: c.data == "check_sub")
async def check_sub(call: CallbackQuery):

    if await subscribed(call.message):

        await add_user(
            call.from_user.id,
            call.from_user.username
        )

        await call.message.edit_text(
            "✅ <b>Obuna muvaffaqiyatli tasdiqlandi!</b>",
            parse_mode="HTML"
        )

        await call.message.answer(
            "🖥️ <b>Asosiy menyudasiz.</b>",
            reply_markup=main_menu,
            parse_mode="HTML"
        )

    else:

        await call.answer(
            "❌ Hali obuna bo'lmagansiz!",
            show_alert=True
        )
        
        
@router.callback_query(lambda c: c.data == "main_menu")
async def back_main_menu(call: CallbackQuery):

    await call.message.answer(
        "🖥️ <b>Asosiy menyudasiz.</b>",
        reply_markup=main_menu,
        parse_mode="HTML"
    )

    await call.answer()
        
        
@router.message(lambda message: message.text == "💡 Xizmatlar")
async def services_menu_handler(message: Message):

    from keyboards import services_keyboard

    await message.answer(
        "📱 <b>Kerakli tarmoqni tanlang!</b>",
        reply_markup=services_keyboard,
        parse_mode="HTML"
    )
    
    
@router.callback_query(
    lambda c: c.data == "telegram"
)
async def network_services(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Obunachi", callback_data="tg_sub")],
            [InlineKeyboardButton(text="🌟 Premium 👥 Obunachi", callback_data="tg_premium")],
            [InlineKeyboardButton(text="🤖 Bot 👥 Obunachi", callback_data="tg_bot_sub")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Telegram bo‘limlaridan birini tanlang!</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "tg_sub")
async def telegram_subscribers(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Obunachi • Kafolatsiz", callback_data="tg_sub_noguarantee")],
            [InlineKeyboardButton(text="♻️ Obunachi • Kafolatli", callback_data="tg_sub_guarantee")],
            [InlineKeyboardButton(text="🌱 Obunachi • Tabiiy & Aktiv", callback_data="tg_sub_natural")],
            [InlineKeyboardButton(text="🟢 Obunachi • Onlayn", callback_data="tg_sub_online")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="telegram")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Ichki bo'limlaridan birini tanlang.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "tg_sub_noguarantee")
async def tg_sub_noguarantee(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👣 Obunachi ⚡️ — 1000 so'm", callback_data="service_235")],
            [InlineKeyboardButton(text="👣 Obunachi (♻️ R3) — 1200 so'm", callback_data="service_236")],
            [InlineKeyboardButton(text="👣 Obunachi (♻️ R7) — 1500 so'm", callback_data="service_237")],
            [InlineKeyboardButton(text="👣 Obunachi (♻️ R15) — 2000 so'm", callback_data="service_238")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="tg_sub")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Marhamat, kerakli ta'rifni tanlang!</b>\n\n"
        "💰 <b>Narxlar 1000 tasi uchun berilgan.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    await call.answer()


@router.callback_query(lambda c: c.data == "tg_sub_natural")
async def tg_sub_natural(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👣 Obunachi + ko‘rish (♻️ R30) — 60 000 so'm", callback_data="service_239")],
            [InlineKeyboardButton(text="👣 Obunachi + ko‘rish (♻️ R60) — 95 000 so'm", callback_data="service_240")],
            [InlineKeyboardButton(text="👣 Obunachi + ko‘rish (♻️ R90) — 140 000 so'm", callback_data="service_241")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="tg_sub")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Marhamat, kerakli ta'rifni tanlang!</b>\n\n"
        "💰 <b>Narxlar 1000 tasi uchun berilgan.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "tg_sub_online")
async def tg_sub_online(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Obunachi 🇷🇺 RUS (🟢Online | ♻️R30) — 30 000 so'm", callback_data="service_246")],
            [InlineKeyboardButton(text="👥 Obunachi (🟢Online | ♻️R30) — 40 000 so'm", callback_data="service_245")],
            [InlineKeyboardButton(text="👥 Obunachi 🇨🇳 Xitoy (🟢Online | ♻️R30) — 40 000 so'm", callback_data="service_247")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="tg_sub")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Marhamat, kerakli ta'rifni tanlang!</b>\n\n"
        "💰 <b>Narxlar 1000 tasi uchun berilgan.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data in ["tg_sub_uzbek", "tg_sub_uzbek2"])
async def tg_sub_uzbek(call: CallbackQuery):

    await call.answer(
        "⚠️ Ushbu xizmat tez orada qo'shiladi!",
        show_alert=True
    )
    
    
@router.callback_query(lambda c: c.data == "tg_sub_guarantee")
async def tg_sub_guarantee(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="👣 Obunachi SOXTA (⛔️ BEZ MINUS) HOT🔥 — 13 000 so'm",
                callback_data="service_242"
            )],
            [InlineKeyboardButton(
                text="👣 Obunachi (⛔️ BEZ MINUS) HOT🔥 — 13 000 so'm",
                callback_data="service_243"
            )],
            [InlineKeyboardButton(
                text="👣 Obunachi (⛔️ Bezminus | ♻️ R30) — 5 000 so'm",
                callback_data="service_278"
            )],
            [InlineKeyboardButton(
                text="👣 Obunachi (⛔️ Bezminus | ♻️ R30) ⚡️ — 4 900 so'm",
                callback_data="service_279"
            )],
            [InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="tg_sub"
            )]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Marhamat, kerakli ta'rifni tanlang!</b>\n\n"
        "💰 <b>Narxlar 1000 tasi uchun berilgan.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "tg_premium")
async def telegram_premium(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🌟 Premium 👥 Obunachi (Kafolatsiz)",
                callback_data="tg_premium_noguarantee"
            )],
            [InlineKeyboardButton(
                text="🌟 Premium 👥 Obunachi (♻️ Kafolatli)",
                callback_data="tg_premium_guarantee"
            )],
            [InlineKeyboardButton(
                text="🌟 Premium 👥 Obunachi (Arzon baza)",
                callback_data="tg_premium_cheap"
            )],
            [InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="telegram"
            )]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Ichki bo'limlaridan birini tanlang.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "tg_views")
async def telegram_views(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👁️ Ko'rish (Bitta post uchun)",
                    callback_data="tg_views_single"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👁️ Ko'rish (Eski - oxirgi post uchun)",
                    callback_data="tg_views_old"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👁️ Ko'rish (Kelgusi post uchun)",
                    callback_data="tg_views_future"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data="telegram"
                )
            ]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Ichki bo'limlaridan birini tanlang.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "tg_views_old")
async def tg_views_old(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="👁️ Eski-oxirgi 5 ta post — 805 so'm",
                callback_data="service_303"
            )],
            [InlineKeyboardButton(
                text="👁️ Eski-oxirgi 10 ta post — 1 500 so'm",
                callback_data="service_304"
            )],
            [InlineKeyboardButton(
                text="👁️ Eski-oxirgi 20 ta post — 3 000 so'm",
                callback_data="service_305"
            )],
            [InlineKeyboardButton(
                text="👁️ Eski-oxirgi 50 ta post — 5 560 so'm",
                callback_data="service_306"
            )],
            [InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="tg_views"
            )]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Marhamat, kerakli ta'rifni tanlang!</b>\n\n"
        "💰 <b>Narxlar 1000 tasi uchun berilgan.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "tg_reaction")
async def telegram_reaction(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎭 Reaksiya (Aralash)", callback_data="tg_reaction_mix")],
            [InlineKeyboardButton(text="🎭 Reaksiya - 1", callback_data="tg_reaction_1")],
            [InlineKeyboardButton(text="🎭 Reaksiya - 2", callback_data="tg_reaction_2")],
            [InlineKeyboardButton(text="🎭 Reaksiya - 3", callback_data="tg_reaction_3")],
            [InlineKeyboardButton(text="🎭 Reaksiya - 4", callback_data="tg_reaction_4")],
            [InlineKeyboardButton(text="🎭 Reaksiya - 5", callback_data="tg_reaction_5")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="telegram")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Ichki bo'limlaridan birini tanlang.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "tg_bot_sub")
async def telegram_bot_sub(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖 Oddiy start",
                    callback_data="tg_bot_start"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🤖 Bot start (Referal ID)",
                    callback_data="tg_bot_ref"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data="telegram"
                )
            ]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Ichki bo'limlaridan birini tanlang.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    

@router.callback_query(
    lambda c: c.data == "instagram"
)
async def network_services(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Obunachi", callback_data="ig_sub")],
            [InlineKeyboardButton(text="▶️ Video ko'rish", callback_data="ig_views")],
            [InlineKeyboardButton(text="❤️ Like | Yoqtirish", callback_data="ig_like")],
            [InlineKeyboardButton(text="💬 Comment", callback_data="ig_comment")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ]
    )

    await call.message.edit_text(
        "📦 <b>Instagram bo‘limlaridan birini tanlang!</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.message(lambda message: message.text == "🛒 Buyurtmalar")
async def my_orders(message: Message):

    from database import get_orders

    orders = await get_orders(
        message.from_user.id
    )


    if not orders:

        await message.answer(
            "❗️Sizda buyurtmalar mavjud emas."
        )

        return


    text = "📦 <b>Buyurtmalar:</b>\n\n"

    for order in orders:

        service, status = order

        text += (
            f"✅ {status}\n"
        )


    await message.answer(
        text,
        parse_mode="HTML"
    )
    

@router.message(lambda message: message.text == "💰 Balans")
async def balance_handler(message: Message):

    from database import get_balance
    from keyboards import balance_keyboard


    balance = await get_balance(
        message.from_user.id
    )


    await message.answer(
        f"💰 <b>Balansingiz:</b> {balance:.2f} so'm\n\n"
        f"👤 <b>ID raqam:</b> {message.from_user.id}",
        reply_markup=balance_keyboard,
        parse_mode="HTML"
    )



@router.callback_query(lambda c: c.data == "discount")
async def discount_handler(call: CallbackQuery):

    await call.answer(
        "⚠️ Chegirma turlari mavjud emas",
        show_alert=True
    )
    
    
@router.message(lambda message: message.text == "🗣️ Referal")
async def referral_handler(message: Message):

    from database import get_referrals
    from keyboards import referal_keyboard

    referrals = await get_referrals(
        message.from_user.id
    )

    bot_username = (await message.bot.get_me()).username

    referral_link = (
        f"https://t.me/{bot_username}?start={message.from_user.id}"
    )

    await message.answer(
        "🗣️ <b>Sizning referal havolangiz:</b>\n\n"
        f"{referral_link}\n\n"
        f"👥 <b>Sizning referallaringiz:</b> {referrals} ta\n\n"
        "💰 Har bir taklif qilgan o'zbek referalingiz uchun 100 so'm beriladi.\n"
        "🌍 Boshqa davlat referali uchun 50 so'm beriladi.\n\n"
        "⚠️ Feyk yoki yolg'on reklama block bo'lishga sabab bo'ladi.\n\n"
        f"👤 <b>ID raqam:</b> {message.from_user.id}",
        reply_markup=referal_keyboard,
        parse_mode="HTML"
    )


@router.callback_query(lambda c: c.data == "top_referrals")
async def top_referrals(call: CallbackQuery):

    from database import get_top_referrals
    from keyboards import top_referrals_keyboard
    from datetime import datetime

    users = await get_top_referrals()

    text = (
        "⚡️ <b>Mavjud natijalar:</b>\n\n"
        "🔍 <b>So'rov:</b> 📎 Referal bo'yicha\n\n"
        "🏆 <b>Top reyting: 10 ta</b>\n\n"
    )

    if users:
        for i, (username, user_id, referrals) in enumerate(users, start=1):
            if username:
                name = f"@{username}"
            else:
                name = str(user_id)

            text += f"{i}) {name} — {referrals}\n"
    else:
        text += "Hozircha reyting mavjud emas.\n"

    text += f"\n⏰ {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

    await call.message.edit_text(
        text,
        reply_markup=top_referrals_keyboard,
        parse_mode="HTML"
    )

    await call.answer()


@router.message(lambda message: message.text == "💳 To'lov")
async def payment_handler(message: Message):

    from keyboards import payment_keyboard

    await message.answer(
        "👇 <b>Pastdagi berilgan tugmalardan birini tanlang "
        "va to'lov summasini kiriting hamda sizga berilgan "
        "havola orqali to'lovni amalga oshiring va tasdiqlang!</b>\n\n"
        "⚠️ <b>Diqqat!</b> Barcha to'lov tizimlari xavfsiz. "
        "To'lov qilganingizdan so'ng kartangizdan ortiqcha pul "
        "yechilmaydi va kartangizga ulanilmaydi.\n\n"
        "ID raqam: "
        f"{message.from_user.id}",
        reply_markup=payment_keyboard,
        parse_mode="HTML"
    )


@router.callback_query(
    lambda c: c.data in ["tiktok", "youtube", "stars"]
)
async def unavailable_services(call: CallbackQuery):

    await call.answer()

    await call.message.answer(
        "⚠️ <b>Ushbu tarmoq uchun xizmat turlari topilmadi.</b>",
        parse_mode="HTML"
    )


@router.callback_query(lambda c: c.data == "humocard")
async def humocard_handler(call: CallbackQuery):

    from keyboards import humocard_keyboard

    await call.message.answer(
        "🪙 <b>To'lov tizimi:</b> 🟡 HumoCard\n\n"
        "💳 <b>Hamyon:</b> 9860 1701 1031 3641\n\n"
        "👤 <b>Ega:</b> Gulhumor Raximova\n"
        "🏦 <b>Bank:</b> IpakYuli Bank\n"
        "☎️ <b>Raqam:</b> +998 (88) 676 05 79\n\n"
        "🤝 Hisobingizni muvaffaqiyatli to'ldirish uchun:\n\n"
        "1) Pul miqdorini tepadagi hamyonga tashlang.\n"
        "2) «✅ To'lov qildim» tugmasini bosing.\n"
        "3) Qancha yuborganingizni kiriting.\n"
        "4) To'lov suratini yuboring.\n"
        "5) Operator tasdiqlashini kuting.\n\n"
        "⚠️ Minimal 1000 so'm. Undan kam summaga to'ldirib bo'lmaydi.",
        reply_markup=humocard_keyboard,
        parse_mode="HTML"
    )
    
    
from aiogram.fsm.context import FSMContext
from states import PaymentState


@router.callback_query(lambda c: c.data == "payment_done")
async def payment_done_handler(
    call: CallbackQuery,
    state: FSMContext
):

    await call.message.answer(
        "💸 To'lov miqdorini kiriting.\n\n"
        "Kartaga qancha tashlagan bo'lsangiz shuni kiriting!"
    )

    await state.set_state(
        PaymentState.amount
    )

    await call.answer()



@router.message(PaymentState.amount)
async def payment_amount_handler(
    message: Message,
    state: FSMContext
):

    try:
        amount = float(message.text)

    except:

        await message.answer(
            "❌ Iltimos, faqat raqam kiriting."
        )

        return


    await state.update_data(
        amount=amount
    )


    await message.answer(
        "📃 To'lov chekini rasmini yuboring."
    )


    await state.set_state(
        PaymentState.photo
    )



@router.message(
    PaymentState.photo
)
async def payment_photo_handler(
    message: Message,
    state: FSMContext
):

    if not message.photo:

        await message.answer(
            "❌ Iltimos, chek rasmini yuboring."
        )

        return


    data = await state.get_data()

    amount = data["amount"]


    from database import add_payment


    await add_payment(
        message.from_user.id,
        amount,
        message.photo[-1].file_id
    )


    await message.bot.send_photo( 
        8638810880,
        message.photo[-1].file_id,
        caption=(
            "💳 Yangi to'lov!\n\n"
            f"👤 Foydalanuvchi ID: {message.from_user.id}\n"
            f"💰 Summa: {amount} so'm\n\n"
            "Tasdiqlash kerak."
        ),
        reply_markup=payment_admin_keyboard
    )


    await message.answer(
        "⏰ Sizning to'lovingiz administratorlarga yuborildi.\n\n"
        "💸 To'lov tasdiqlanishi bilan hisobingizga pul tushadi.\n\n"
        "⚠️ To'lovlar 30 daqiqadan 48 soatgacha "
        "bo'lgan muddat ichida ko'rib chiqiladi.",
        reply_markup=main_menu
    )


    await state.clear()

    
    
@router.message(lambda message: message.text == "📔 Qo'llanma")
async def guide_handler(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👨‍💻 Admin bilan bog'lanish",
                    url="https://t.me/moonsmm_help"
                )
            ]
        ]
    )

    await message.answer(
        "📘 <b>Botdan foydalanish yo'riqnomasi:</b>\n\n"
        "🔄 <b>Buyurtma bekor qilindimi?</b>\n"
        "Xavotir olmang! Mablag'ingiz avtomatik ravishda hisobingizga qaytariladi.\n\n"
        "🕒 <b>To'lovdan so'ng kutish vaqti:</b>\n"
        "Pullar hisobingizga 24 soat ichida tushadi, sabrli bo'ling.\n\n"
        "🚫 <b>Mablag'lar qaytarilmaydi!</b>\n"
        "Botga joylashtirilgan mablag'lar qaytarib berilmaydi.\n\n"
        "📩 <b>Buyurtma haqida savol bormi?</b>\n"
        "Muammo yoki savol tug'ilsa, adminlarga murojaat qiling.\n\n"
        "⚠️ <b>Bitta xizmat — bitta buyurtma:</b>\n"
        "Bir vaqtda faqat bitta buyurtma berishingiz mumkin.\n\n"
        "🎯 <b>Referal mukofoti:</b>\n"
        "Agar referallingiz kanallarga qo'shilmasa, mukofot puli berilmaydi.\n\n"
        "❗️ Xatolik yoki muammolar uchun: @moonsmm_help",
        reply_markup=keyboard,
        parse_mode="HTML"
    )



@router.message(lambda message: message.text == "☎️ Qo'llab Quvvatlash")
async def support_handler(message: Message):

    from keyboards import support_keyboard

    await message.answer(
        "☎️ <b>Qo'llab Quvvatlash</b>\n\n"
        "Savolingiz yoki muammoingiz bo'lsa, quyidagi tugma orqali admin bilan bog'laning.",
        reply_markup=support_keyboard,
        parse_mode="HTML"
    )



@router.callback_query(lambda c: c.data == "back_menu")
async def back_menu(call: CallbackQuery):

    await call.message.answer(
        "🖥️ <b>Asosiy menyudasiz.</b>",
        reply_markup=main_menu,
        parse_mode="HTML"
    )

    await call.answer()
    
    
id="4rj8mk"
@router.callback_query(lambda c: c.data == "payment_back")
async def payment_back(call: CallbackQuery):

    await call.message.answer(
        "🖥️ <b>Asosiy menyudasiz.</b>",
        reply_markup=main_menu,
        parse_mode="HTML"
    )

    await call.answer()
    
    
@router.callback_query(lambda c: c.data == "approve_payment")
async def approve_payment(call: CallbackQuery):

    from database import add_balance, get_last_payment, add_user

    user_id = call.message.caption.split("ID: ")[1].split("\n")[0]

    payment = await get_last_payment(
        int(user_id)
    )

    if not payment:
        await call.answer(
            "❌ To'lov topilmadi",
            show_alert=True
        )
        return

    amount = payment[2]

    print("BALANS QO'SHILMOQDA:", user_id, amount)

    await add_user(
        int(user_id),
        None
    )

    await add_balance(
        int(user_id),
        amount
    )

    await call.message.bot.send_message(
        int(user_id),
        f"✅ To'lov tasdiqlandi!\n\n"
        f"💰 Hisobingizga {amount} so'm qo'shildi."
    )

    await call.answer(
        "✅ Tasdiqlandi",
        show_alert=True
    )