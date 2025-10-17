from aiogram import types
from aiogram.types import Message

def register_order_handlers(dp):
    @dp.message(lambda message: message.text == "📞 Place Order")
    async def place_order(message: Message):
        await message.answer("📞 Your order has been placed! Thank you for choosing Fast Food bot!")