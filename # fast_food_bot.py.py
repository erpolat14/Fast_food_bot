from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import asyncio

TOKEN = "8336802811:AAEodtJlk7nJGNN53oVCA-HAGAiVdK_nJ5U"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Paydalanıwshı Tańlaytuǵın til
user_language = {}

# --- Baqalar ---
prices = {
    "🍔 Burger": "25 000 so‘m",
    "🍕 Pizza": "30 000 so‘m",
    "🥤 Ichimliklar": "10 000 so‘m",
    "🍟 Fri kartoshka": "12 000 so‘m",
    "🥤 Ishimlikler": "10 000 so‘m"  # Qaraqalpaqsha til Ushın
}

# --- 1. Til tanlash menyusi ---
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 O‘zbek tili"), KeyboardButton(text="🇶🇷 Qaraqalpaq tili")]
    ],
    resize_keyboard=True
)

# --- O‘zbekcha menyu ---
menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Burger – 25 000 so‘m"), KeyboardButton(text="🍕 Pizza – 30 000 so‘m")],
        [KeyboardButton(text="🥤 Ichimliklar – 10 000 so‘m"), KeyboardButton(text="🍟 Fri kartoshka – 12 000 so‘m")],
        [KeyboardButton(text="📞 Buyurtma berish")]
    ],
    resize_keyboard=True
)

# --- Qaraqalpaqcha menyu ---
menu_qq = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Burger – 25 000 so'm"), KeyboardButton(text="🍕 Pizza – 30 000 so'm")],
        [KeyboardButton(text="🥤 Ishimlikler – 10 000 so'm"), KeyboardButton(text="🍟 Fri kartoshka – 12 000 so'm")],
        [KeyboardButton(text="📞 Tapsiris beriw")]
    ],
    resize_keyboard=True
)

# --- /start komandasi ---
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "👋 Tilni tanlang / Tildi saylań:",
        reply_markup=language_keyboard
    )

# --- Til tańlaw ---
@dp.message(F.text.in_(["🇺🇿 O‘zbek tili", "🇶🇷 Qaraqalpaq tili"]))
async def select_language(message: Message):
    if "O‘zbek" in message.text:
        user_language[message.from_user.id] = "uz"
        await message.answer("✅ Til tanlandi: O‘zbek tili.\nMenyudan taomni tanlang 👇", reply_markup=menu_uz)
    else:
        user_language[message.from_user.id] = "qq"
        await message.answer("✅ Til saylandi: Qaraqalpaq tili.\nMenyu'dan taǵamdi saylań 👇", reply_markup=menu_qq)

# --- Taom tanlash ---
@dp.message(F.text.regexp(r"🍔|🍕|🥤|🍟"))
async def select_food(message: Message):
    lang = user_language.get(message.from_user.id, "qq")

    
    for food, price in prices.items():
        if food in message.text:
            selected = f"{food} – {price}"
            break
    else:
        selected = message.text

    if lang == "uz":
        await message.answer(f"Siz tanladingiz: {selected} ✅\nBuyurtmani tasdiqlash uchun 📞 'Buyurtma berish' tugmasini bosing.")
    else:
        await message.answer(f"Siz tańladińız: {selected} ✅\nTapsiris tastıyqlaw ushın 📞 'Tapsiris beriw' túymesin basiń.")

# --- Tapsiris beriw ushin tel nomer soraw ---
@dp.message(F.text.in_(["📞 Buyurtma berish", "📞 Tapsiris beriw"]))
async def order(message: Message):
    lang = user_language.get(message.from_user.id, "qq")
    contact_button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Kontakt yuborish", request_contact=True)],
            [KeyboardButton(text="⬅️ Ortga qaytish" if lang == "uz" else "⬅️ Artqa qaytıw")]
        ],
        resize_keyboard=True
    )
    if lang == "uz":
        await message.answer("Buyurtmani tasdiqlash uchun telefon raqamingizni yuboring 📱", reply_markup=contact_button)
    else:
        await message.answer("Tapsiristi tastıyqlaw ushın telefon nomerińizdi jiberiń 📱", reply_markup=contact_button)

# --- Lokaciyasın soraw ---
@dp.message(F.contact)
async def contact_received(message: Message):
    lang = user_language.get(message.from_user.id, "qq")
    phone = message.contact.phone_number
    name = message.from_user.full_name

    location_button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
            [KeyboardButton(text="⬅️ Ortga qaytish" if lang == "uz" else "⬅️ Artqa qaytıw")]
        ],
        resize_keyboard=True
    )

    if lang == "uz":
        await message.answer(f"✅ Rahmat, {name}!\nSizning raqamingiz: {phone}")
        await message.answer("Endi buyurtmani yetkazish uchun manzilingizni yuboring 📍", reply_markup=location_button)
    else:
        await message.answer(f"✅ Raxmet, {name}!\nSizsiń nomerińiz: {phone}")
        await message.answer("Endi tapsiris jetkiziwi ushın manzilińizdi jiberiń 📍", reply_markup=location_button)

# --- Lokaciyani qabıl etiw ---
@dp.message(F.location)
async def location_received(message: Message):
    lang = user_language.get(message.from_user.id, "qq")
    latitude = message.location.latitude
    longitude = message.location.longitude

    if lang == "uz":
        await message.answer(f"📍 Joylashuv qabul qilindi!\nKenglik: {latitude}\nUzunlik: {longitude}\nBuyurtmangiz yo‘lga chiqdi 🚗💨", reply_markup=menu_uz)
    else:
        await message.answer(f"📍 Manzil qabul etildi!\nEnligi: {latitude}\nUzunligi: {longitude}\nBuyurtma jetkizilmege tayın 🚗💨", reply_markup=menu_qq)

# --- Artqa qaytıw ---
@dp.message(F.text.in_(["⬅️ Ortga qaytish", "⬅️ Artqa qaytıw"]))
async def go_back(message: Message):
    lang = user_language.get(message.from_user.id, "qq")
    if lang == "uz":
        await message.answer("Asosiy menyu 👇", reply_markup=menu_uz)
    else:
        await message.answer("Tiykarǵi menyu 👇", reply_markup=menu_qq)

@dp.message()
async def unknown(message: Message):
    lang = user_language.get(message.from_user.id, "qq")
    if lang == "uz":
        await message.answer("Iltimos, menyudagi tugmalardan foydalaning 👇", reply_markup=menu_uz)
    else:
        await message.answer("Iltimas, menyudegi túymelerden paydalanıń 👇", reply_markup=menu_qq)

# --- Botdi iske túsirıw ---
async def main():
    print("🤖 Bot isge tústi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
