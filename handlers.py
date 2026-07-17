from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states import PaymentState
from aiogram.types import Message, CallbackQuery

from keyboards import (
    main_menu,
    subscribe_keyboard
)

from database import (
    create_db,
    add_user,
)

from config import CHANNEL_1, CHANNEL_2


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
        
        
@router.message(lambda message: message.text == "💡 Xizmatlar")
async def services_menu_handler(message: Message):

    from keyboards import services_keyboard

    await message.answer(
        "📱 <b>Kerakli tarmoqni tanlang!</b>",
        reply_markup=services_keyboard,
        parse_mode="HTML"
    )
    
    
@router.callback_query(
    lambda c: c.data in [
        "telegram",
        "instagram",
        "youtube",
        "tiktok",
        "stars"
    ]
)
async def network_services(call: CallbackQuery):

    services = {
        "telegram": "🔵 Telegram xizmatlari",
        "instagram": "🟣 Instagram xizmatlari",
        "youtube": "🔴 YouTube xizmatlari",
        "tiktok": "⚫️ TikTok xizmatlari",
        "stars": "⭐️ Stars or Premium xizmatlari"
    }


    await call.message.answer(
        f"📦 <b>{services[call.data]}</b>\n\n"
        "Kerakli xizmat turini tanlang.\n"
        "Tez orada xizmatlar ro'yxati chiqadi.",
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
        "💰 Har bir taklif qilgan o'zbek referalingiz uchun "
        "100 so'm beriladi.\n"
        "🌍 Boshqa davlat referali uchun 50 so'm beriladi.\n\n"
        "⚠️ Feyk yoki yolg'on reklama block bo'lishga sabab bo'ladi.\n\n"
        f"👤 <b>ID raqam:</b> {message.from_user.id}",
        parse_mode="HTML"
    )
    
    
id="pay1"
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


from config import ADMIN_ID


await message.bot.send_photo(
    8638810880,
    message.photo[-1].file_id,
    caption=(
        "💳 Yangi to'lov!\n\n"
        f"👤 Foydalanuvchi ID: {message.from_user.id}\n"
        f"💰 Summa: {amount} so'm\n\n"
        "Tasdiqlash kerak."
    )
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
        parse_mode="HTML"
    )



@router.message(lambda message: message.text == "☎️ Qo'llab Quvvatlash")
async def support_handler(message: Message):

    await message.answer(
        "☎️ <b>Qo'llab Quvvatlash:</b>\n\n"
        "Admin: @khosimov_abu",
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
