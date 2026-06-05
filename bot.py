import asyncio
import html
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
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

from config import ADMIN_GROUP_ID, BOT_TOKEN, COURSES, WELCOME_TEXT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

business_connections: dict[str, int] = {}

TRIGGER_WORDS = ["kurs", "курс", "course", "narx", "price", "chegirma", "скидка", "fotiha", "фотиха"]

DISCOUNT_WELCOME = (
    "Assalomu aleykum😇\n\n"
    "Xozirda <b>Standart va VIP tarifimizda</b> juda katta chegirma ketmoqda🎉🥳\n\n"
    "Pastdagi <b>«Chegirma»</b> tugmasiga bosing👇"
)

FOTIHA_TEXT = (
    "🌕 <b>\"FOTIHA\" TRANSFORMATSION KURSI</b> 🌕\n\n"
    "✨ Chuqur ichki o'zgarish va uyg'onish kursi\n\n"
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
    "ochiladi 🤍\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "🌿 <b>STANDARD TARIF</b>\n\n"
    "✔ 8 ta jonli darslik\n"
    "✔ Kurator yordamidan foydalanish\n"
    "✔ Muloqot chat guruhiga kirish\n"
    "✔ Kursga 3 oylik доступ\n\n"
    "💎 Asl narxi:\n<s>990.000</s> ❌\n\n"
    "✨ Chegirmada:\n<b>299.000 so'm</b> ✅\n\n"
    "🎁 BONUS:\n"
    "189$ lik\n"
    "<b>\"MINNATDORCHILIK VA O'ZINI SEVISH\"</b>\n"
    "darsi sovg'a 🎁\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "👑 <b>VIP TARIF</b>\n\n"
    "✔ 8 ta jonli darslik\n"
    "✔ Kuchli kurator support\n"
    "✔ Yopiq chat guruh\n"
    "✔ Keyingi kursga 30% voucher\n"
    "✔ Kursga 6 oylik доступ\n\n"
    "💎 Asl narxi:\n<s>2.400.000</s> ❌\n\n"
    "✨ Chegirmada:\n<b>599.000 so'm</b> ✅\n\n"
    "🎁 BONUS:\n"
    "210$ lik\n"
    "<b>\"BARAKALI AYOL\"</b>\n"
    "to'liq kursiga umrbod доступ 🎁"
)

LEAD_TEXT = (
    "🥳 Faqatgina <b>hozir to'lov qilgan</b> o'quvchilarimga "
    "chegirma uchun joylar ochildi.\n\n"
    "✅ <b>1 - imkoniyat:</b>\n"
    "189 $ lik <b>«Minnatdorchilik va o'zini sevish»</b> darsi "
    "sovg'a sifatida qo'shib beriladi.\n\n"
    "233 $ lik <b>«XIYONATGA MOYILLIK»</b> darsimni butun umrga доступ\n\n"
    "✅ <b>2 - imkoniyat:</b>\n"
    "6 ta bonus sovg'alarga erishish imkoniyatiga ega bo'lasiz.\n\n"
    "✅ <b>3 - imkoniyat:</b>\n"
    "3 kunlik to'liq darslarini audio formatda qo'lga kiritish imkoniyati\n\n"
    "✅ <b>4 - imkoniyat:</b>\n"
    "190 $ lik <b>PULLARGA OCHILISH</b> amalyotimni sovg'a qilaman\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "⚠️ <b>Diqqat! Joylar cheklangan.</b>\n"
    "⏳ Chegirma faqat <b>2 soat</b> davomida amal qiladi!\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "💳 <b>TO'LOV UCHUN KARTA:</b>\n\n"
    "5614 6810 1232 3550\n"
    "👤 Sharopova Jamila\n\n"
    "💰 Narxi: <b>99 000 so'm</b>\n\n"
    "✅ To'lov qilgach — <b>chekni yuboring</b> 📩\n"
    "✨ Tasdiqlangach kurs ochiladi 🤍\n\n"
    "━━━━━━━━━━━━━━━\n\n"
    "💬 Agar savolingiz bo'lsa yozing,\n"
    "navbatingiz kelganda javob beraman.\n\n"
    "⚡️ Navbatlar ko'p —\n"
    "kurs to'lib qolmasidan to'lovingizni qilib,\n"
    "<b>o'rningizni egallab oling!</b> 🌿"
)

PAYMENT_TEXT = (
    "💳 <b>TO'LOV UCHUN KARTA:</b>\n\n"
    "5614 6810 1232 3550\n"
    "👤 Sharopova Jamila\n\n"
    "✅ To'lov qilgach:\n"
    "📩 chekni yuboring\n\n"
    "✨ To'lov tasdiqlangach,\n"
    "sizga kurs ochiladi 🤍\n\n"
    "⚠ AKSIYA LIMITLANGAN ⚠\n\n"
    "🌕 Hozirda faqatgina\n"
    "10 ta joy qoldi ✅\n\n"
    "tez orada yopiladi ❗\n\n"
    "⏳ Joylar tugagach:\n"
    "❌ chegirma bekor qilinadi\n"
    "❌ narxlar yana oshadi\n\n"
    "💎 STANDARD:\n"
    "990.000 ❌ → 299.000 ✅\n\n"
    "👑 VIP:\n"
    "2.400.000 ❌ → 599.000 ✅\n\n"
    "🌿 Hoziroq joyingizni band qiling 🤍"
)


# ─── States ──────────────────────────────────────────

class Order(StatesGroup):
    waiting_screenshot = State()
    waiting_name = State()
    waiting_phone = State()


# ─── Keyboards ───────────────────────────────────────

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌕 FOTIHA kursi va narxlar", callback_data="show_discount")],
        [InlineKeyboardButton(text="❓ Ko'p so'raladigan savollar", callback_data="faq")],
        [InlineKeyboardButton(text="📞 Psixolog bilan bog'lanish", callback_data="contact")],
    ])

def tariff_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 VIP 599.000 ni tanladim", callback_data="enroll_vip")],
        [InlineKeyboardButton(text="🌿 Standart 299.000 ni tanladim", callback_data="enroll_standart")],
    ])

def lead_pay_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 To'ladim — chek yuborish", callback_data="paid")],
    ])

def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ])

def discount_trigger_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎉 Chegirma", callback_data="show_discount")],
    ])


# ─── Helpers ─────────────────────────────────────────

async def safe_edit(call: CallbackQuery, text: str, reply_markup=None):
    try:
        await call.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")


# ─── /start ──────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    args = message.text.split()
    if len(args) > 1 and args[1] == "lead":
        await state.update_data(source="lead")
        await message.answer(LEAD_TEXT, reply_markup=lead_pay_kb(), parse_mode="HTML")
    else:
        await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


# ─── Обычные сообщения ───────────────────────────────

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

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


# ─── Callbacks — обычная воронка ─────────────────────

@dp.callback_query(F.data == "show_discount")
async def show_discount(call: CallbackQuery):
    await safe_edit(call, FOTIHA_TEXT, reply_markup=tariff_kb())

@dp.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit(call, WELCOME_TEXT, reply_markup=main_menu_kb())

@dp.callback_query(F.data.startswith("enroll_"))
async def enroll_start(call: CallbackQuery, state: FSMContext):
    key = call.data.replace("enroll_", "")
    tariff = "👑 VIP — 599.000 so'm" if key == "vip" else "🌿 Standart — 299.000 so'm"
    await state.update_data(tariff=tariff)
    await state.set_state(Order.waiting_screenshot)
    await safe_edit(call, PAYMENT_TEXT, reply_markup=cancel_kb())

@dp.callback_query(F.data == "faq")
async def show_faq(call: CallbackQuery):
    text = (
        "❓ <b>Ko'p so'raladigan savollar</b>\n\n"
        "📌 <b>Darslar qanday o'tadi?</b>\n"
        "Onlayn, Zoom / Telegram orqali. Uydan qulay!\n\n"
        "📌 <b>Kurs qachon boshlanadi?</b>\n"
        "Yaqin orada yangi oqim boshlanadi. Hoziroq yoziling — o'tkazib yubormang!\n\n"
        "📌 <b>Sertifikat beriladimi?</b>\n"
        "Ha, kursni tugatgandan so'ng sertifikat beriladi.\n\n"
        "📌 <b>Darsga kela olmasam nima bo'ladi?</b>\n"
        "Barcha darslar yozib olinadi, qulay vaqtda ko'rishingiz mumkin."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌕 Kursga yozilish", callback_data="show_discount")],
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


# ─── Callback — лид воронка ──────────────────────────

@dp.callback_query(F.data == "show_lead")
async def show_lead(call: CallbackQuery):
    await safe_edit(call, LEAD_TEXT, reply_markup=lead_pay_kb())

@dp.callback_query(F.data == "paid")
async def on_paid(call: CallbackQuery, state: FSMContext):
    await state.set_state(Order.waiting_screenshot)
    await safe_edit(
        call,
        "📸 Ajoyib! Endi to'lov <b>skrinshotini</b> yuboring:",
        reply_markup=cancel_kb()
    )

@dp.callback_query(F.data == "cancel")
async def cancel_order(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    if data.get("source") == "lead":
        await safe_edit(call, LEAD_TEXT, reply_markup=lead_pay_kb())
    else:
        await safe_edit(call, WELCOME_TEXT, reply_markup=main_menu_kb())


# ─── Сбор данных (общий для обеих воронок) ───────────

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
        "📝 <b>Ism va familiyangizni</b> yozing:",
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

    tariff = data.get("tariff", "FOTIHA kursi — 99 000 so'm")
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

    source = data.get("source", "")
    source_line = "\n🌐 <b>YANGI LID</b> (saytdan) " + datetime.now().strftime("%d/%m") if source == "lead" else ""

    caption = (
        f"💰 <b>YANGI TO'LOV!</b>{source_line}\n\n"
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
        parse_mode="HTML"
    )


# ─── Business account ────────────────────────────────

@dp.business_connection()
async def on_business_connect(bc: BusinessConnection):
    if bc.is_enabled:
        business_connections[bc.id] = bc.user.id
        logger.info("Biznes akkaunt ulandi: user_id=%s", bc.user.id)
        await bot.send_message(
            chat_id=bc.user.id,
            text="✅ Bot biznes akkauntingizga muvaffaqiyatli ulandi!",
        )
    else:
        business_connections.pop(bc.id, None)

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

    # Любое новое сообщение в личке менеджера — показываем красивую кнопку
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🌕 FOTIHA kursi haqida ma'lumot olish",
            callback_data="show_lead"
        )],
    ])
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Bizning <b>transformatsion kursimiz</b> haqida bilmoqchimisiz?\n\n"
        "Quyidagi tugmani bosing 👇",
        reply_markup=kb,
        parse_mode="HTML"
    )


# ─── Entry point ─────────────────────────────────────

async def main():
    logger.info("Bot ishga tushdi!")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=["message", "callback_query", "business_connection", "business_message"]
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
