import asyncio
import html
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    BusinessConnection,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_GROUP_ID, BOT_TOKEN, WELCOME_TEXT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

business_connections: dict[str, int] = {}

TRIGGER_WORDS = ["kurs", "курс", "course", "narx", "price", "chegirma", "скидка", "fotiha", "фотиха"]
RETREAT_TRIGGER_WORDS = ["retreat", "ретрит", "retrit"]

FOTIHA_TEXT = (
    "🌕 <b>\"FOTIHA\" TRANSFORMATSION KURSI</b> 🌕\n\n"
    "✨ Chuqur ichki o'zgarish va uyg'onish kursi\n\n"
    "📌 <b>Kurs hozir faol davom etmoqda!</b>\n\n"
    "Hoziroq qo'shilsangiz sizga:\n"
    "🔓 <b>o'tib bo'lgan barcha darslar yozuvlariga</b> to'liq доступ\n"
    "🔓 <b>keyingi barcha yangi darslarga</b> to'liq доступ\n\n"
    "beriladi — hech narsani o'tkazib yubormaysiz! 🤍\n\n"
    "Bu kursda siz:\n"
    "🌿 ong osti bilan ishlaysiz\n"
    "🌿 qo'rquvlarni yechasiz\n"
    "🌿 qadrsizlikdan chiqasiz\n"
    "🌿 ichki erkinlikni ochasiz\n"
    "🌿 pul oqimi va energiya bilan ishlaysiz\n"
    "🌿 o'zingizni qayta kashf qilasiz\n\n"
    "✨ Kurs davomida:\n"
    "🎧 audio aktivatsiyalar\n"
    "📘 maxfiy PDF'lar\n"
    "🌿 practice va topshiriqlar\n"
    "💰 pul oqimi meditasiya\n"
    "🔐 yopiq support chat\n"
    "🎁 bonus darslar\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "✔ Jonli darslar\n"
    "✔ Kurator yordamidan foydalanish\n"
    "✔ Muloqot chat guruhiga kirish\n"
    "✔ O'tgan barcha darslar yozuvi\n"
    "✔ Kelajakdagi barcha darslar\n\n"
    "💎 Narxi: <b>299.000 so'm</b> ✅"
)

RETREAT_INTRO_TEXT = (
    "🌿 Assalomu alaykum! ✨ Yozganingiz uchun rahmat!\n\n"
    "🌊 Ha, Oybarchin Obidova Alaniyada o'zining mualliflik "
    "retreatini o'tkazadi — <b>«Perezagruzka / Qayta yuklanish»</b> "
    "nomli 🌅\n\n"
    "📅 <b>25-iyuldan 1-avgustgacha</b>\n"
    "🏖 Dengiz bo'yida 7 kunlik jonli, chuqur ishlov asosida\n\n"
    "💬 Qisqacha aytsam: bu «osoyishtalik haqida» ma'ruza emas.\n"
    "🔥 Bu — chuqur shaxsiy ish.\n\n"
    "🧘‍♀️ Bir hafta ichida inson o'zining haqiqiy holatlarini ko'rib "
    "chiqadi — 😟 xavotir, 😮‍💨 charchoq, 🔁 aylanib yuradigan "
    "munosabatlar — va shunchaki konspekt bilan emas, "
    "💪 ichki tayanch va aniq vositalar bilan qaytadi.\n\n"
    "🪑 Oqimga joylar ko'p emas — jami <b>35 ta</b>, va ular "
    "oldindan to'lov asosida band qilinadi.\n"
    "🎯 Oqim bitta, sanalar aniq. 🤍"
)

RETREAT_TEXT = (
    "🌊 <b>OYBARCHIN OBIDOVA BILAN RETREAT</b> 🌊\n\n"
    "📍 <b>Alaniya, Turkiya</b>\n\n"
    "✨ 7 kunlik chuqur ichki transformatsiya — "
    "dengiz bo'yida, real hayotda, real odamlar bilan 🤍\n\n"
    "Bu shunchaki dam olish emas — bu o'zingiz bilan "
    "yuzma-yuz kelish, ichingizdagi to'siqlarni yechish "
    "va yangi, kuchli versiyangizni topish sayohati.\n\n"
    "🎁 <b>Retreatdan nimalarga ega bo'lasiz:</b>\n"
    "🌿 ichingizdagi qo'rquv va bloklardan xalos bo'lasiz\n"
    "💪 o'ziga ishonch va ichki kuchni tiklaysiz\n"
    "❤️ o'zingiz va atrofdagilar bilan munosabatni yangilaysiz\n"
    "🧘 tinchlik, energiya va ravshanlikni his qilasiz\n"
    "👯 hayot bo'yi davom etadigan qadrli tanishuvlar orttirasiz\n"
    "🔑 hayotingizni yangi bosqichga olib chiqadigan insightlarga ega bo'lasiz\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "🔴 <b>JOYLAR CHEKLANGAN!</b>\n"
    "Ikkala formatda ham o'rinlar soni qat'iy belgilangan — "
    "ko'pchilik allaqachon band qilmoqda ⏳\n\n"
    "━━━━━━━━━━━━━━━\n\n"

    "🔵 <b>VIP — Jonli Retreat</b>\n"
    "💵 $1,550\n\n"
    "7 kun davomida Oybarchin Obidova bilan bir makonda bo'lasiz:\n"
    "🌅 dengiz bo'yida ertalabki amaliyotlar\n"
    "🌿 kichik guruhlarda chuqur sessiyalar\n"
    "🔍 shaxsiy so'rovingiz tahlili\n"
    "🍽 welcome va farewell kechki ovqatlari\n"
    "🧳 qayta zaryad beruvchi sayohat\n"
    "📸 professional foto va video\n"
    "💫 keyin ham aloqada qoladigan «o'z odamlaringiz» davrasi\n\n"
    "🏨 Yashash joyini maydon yaqinidan o'zingiz tanlaysiz — "
    "tanlashda yordam beramiz.\n\n"
    "🪑 <b>Bunday joylar — atigi 30 ta.</b>\n\n"
    "━━━━━━━━━━━━━━━\n\n"

    "🟡 <b>PREMIUM — Ekspert bilan shaxsan</b>\n"
    "💵 $2,500\n\n"
    "VIP'dagi barcha imkoniyatlar + Oybarchin Obidova butun davomida "
    "siz bilan shaxsan yonma-yon bo'ladi — \"sahnadan\" emas, "
    "tirik muloqotda:\n"
    "🎯 ustuvor individual sessiyalar\n"
    "🤍 eng tor doiradagi joy\n"
    "🎁 <b>SOVG'A:</b> retreatdan keyin 5 kun shaxsiy hamrohlik — "
    "aynan o'shanda insightlar bir haftada yo'qolib ketmasdan, "
    "haqiqiy o'zgarishga aylanadi\n\n"
    "🪑 <b>Bunday joylar — atigi 5 ta.</b>\n"
    "Bu Oybarchinning shaxsiy e'tibori chegarasi.\n"
    "⚠️ Bir qismi allaqachon band qilingan.\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "💬 Qaysi format sizga his-tuyg'u jihatidan yaqinroq?\n"
    "Tanlang 👇"
)

RETREAT_PHONE_TEXT = (
    "🤍 Ajoyib tanlov!\n\n"
    "📱 Endi <b>telefon raqamingizni</b> qoldiring — "
    "Oybarchin Obidova shaxsan sizga qo'ng'iroq qilib, "
    "barcha tafsilotlarni aytib beradi."
)

PAYMENT_TEXT = (
    "💳 <b>TO'LOV UCHUN KARTA:</b>\n\n"
    "5614 6810 1232 3550\n"
    "👤 Sharopova Jamila\n\n"
    "💰 Narxi: <b>299.000 so'm</b>\n\n"
    "✅ To'lov qilgach:\n"
    "📩 chekni yuboring\n\n"
    "✨ To'lov tasdiqlangach,\n"
    "sizga kurs guruhi va barcha darslar ochiladi 🤍"
)


class Order(StatesGroup):
    waiting_screenshot = State()
    waiting_name = State()
    waiting_phone = State()


class Retreat(StatesGroup):
    waiting_phone = State()


# ─── Keyboards ───────────────────────────────────────

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌕 FOTIHA kursi haqida", callback_data="show_fotiha")],
        [InlineKeyboardButton(text="❓ Ko'p so'raladigan savollar", callback_data="faq")],
        [InlineKeyboardButton(text="📞 Psixolog bilan bog'lanish", callback_data="contact")],
    ])


def fotiha_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ 299.000 ni to'lab qo'shilaman", callback_data="enroll_fotiha")],
    ])


def retreat_intro_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌿 Retreat haqida batafsil ma'lumot", callback_data="show_retreat")],
    ])


def retreat_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔵 VIP — $1,550", callback_data="retreat_vip")],
        [InlineKeyboardButton(text="🟡 PREMIUM — $2,500", callback_data="retreat_premium")],
    ])


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ])


# ─── Helpers ─────────────────────────────────────────

async def safe_edit(call: CallbackQuery, text: str, reply_markup=None, parse_mode="HTML"):
    try:
        await call.message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)


# ─── Handlers ────────────────────────────────────────

@dp.message()
async def any_message(message: Message, state: FSMContext):
    is_private = message.chat.type == "private"
    is_business = bool(message.business_connection_id)
    if not is_private and not is_business:
        return

    current = await state.get_state()

    if current == Order.waiting_screenshot:
        if message.photo:
            await get_screenshot(message, state)
        return

    if current == Order.waiting_name:
        await get_name(message, state)
        return

    if current == Order.waiting_phone:
        await get_phone(message, state)
        return

    if current == Retreat.waiting_phone:
        await get_retreat_phone(message, state)
        return

    text_lower = (message.text or "").lower()
    if any(word in text_lower for word in RETREAT_TRIGGER_WORDS):
        await message.answer(RETREAT_INTRO_TEXT, reply_markup=retreat_intro_kb(), parse_mode="HTML")
        return

    if any(word in text_lower for word in TRIGGER_WORDS):
        await message.answer(FOTIHA_TEXT, reply_markup=fotiha_kb(), parse_mode="HTML")
        return

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


@dp.callback_query(F.data == "show_retreat")
async def show_retreat(call: CallbackQuery):
    await safe_edit(call, RETREAT_TEXT, reply_markup=retreat_kb())


@dp.callback_query(F.data.startswith("retreat_"))
async def retreat_choice(call: CallbackQuery, state: FSMContext):
    key = call.data.replace("retreat_", "")
    tariff = "🔵 VIP Retreat — $1,550" if key == "vip" else "🟡 PREMIUM Retreat — $2,500"
    await state.update_data(
        retreat_tariff=tariff,
        user_id=call.from_user.id,
        username=call.from_user.username or "",
        first_name=call.from_user.first_name or "",
    )
    await state.set_state(Retreat.waiting_phone)
    await safe_edit(call, RETREAT_PHONE_TEXT, reply_markup=cancel_kb())


async def get_retreat_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    tariff = data.get("retreat_tariff", "—")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    safe_phone = html.escape(message.text or "—")
    user_id = data.get("user_id", message.from_user.id)
    username = data.get("username", "")
    first_name = html.escape(data.get("first_name", "") or "")

    if username:
        user_line = f"@{html.escape(username)}"
    else:
        user_line = f'<a href="tg://user?id={user_id}">{first_name or str(user_id)}</a>'

    caption = (
        f"🌊 <b>YANGI RETREAT SO'ROVI!</b>\n\n"
        f"🎯 Format: {tariff}\n"
        f"📱 Telefon: {safe_phone}\n"
        f"🆔 Telegram ID: <code>{user_id}</code>\n"
        f"✈️ Username: {user_line}\n"
        f"📅 Sana: {now}"
    )
    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=caption, parse_mode="HTML")
    await state.clear()
    await message.answer(
        "🤍 <b>Rahmat! Ma'lumotlaringiz qabul qilindi.</b>\n\n"
        "Oybarchin Obidova tez orada sizga shaxsan qo'ng'iroq qiladi 📞",
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "show_fotiha")
async def show_fotiha(call: CallbackQuery):
    await safe_edit(call, FOTIHA_TEXT, reply_markup=fotiha_kb())


@dp.callback_query(F.data == "enroll_fotiha")
async def enroll_fotiha(call: CallbackQuery, state: FSMContext):
    await state.update_data(tariff="FOTIHA kursi — 299.000 so'm")
    await state.set_state(Order.waiting_screenshot)
    await safe_edit(call, PAYMENT_TEXT, reply_markup=cancel_kb())


async def get_screenshot(message: Message, state: FSMContext):
    await state.update_data(
        photo_id=message.photo[-1].file_id,
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
    )
    await state.set_state(Order.waiting_name)
    await message.answer(
        "✅ Chek qabul qilindi!\n\n"
        "📝 Endi <b>ism va familiyangizni</b> yozing:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )


async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order.waiting_phone)
    await message.answer(
        "📱 <b>Telefon raqamingizni</b> yozing:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )


async def get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    data["phone"] = message.text

    tariff = data.get("tariff", "FOTIHA kursi — 299.000 so'm")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    safe_name = html.escape(data.get("name") or "—")
    safe_phone = html.escape(data.get("phone") or "—")
    user_id = data.get("user_id", message.from_user.id)
    username = data.get("username", "")
    first_name = html.escape(data.get("first_name", "") or "")

    if username:
        user_line = f"@{html.escape(username)}"
    else:
        user_line = f'<a href="tg://user?id={user_id}">{first_name or str(user_id)}</a>'

    caption = (
        f"💰 <b>YANGI TO'LOV!</b>\n\n"
        f"🎯 Tarif: {tariff}\n"
        f"👤 Ism: {safe_name}\n"
        f"📱 Telefon: {safe_phone}\n"
        f"🆔 Telegram ID: <code>{user_id}</code>\n"
        f"✈️ Username: {user_line}\n"
        f"📅 Sana: {now}"
    )
    await bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=data["photo_id"],
        caption=caption,
        parse_mode="HTML"
    )
    await state.clear()
    await message.answer(
        "🎉 <b>Rahmat! Ma'lumotlaringiz qabul qilindi.</b>\n\n"
        "Tekshirib, tez orada kurs guruhiga qo'shamiz. Odatda 24 soat ichida 🤍",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Psixologga yozish", callback_data="contact")],
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")],
        ]),
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit(call, WELCOME_TEXT, reply_markup=main_menu_kb())


@dp.callback_query(F.data == "faq")
async def show_faq(call: CallbackQuery):
    text = (
        "❓ <b>Ko'p so'raladigan savollar</b>\n\n"
        "📌 <b>Kurs allaqachon boshlangan, kech bo'lmaydimi?</b>\n"
        "Yo'q! Qo'shilganingizda o'tgan barcha darslar yozuvi sizga ochiladi, "
        "shu bilan birga keyingi yangi darslarga ham to'liq доступ olasiz.\n\n"
        "📌 <b>Darslar qanday o'tadi?</b>\n"
        "Onlayn, Zoom / Telegram orqali. Uydan qulay!\n\n"
        "📌 <b>Sertifikat beriladimi?</b>\n"
        "Ha, kursni tugatgandan so'ng sertifikat beriladi.\n\n"
        "📌 <b>Darsga kela olmasam nima bo'ladi?</b>\n"
        "Barcha darslar yozib olinadi, qulay vaqtda ko'rishingiz mumkin."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌕 Kursga qo'shilish", callback_data="show_fotiha")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")],
    ])
    await safe_edit(call, text, reply_markup=kb)


@dp.callback_query(F.data == "contact")
async def show_contact(call: CallbackQuery):
    text = (
        "📞 <b>Psixolog bilan bog'lanish</b>\n\n"
        "Shaxsiy savollaringiz bo'lsa yoki konsultatsiya olmoqchi bo'lsangiz:\n\n"
        "👩‍💼 @OybarchinObidova\n\n"
        "Bir necha soat ichida javob beramiz 🤍"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")],
    ])
    await safe_edit(call, text, reply_markup=kb)


@dp.callback_query(F.data == "cancel")
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit(
        call,
        "❌ Bekor qilindi.\n\nMenyuga qaytish uchun tugmani bosing 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")]
        ])
    )


# ─── Business account ────────────────────────────────

@dp.business_connection()
async def on_business_connect(bc: BusinessConnection):
    if bc.is_enabled:
        business_connections[bc.id] = bc.user.id
        logger.info("Biznes akkaunt ulandi: user_id=%s", bc.user.id)
        await bot.send_message(
            chat_id=bc.user.id,
            text="✅ Bot biznes akkauntingizga muvaffaqiyatli ulandi!\n\nEndi mijozlar xabar yozganda bot avtomatik javob beradi.",
        )
    else:
        business_connections.pop(bc.id, None)
        logger.info("Biznes akkaunt uzildi: user_id=%s", bc.user.id)


@dp.business_message()
async def any_business_message(message: Message, state: FSMContext):
    conn_id = message.business_connection_id

    if conn_id not in business_connections:
        try:
            bc = await bot.get_business_connection(conn_id)
            business_connections[conn_id] = bc.user.id
        except Exception:
            pass

    owner_id = business_connections.get(conn_id)
    if owner_id and message.from_user and message.from_user.id == owner_id:
        return

    current = await state.get_state()

    if current == Order.waiting_screenshot:
        if message.photo:
            await get_screenshot(message, state)
        return

    if current == Order.waiting_name:
        await get_name(message, state)
        return

    if current == Order.waiting_phone:
        await get_phone(message, state)
        return

    if current == Retreat.waiting_phone:
        await get_retreat_phone(message, state)
        return

    text_lower = (message.text or "").lower()
    if any(word in text_lower for word in RETREAT_TRIGGER_WORDS):
        await message.answer(RETREAT_INTRO_TEXT, reply_markup=retreat_intro_kb(), parse_mode="HTML")
        return

    if any(word in text_lower for word in TRIGGER_WORDS):
        await message.answer(FOTIHA_TEXT, reply_markup=fotiha_kb(), parse_mode="HTML")


# ─── Entry point ─────────────────────────────────────

async def main():
    logger.info("Bot ishga tushdi!")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=[
                "message",
                "callback_query",
                "business_connection",
                "business_message",
            ]
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
