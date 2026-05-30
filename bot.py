import asyncio
import html
import logging
import os
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

from config import ADMIN_GROUP_ID, BOT_TOKEN, COURSES, PAYMENT_DETAILS, WELCOME_TEXT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

paid_clients: list[dict] = []
business_connections: dict[str, int] = {}  # connection_id -> owner user_id

TRIGGER_WORDS = ["kurs", "курс", "course", "narx", "price", "chegirma", "скидка"]

DISCOUNT_WELCOME = (
    "Assalomu aleykum😇\n\n"
    "Xozirda <b>Standart va VIP tarifimizda</b> juda katta chegirma ketmoqda🎉🥳\n\n"
    "Pastdagi <b>«Chegirma»</b> tugmasiga bosing👇"
)


async def safe_edit(call: CallbackQuery, text: str, reply_markup=None, parse_mode="HTML"):
    try:
        await call.message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)


class Order(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_screenshot = State()
    waiting_bron_screenshot = State()


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Kurslar va narxlar", callback_data="show_courses")],
        [InlineKeyboardButton(text="❓ Ko'p so'raladigan savollar", callback_data="faq")],
        [InlineKeyboardButton(text="📞 Psixolog bilan bog'lanish", callback_data="contact")],
    ])


def courses_kb() -> InlineKeyboardMarkup:
    buttons = []
    for key, course in COURSES.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{course['emoji']} {course['name']} — {course['price']}",
                callback_data=f"course_{key}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def course_detail_kb(course_key: str) -> InlineKeyboardMarkup:
    course = COURSES.get(course_key, {})
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"✅ To'liq to'lash — {course.get('price', '')}",
            callback_data=f"enroll_{course_key}"
        )],
        [InlineKeyboardButton(
            text=f"🔒 Bron qilish — {course.get('bron_price', '')} (oldindan to'lov)",
            callback_data=f"bron_{course_key}"
        )],
        [InlineKeyboardButton(text="🔙 Kurslarga qaytish", callback_data="show_courses")],
    ])


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ])


def discount_trigger_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎉 Chegirma", callback_data="show_discount")],
    ])


@dp.message()
async def any_message(message: Message, state: FSMContext):
    is_private = message.chat.type == "private"
    is_business = bool(message.business_connection_id)
    if not is_private and not is_business:
        return

    current = await state.get_state()

    if current == Order.waiting_name:
        await get_name(message, state)
        return
    if current == Order.waiting_phone:
        await get_phone(message, state)
        return
    if current == Order.waiting_screenshot:
        if message.photo:
            await get_screenshot(message, state)
        else:
            await message.answer(
                "📸 Iltimos, aynan to'lov <b>skrinshotini</b> (rasm) yuboring.",
                reply_markup=cancel_kb(), parse_mode="HTML"
            )
        return
    if current == Order.waiting_bron_screenshot:
        if message.photo:
            await get_bron_screenshot(message, state)
        else:
            await message.answer(
                "📸 Iltimos, aynan bron to'lovi <b>skrinshotini</b> (rasm) yuboring.",
                reply_markup=cancel_kb(), parse_mode="HTML"
            )
        return

    text_lower = (message.text or "").lower()
    if any(word in text_lower for word in TRIGGER_WORDS):
        await message.answer(DISCOUNT_WELCOME, reply_markup=discount_trigger_kb(), parse_mode="HTML")
        return

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


@dp.callback_query(F.data == "show_discount")
async def show_discount(call: CallbackQuery):
    text = (
        "🎉 <b>Maxsus chegirma narxlar!</b>\n\n"
        "📦 <b>Standart tarif</b>\n"
        "<s>990,000 so'm</s> → <b>299,000 so'm</b> 🔥\n\n"
        "💎 <b>VIP tarif</b>\n"
        "<s>2,400,000 so'm</s> → <b>599,000 so'm</b> 🔥\n\n"
        "⏰ Chegirma <b>cheklangan vaqtga!</b>\n\n"
        "Kursga yozilish yoki batafsil ma'lumot uchun 👇"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Kurslarga qarash", callback_data="show_courses")],
        [InlineKeyboardButton(text="📞 Psixolog bilan bog'lanish", callback_data="contact")],
    ])
    await safe_edit(call, text, reply_markup=kb)


@dp.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit(call, WELCOME_TEXT, reply_markup=main_menu_kb())


@dp.callback_query(F.data == "show_courses")
async def show_courses(call: CallbackQuery):
    text = "📚 <b>Bizning kurslar:</b>\n\nBatafsil ma'lumot uchun kursni tanlang 👇"
    await safe_edit(call, text, reply_markup=courses_kb())


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
        [InlineKeyboardButton(text="📚 Kurslarga qarash", callback_data="show_courses")],
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


@dp.callback_query(F.data.startswith("course_"))
async def course_detail(call: CallbackQuery):
    key = call.data.replace("course_", "")
    course = COURSES.get(key)
    if not course:
        await call.answer("Kurs topilmadi", show_alert=True)
        return

    old_price_line = f"<s>{course['old_price']}</s> → " if course.get("old_price") else ""

    text = (
        f"{course['emoji']} <b>{course['name']}</b>\n\n"
        f"📝 {course['description']}\n\n"
        f"⏱ <b>Davomiyligi:</b> {course['duration']}\n"
        f"👥 <b>Format:</b> {course['format']}\n"
        f"💰 <b>Narxi:</b> {old_price_line}<b>{course['price']}</b>\n"
        f"🔒 <b>Bron:</b> {course['bron_price']} (oldindan to'lov)\n\n"
        f"✨ {course['bonus']}"
    )
    await safe_edit(call, text, reply_markup=course_detail_kb(key))


@dp.callback_query(F.data.startswith("enroll_"))
async def enroll_start(call: CallbackQuery, state: FSMContext):
    key = call.data.replace("enroll_", "")
    await state.update_data(course_key=key, order_type="full")
    await state.set_state(Order.waiting_name)
    await safe_edit(
        call,
        "✍️ <b>Zo'r! Ro'yxatdan o'tamiz.</b>\n\n<b>Ism va familiyangizni</b> yozing:",
        reply_markup=cancel_kb()
    )


@dp.callback_query(F.data.startswith("bron_"))
async def bron_start(call: CallbackQuery, state: FSMContext):
    key = call.data.replace("bron_", "")
    await state.update_data(course_key=key, order_type="bron")
    await state.set_state(Order.waiting_name)
    await safe_edit(
        call,
        "🔒 <b>Ajoyib! Bron qilamiz.</b>\n\n<b>Ism va familiyangizni</b> yozing:",
        reply_markup=cancel_kb()
    )


async def get_name(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer("❌ Ism juda uzun. Iltimos, qisqaroq yozing.", reply_markup=cancel_kb())
        return
    await state.update_data(name=message.text)
    await state.set_state(Order.waiting_phone)
    await message.answer(
        "📱 <b>Telefon raqamingizni</b> yozing (yoki Telegram @username):",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )


async def get_phone(message: Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("❌ Raqam juda uzun. Iltimos, qayta yozing.", reply_markup=cancel_kb())
        return
    await state.update_data(phone=message.text)
    data = await state.get_data()
    course = COURSES.get(data["course_key"])
    order_type = data.get("order_type", "full")

    if order_type == "bron":
        summa = course["bron_price"]
        await state.set_state(Order.waiting_bron_screenshot)
        label = "🔒 <b>Bron uchun to'lov rekvizitlari</b>"
        note = (
            f"Bron summasi: <b>{summa}</b>\n\n"
            "To'lovdan keyin <b>skrinshot</b> yuboring 📸\n"
            "Sizni ro'yxatga olamiz va kurs boshlanishidan oldin xabar beramiz! 🤍"
        )
    else:
        summa = course["price"]
        await state.set_state(Order.waiting_screenshot)
        label = "💳 <b>To'liq to'lov rekvizitlari</b>"
        note = (
            f"To'lov summasi: <b>{summa}</b>\n\n"
            "To'lovdan keyin <b>skrinshot</b> yuboring 📸\n"
            "Tekshirib, kursning yopiq guruhiga qo'shamiz! 🔐"
        )

    payment_text = f"{label}\n\nKurs: <b>{course['name']}</b>\nSumma: <b>{summa}</b>\n\n"
    for method, details in PAYMENT_DETAILS.items():
        payment_text += f"<b>{method}:</b>\n{details}\n\n"
    payment_text += note

    await message.answer(payment_text, reply_markup=cancel_kb(), parse_mode="HTML")


async def get_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    course = COURSES.get(data["course_key"])
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    paid_clients.append({
        "name": data.get("name"),
        "phone": data.get("phone"),
        "course": course["name"],
        "type": "To'liq to'lov",
        "user_id": message.from_user.id,
        "username": message.from_user.username or "—",
        "date": now,
    })

    safe_name = html.escape(data.get("name") or "")
    safe_phone = html.escape(data.get("phone") or "")
    safe_username = html.escape(message.from_user.username or "—")
    caption = (
        f"💰 <b>YANGI TO'LIQ TO'LOV!</b>\n\n"
        f"👤 Ism: {safe_name}\n"
        f"📱 Telefon: {safe_phone}\n"
        f"📚 Kurs: {course['name']}\n"
        f"💵 Summa: {course['price']}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"👤 Username: @{safe_username}\n"
        f"📅 Sana: {now}"
    )
    await bot.send_photo(chat_id=ADMIN_GROUP_ID, photo=message.photo[-1].file_id,
                         caption=caption, parse_mode="HTML")
    await state.clear()
    await message.answer(
        "✅ <b>Rahmat! To'lovingiz qabul qilindi.</b>\n\n"
        "Tekshirib, tez orada kurs guruhiga qo'shamiz. Odatda 24 soat ichida 🤍",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Psixologga yozish", callback_data="contact")],
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")],
        ]), parse_mode="HTML"
    )


async def get_bron_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    course = COURSES.get(data["course_key"])
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    paid_clients.append({
        "name": data.get("name"),
        "phone": data.get("phone"),
        "course": course["name"],
        "type": "Bron",
        "user_id": message.from_user.id,
        "username": message.from_user.username or "—",
        "date": now,
    })

    safe_name = html.escape(data.get("name") or "")
    safe_phone = html.escape(data.get("phone") or "")
    safe_username = html.escape(message.from_user.username or "—")
    caption = (
        f"🔒 <b>YANGI BRON!</b>\n\n"
        f"👤 Ism: {safe_name}\n"
        f"📱 Telefon: {safe_phone}\n"
        f"📚 Kurs: {course['name']}\n"
        f"💵 Bron summasi: {course['bron_price']}\n"
        f"💰 Qolgan summa: ???\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"👤 Username: @{safe_username}\n"
        f"📅 Sana: {now}"
    )
    await bot.send_photo(chat_id=ADMIN_GROUP_ID, photo=message.photo[-1].file_id,
                         caption=caption, parse_mode="HTML")
    await state.clear()
    await message.answer(
        "🔒 <b>Bron tasdiqlandi!</b>\n\n"
        "Siz ro'yxatga olindingiz! Kurs boshlanishidan oldin siz bilan bog'lanamiz 🤍\n\n"
        "Qolgan to'lovni kurs boshlanishidan oldin amalga oshirasiz.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Psixologga yozish", callback_data="contact")],
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")],
        ]), parse_mode="HTML"
    )


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

    # Владельца кэшируем, если ещё не знаем
    if conn_id not in business_connections:
        try:
            bc = await bot.get_business_connection(conn_id)
            business_connections[conn_id] = bc.user.id
        except Exception:
            pass

    # Игнорируем сообщения от самого владельца бизнес-аккаунта
    owner_id = business_connections.get(conn_id)
    if owner_id and message.from_user and message.from_user.id == owner_id:
        return

    text_lower = (message.text or "").lower()
    if any(word in text_lower for word in TRIGGER_WORDS):
        await message.answer(DISCOUNT_WELCOME, reply_markup=discount_trigger_kb(), parse_mode="HTML")


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
