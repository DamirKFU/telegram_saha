import os

import aiogram
import dotenv
import requests


__all__ = []

dotenv.load_dotenv()

bot = aiogram.Bot(os.getenv("TOKEN"), parse_mode="MARKDOWN")
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message, page=1, new=True):
    responce = requests.get(
        "http://127.0.0.1:8000/api-test/tests/",
        params={"page": page},
    )

    tests = responce.json()
    pages_count = tests["count"]
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1

    buttons = aiogram.types.InlineKeyboardMarkup()
    left_button = aiogram.types.InlineKeyboardButton(
        "←",
        callback_data=f"test {left}",
    )
    page_button = aiogram.types.InlineKeyboardButton(
        f"{str(page)}/{str(pages_count)}",
        callback_data="_",
    )
    right_button = aiogram.types.InlineKeyboardButton(
        "→",
        callback_data=f"test {right}",
    )
    go_button = aiogram.types.InlineKeyboardButton(
        "ПРОЙТИ",
        callback_data=f"go t {tests['results'][0]['id']}",
    )
    buttons.add(left_button, page_button, right_button)
    buttons.add(go_button)
    if not tests["results"]:
        await bot.send_message(
            text="Пусто",
            chat_id=message.chat.id,
            reply_markup=buttons,
        )

    elif new:
        await bot.send_message(
            text=tests["results"][0]["name"],
            chat_id=message.chat.id,
            reply_markup=buttons,
        )
    else:
        await bot.edit_message_text(
            message_id=message.message_id,
            chat_id=message.chat.id,
            text=tests["results"][0]["name"],
            reply_markup=buttons,
        )


async def test_questions(message, test_id, page=1):
    responce = requests.get(
        f"http://127.0.0.1:8000/api-test/questions/{test_id}/",
        params={"page": page},
    )

    questions = responce.json()
    pages_count = questions["count"]
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1

    buttons = aiogram.types.InlineKeyboardMarkup()
    left_button = aiogram.types.InlineKeyboardButton(
        "←",
        callback_data=f"que {test_id} {left}",
    )
    page_button = aiogram.types.InlineKeyboardButton(
        f"{str(page)}/{str(pages_count)}",
        callback_data="_",
    )
    right_button = aiogram.types.InlineKeyboardButton(
        "→",
        callback_data=f"que {test_id} {right}",
    )
    go_button = aiogram.types.InlineKeyboardButton(
        "НАЗАД",
        callback_data="start",
    )
    buttons.add(left_button, page_button, right_button)
    buttons.add(go_button)

    if not questions["results"]:
        back = aiogram.types.InlineKeyboardMarkup()
        back.add(go_button)
        await bot.edit_message_text(
            message_id=message.message_id,
            text="Пусто",
            chat_id=message.chat.id,
            reply_markup=back,
        )
    else:
        await bot.edit_message_text(
            message_id=message.message_id,
            chat_id=message.chat.id,
            text=questions["results"][0]["text"],
            reply_markup=buttons,
        )


@dp.callback_query_handler(lambda callback: callback.data.startswith("test"))
async def page_test_callback(callback):
    page = int(callback.data.split()[1])
    await start(callback.message, page=page, new=False)


@dp.callback_query_handler(lambda callback: callback.data.startswith("que"))
async def page_question_callback(callback):
    test_id, page = callback.data.split()[1:]
    await test_questions(callback.message, test_id, page=int(page))


@dp.callback_query_handler(lambda callback: callback.data == "start")
async def start_callback(callback):
    await start(callback.message, new=False)


@dp.callback_query_handler(lambda callback: callback.data.startswith("go"))
async def go_callback(callback):
    item, item_id = callback.data.split()[1:]
    if item == "t":
        await test_questions(callback.message, item_id)


aiogram.executor.start_polling(dp, skip_updates=True)
