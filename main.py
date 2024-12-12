import asyncio
import logging
import json
import os
from pathlib import Path
from time import time

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from parsers import scrape_auto_ria


TOKEN = '7738647257:AAH8NwOksVaOgt8PXvuuqxKDZv3k0R-PM34'
JSON_FILE = "sent_cars.json"
CHECK_INTERVAL = 900


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

last_check_time = 0


def load_sent_cars() -> dict:
    if not Path(JSON_FILE).exists():
        logging.info("JSON файл не існує. Створюємо новий.")
        return {}
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logging.error("Помилка зчитування JSON-файлу. Використовується порожній список.")
            return {}


def save_sent_cars(sent_cars: dict) -> None:
    """
    Зберігає список відправлених автомобілів у JSON-файл.
    """
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(sent_cars, f, ensure_ascii=False, indent=2)
    logging.info("Оновлено JSON файл.")


async def send_car_notification(message: Message, car: dict, reason: str) -> None:
    """
    Надсилає повідомлення з інформацією про автомобіль.
    """
    if reason == "Видалено":
        caption = f"<b>{car.get('title', 'Невідомо')}</b>\nАвтомобіль було видалено з сайту."
    else:
        caption = (
            f"<b>{car.get('title')}</b>\n"
            f"Ціна: {car.get('price')}\n"
            f"Пробіг: {car.get('mileage')}\n"
            f"Причина: {reason}\n"
            f"<a href='{car.get('auction_link')}'>Перейти на аукціон</a>"
        )

    photos = car.get("photos", [])
    if photos and reason != "Видалено":
        try:
            await bot.send_photo(chat_id=message.chat.id, photo=photos[0], caption=caption)
            logging.info(f"Відправлено для автомобіля: {car.get('title')}")
        except Exception as e:
            logging.error(f"Помилка: {e}")
    else:
        try:
            await bot.send_message(chat_id=message.chat.id, text=caption)
            logging.info(f"Відправлено повідомлення для автомобіля: {car.get('title', 'Невідомо')}")
        except Exception as e:
            logging.error(f"Помилка при надсиланні тексту: {e}")


def file_was_modified() -> bool:
    """
    Перевіряє, чи змінено JSON-файл (порівнює час зміни файлу).
    """
    global last_check_time
    current_time = os.path.getmtime(JSON_FILE)
    if current_time > last_check_time:
        last_check_time = current_time
        logging.info("JSON файл було змінено.")
        return True
    return False


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}! Бот запущено.")
    sent_cars = load_sent_cars()  # Завантаження вже відправлених автомобілів

    while True:
        # Якщо JSON файл змінено, перезавантажуємо список відправлених автомобілів
        if file_was_modified():
            sent_cars = load_sent_cars()

        cars = scrape_auto_ria()  # Отримуємо нові автомобілі
        current_car_ids = {car["auction_link"] for car in cars}

        # Перевіряємо нові автомобілі та зміну ціни
        for car in cars:
            car_id = car.get("auction_link")
            if car_id not in sent_cars:
                # Новий автомобіль
                sent_cars[car_id] = car
                await send_car_notification(message, car, "Новий автомобіль")
            elif sent_cars[car_id]["price"] != car["price"]:
                # Зміна ціни
                sent_cars[car_id] = car
                await send_car_notification(message, car, "Зміна ціни")

        # Перевіряємо видалення автомобілів
        for car_id in list(sent_cars.keys()):
            if car_id not in current_car_ids:
                deleted_car = sent_cars.pop(car_id)
                await send_car_notification(message, deleted_car, "Видалено")

        # Зберігаємо оновлений список автомобілів
        save_sent_cars(sent_cars)

        await asyncio.sleep(CHECK_INTERVAL)


async def main() -> None:
    async with bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
