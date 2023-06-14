# coding: utf8
import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
from scraper import get_new_offers
from aiogram.dispatcher.filters import Text
from background import keep_alive

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Новые заказы").add("Последние 5 заказов").add("Последние 10 заказов")
    await message.answer('Лента', reply_markup=keyboard)


@dp.message_handler(commands="all_offers")
async def get_all_news(message: types.Message):
    with open('dictionary.json') as file:
        offers_dict = json.load(file)
    for k, v in sorted(offers_dict.items()):
        offers = f"Наименование: <b>{v['name']}</b>\n" \
                 f"Цена: <b>{v['price']}</b>\n" \
                 f"Ссылка: {v['link']}"
        await message.answer(offers)


@dp.message_handler(Text(equals="Последние 5 заказов"))
async def get_last_five_offers(message: types.Message):
    with open('dictionary.json') as file:
        offers_dict = json.load(file)
    for k, v in sorted(offers_dict.items())[-5:]:
        offers = f"Наименование: <b>{v['name']}</b>\n" \
                 f"Цена: <b>{v['price']}</b>\n" \
                 f"Ссылка: {v['link']}"
        await message.answer(offers)


@dp.message_handler(Text(equals="Последние 10 заказов"))
async def get_last_ten_offers(message: types.Message):
    with open('dictionary.json') as file:
        offers_dict = json.load(file)
    for k, v in sorted(offers_dict.items())[-10:]:
        offers = f"Наименование: <b>{v['name']}</b>\n" \
                 f"Цена: <b>{v['price']}</b>\n" \
                 f"Ссылка: {v['link']}"
        await message.answer(offers)


@dp.message_handler(Text(equals="Новые заказы"))
async def get_fresh_offers(message: types.Message):
    fresh_offers = get_new_offers()

    if len(fresh_offers) >= 1:
        for k, v in sorted(fresh_offers.items()):
            offers = f"Наименование: <b>{v['name']}</b>\n" \
                     f"Цена: <b>{v['price']}</b>\n" \
                     f"Ссылка: {v['link']}"
            await message.answer(offers)
    else:
        await message.answer('Нет новых заказов')


async def offers_every_hour():
    while True:
        fresh_offers = get_new_offers()
        if len(fresh_offers) >= 1:
            await bot.send_message(user_id, '❗❗❗Новые заказы❗❗❗')
            for k, v in sorted(fresh_offers.items()):
                offers = f"Наименование: <b>{v['name']}</b>\n" \
                         f"Цена: <b>{v['price']}</b>\n" \
                         f"Ссылка: {v['link']}"
                await bot.send_message(user_id, offers)

        await asyncio.sleep(3600)


keep_alive()
def main():
    loop = asyncio.get_event_loop()
    loop.create_task(offers_every_hour())
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
