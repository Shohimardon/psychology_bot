import os

# ══════════════════════════════════════════════════════
#  🔧 SOZLAMALAR — SHU YERDA O'ZGARTIRING
# ══════════════════════════════════════════════════════

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "-1001234567890"))

# ══════════════════════════════════════════════════════
#  📚 KURSLAR
# ══════════════════════════════════════════════════════
COURSES = {
    "standart": {
        "emoji": "🌸",
        "name": "Standart",
        "description": (
            "O'zingiz ustida ishlashni boshlash uchun asosiy tarif.\n\n"
            "Nimalar kiradi:\n"
            "• 8 ta jonli darslik\n"
            "• Kurator hizmatidan foydalanish imkoniyati\n"
            "• Muloqat chat guruhga kirish\n"
            "• Kursga 3 oylik dostup"
        ),
        "duration": "8 ta jonli darslik",
        "format": "Onlayn",
        "old_price": "990 000 so'm",
        "price": "299 000 so'm",
        "bonus": "🔥 Aksiya! Narx 990 000 dan 299 000 so'mga tushirildi",
    },
    "vip": {
        "emoji": "👑",
        "name": "VIP",
        "description": (
            "Barcha imtiyozlar bilan maksimal tarif!\n\n"
            "Nimalar kiradi:\n"
            "• 8 ta jonli darslik\n"
            "• Kurator hizmatidan foydalanish imkoniyati\n"
            "• Muloqat chat guruhga kirish\n"
            "• Keyingi kursga 30% chegirma vaucher 🎟\n"
            "• Kursga 6 oylik dostup"
        ),
        "duration": "8 ta jonli darslik",
        "format": "Onlayn",
        "old_price": "1 899 000 so'm",
        "price": "599 000 so'm",
        "bonus": "🔥 Aksiya! Narx 1 899 000 dan 599 000 so'mga tushirildi",
    },
}

# ══════════════════════════════════════════════════════
#  💳 TO'LOV REKVIZITLARI
# ══════════════════════════════════════════════════════
PAYMENT_DETAILS = {
    "💳 Karta": "5614 6810 1232 3550\nEgasi: Sharopova Jamila",
    # "📱 Click": "havolangiz",
}

# ══════════════════════════════════════════════════════
#  👋 SALOMLASHUV MATNI
# ══════════════════════════════════════════════════════
WELCOME_TEXT = (
    "👋 <b>Assalomu alaykum! Xush kelibsiz!</b>\n\n"
    "Men psixolog yordamchisiman 🤍\n\n"
    "Bu yerda siz:\n"
    "• Kurslar va narxlar haqida bilib olishingiz\n"
    "• Ro'yxatdan o'tib, onlayn to'lashingiz\n"
    "• Savol berishingiz mumkin\n\n"
    "Qiziqtirgan bo'limni tanlang 👇"
)
