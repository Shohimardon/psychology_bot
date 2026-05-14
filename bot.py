import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_GROUP_ID, BOT_TOKEN, COURSES, PAYMENT_DETAILS, WELCOME_TEXT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

paid_clients: list[dict] = []


# ─── States ───────────────────────────────────────────────────────────────────
class Order(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_screenshot = State()      # to'liq to'lov
    waiting_bron_screenshot = State() # bron to'lovi


# ─── Klaviaturalar ────────────────────────────────────────────────────────────
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


# ─── Istalgan xabar → menyu ───────────────────────────────────────────────────
@dp.message()
async def any_message(message: Message, state: FSMContext):
    # Faqat shaxsiy chatda ishlaydi
    if message.chat.type != "private":
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

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


# ─── Asosiy menyu ─────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


@dp.callback_query(F.data == "show_courses")
async def show_courses(call: CallbackQuery):
    text = "📚 <b>Bizning kurslar:</b>\n\nBatafsil ma'lumot uchun kursni tanlang 👇"
    await call.message.edit_text(text, reply_markup=courses_kb(), parse_mode="HTML")


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
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")


@dp.callback_query(F.data == "contact")
async def show_contact(call: CallbackQuery):
    text = (
        "📞 <b>Psixolog bilan bog'lanish</b>\n\n"
        "Shaxsiy savollaringiz bo'lsa yoki konsultatsiya olmoqchi bo'lsangiz:\n\n"
        "👩‍💼 @OybarchinObidova\n\n"  # ← singilingizning username ini almashtiring
        "Bir necha soat ichida javob beramiz 🤍"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")],
    ])
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")


# ─── Kurs tafsilotlari ────────────────────────────────────────────────────────
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
    await call.message.edit_text(text, reply_markup=course_detail_kb(key), parse_mode="HTML")


# ══════════════════════════════════════════════════════
#  ✅ TO'LIQ TO'LOV FLOWI
# ══════════════════════════════════════════════════════

@dp.callback_query(F.data.startswith("enroll_"))
async def enroll_start(call: CallbackQuery, state: FSMContext):
    key = call.data.replace("enroll_", "")
    await state.update_data(course_key=key, order_type="full")
    await state.set_state(Order.waiting_name)
    await call.message.edit_text(
        "✍️ <b>Zo'r! Ro'yxatdan o'tamiz.</b>\n\n"
        "<b>Ism va familiyangizni</b> yozing:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )


# ══════════════════════════════════════════════════════
#  🔒 BRON FLOWI
# ══════════════════════════════════════════════════════

@dp.callback_query(F.data.startswith("bron_"))
async def bron_start(call: CallbackQuery, state: FSMContext):
    key = call.data.replace("bron_", "")
    await state.update_data(course_key=key, order_type="bron")
    await state.set_state(Order.waiting_name)
    await call.message.edit_text(
        "🔒 <b>Ajoyib! Bron qilamiz.</b>\n\n"
        "<b>Ism va familiyangizni</b> yozing:",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )


# ─── Umumiy: ism ──────────────────────────────────────────────────────────────
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order.waiting_phone)
    await message.answer(
        "📱 <b>Telefon raqamingizni</b> yozing (yoki Telegram @username):",
        reply_markup=cancel_kb(), parse_mode="HTML"
    )


# ─── Umumiy: telefon → rekvizitlar ────────────────────────────────────────────
async def get_phone(message: Message, state: FSMContext):
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


# ─── To'liq to'lov skrinshoti ─────────────────────────────────────────────────
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

    caption = (
        f"💰 <b>YANGI TO'LIQ TO'LOV!</b>\n\n"
        f"👤 Ism: {data.get('name')}\n"
        f"📱 Telefon: {data.get('phone')}\n"
        f"📚 Kurs: {course['name']}\n"
        f"💵 Summa: {course['price']}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"👤 Username: @{message.from_user.username or '—'}\n"
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


# ─── Bron skrinshoti ──────────────────────────────────────────────────────────
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

    caption = (
        f"🔒 <b>YANGI BRON!</b>\n\n"
        f"👤 Ism: {data.get('name')}\n"
        f"📱 Telefon: {data.get('phone')}\n"
        f"📚 Kurs: {course['name']}\n"
        f"💵 Bron summasi: {course['bron_price']}\n"
        f"💰 Qolgan summa: ???\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"👤 Username: @{message.from_user.username or '—'}\n"
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


# ─── Bekor qilish ─────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "cancel")
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "❌ Bekor qilindi.\n\nMenyuga qaytish uchun tugmani bosing 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")]
        ])
    )


# ─── Ishga tushirish ──────────────────────────────────────────────────────────
async def main():
    logger.info("Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

