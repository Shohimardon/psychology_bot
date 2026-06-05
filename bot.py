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
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_GROUP_ID, BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ─── Текст курса ─────────────────────────────────────

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
    "✨ Tasdiqlangach kurs ochiladi 🤍"
)

# ─── States ──────────────────────────────────────────

class Order(StatesGroup):
    waiting_screenshot = State()
    waiting_name = State()
    waiting_phone = State()

# ─── Keyboards ───────────────────────────────────────

def pay_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 To'ladim — chek yuborish", callback_data="paid")],
    ])

def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ])

# ─── Helpers ─────────────────────────────────────────

async def safe_edit(call: CallbackQuery, text: str, reply_markup=None):
    try:
        await call.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")

async def show_lead(message: Message):
    await message.answer(LEAD_TEXT, reply_markup=pay_kb(), parse_mode="HTML")

# ─── Handlers ────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    args = message.text.split()
    if len(args) > 1 and args[1] == "lead":
        await state.update_data(source="lead")
    await show_lead(message)


@dp.message()
async def any_message(message: Message, state: FSMContext):
    if message.chat.type != "private":
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

    # любое другое сообщение → показываем курс
    await show_lead(message)


@dp.callback_query(F.data == "paid")
async def on_paid(call: CallbackQuery, state: FSMContext):
    await state.set_state(Order.waiting_screenshot)
    await safe_edit(
        call,
        "📸 Ajoyib! Endi to'lov <b>skrinshotini</b> yuboring:",
        reply_markup=cancel_kb()
    )


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

    tariff = "FOTIHA kursi — 99 000 so'm"
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


@dp.callback_query(F.data == "cancel")
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit(call, LEAD_TEXT, reply_markup=pay_kb())


# ─── Entry point ─────────────────────────────────────

async def main():
    logger.info("Lead bot ishga tushdi!")
    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
