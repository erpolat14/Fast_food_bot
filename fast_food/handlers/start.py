from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup

# --- Меню клавиатуры ---
menu_buttons = [
    ["🍔 Burger", "🍕 Pizza"],
    ["🥤 Drinks", "🍟 Fries"],
    ["📞 Place Order"]
]
menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)

def register_start_handlers(dp):
    @dp.message(Command("start"))
    async def start_cmd(message: Message):
        await message.answer(
            f"Hello, {message.from_user.first_name}! 👋\nWelcome to the Fast Food bot!\n"
            "Choose an item from the menu below 👇",
            reply_markup=menu_keyboard
        )