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
    if questions["results"]:
        question_id = questions["results"][0]["id"]
        responce = requests.get(
            f"http://127.0.0.1:8000/api-test/answer/{question_id}/",
        )
        for answer in responce.json():
            answer_btn = aiogram.types.InlineKeyboardButton(
                answer["text"],
                callback_data=f"ans {question_id} {answer['id']}",
            )
            buttons.add(answer_btn)

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
        if page == pages_count:
            result = aiogram.types.InlineKeyboardButton(
                "РЕЗУЛЬТАТ",
                callback_data=f"result {test_id}",
            )
            buttons.add(result)

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


@dp.callback_query_handler(lambda callback: callback.data.startswith("ans"))
async def answer_callback(callback):
    qu_id, ans_id = callback.data.split()[1:]
    data = {
        "user": callback.from_user.id,
        "question": qu_id,
        "answer": ans_id,
    }
    requests.get(
        "http://127.0.0.1:8000/api-test/answeruser/",
        json=data,
    )
    await bot.edit_message_text(
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        text=callback.message.text + "\nсохранено",
        reply_markup=callback.message.reply_markup,
    )


@dp.callback_query_handler(lambda callback: callback.data.startswith("res"))
async def result_callback(callback):
    test_id, *_ = callback.data.split()[1:]
    user_id = callback.from_user.id
    responce = requests.get(
        f"http://127.0.0.1:8000/api-test/answeruser/{test_id}/{user_id}/",
    )
    result = int(responce.json()["result"])
    if 70 <= result <= 80:
        verdict = "I"
    elif 57 <= result <= 69:
        verdict = "II"
    elif 44 <= result <= 56:
        verdict = "III"
    elif 29 <= result <= 33:
        verdict = "IV"
    else:
        verdict = "V"

    await bot.edit_message_text(
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        text=verdict,
    )


@dp.callback_query_handler(lambda callback: callback.data == "start")
async def start_callback(callback):
    await start(callback.message, new=False)


@dp.callback_query_handler(lambda callback: callback.data.startswith("go"))
async def go_callback(callback):
    item, item_id = callback.data.split()[1:]
    if item == "t":
        await test_questions(callback.message, item_id)


aiogram.executor.start_polling(dp, skip_updates=True)
