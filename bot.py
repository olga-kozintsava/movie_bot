from logging.handlers import RotatingFileHandler

import psycopg2
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from config import TOKEN, db_name, db_user, db_host, db_password

logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('bot.log', maxBytes=2000, backupCount=2)
logger.addHandler(handler)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

inline_btn_1 = InlineKeyboardButton('Космос', callback_data='space')
inline_btn_2 = InlineKeyboardButton('Поломать голову', callback_data='brainstorm')
inline_btn_3 = InlineKeyboardButton('Мистика', callback_data='horror')
inline_btn_4 = InlineKeyboardButton('Юмор', callback_data='humor')
inline_btn_5 = InlineKeyboardButton('Драма', callback_data='dram')
inline_btn_6 = InlineKeyboardButton('Приключения', callback_data='adventure')
inline_btn_7 = InlineKeyboardButton('Триллер', callback_data='thriller')
inline_btn_8 = InlineKeyboardButton('Криминал', callback_data='criminall')
inline_btn_9 = InlineKeyboardButton('Позновательное', callback_data='educational')
inline_kb = InlineKeyboardMarkup(row_width=1)
inline_kb.add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5, inline_btn_6, inline_btn_7,
              inline_btn_8, inline_btn_9)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_name = message.from_user.first_name
    await bot.send_message(
        message.from_user.id,
        text='Приветствую {}! Выбери интересующую категорию, а я подберу тебе фильм)'.format(user_name),
        reply_markup=inline_kb)



@dp.callback_query_handler(lambda c: c.data)
async def process_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == 'back':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            text='Выбери интересующую категорию, а я подберу тебе фильм)',
            reply_markup=inline_kb
        )
    else:
        movie = search_movie(data)
        choice = InlineKeyboardMarkup()
        for item in movie:
            choice.add(InlineKeyboardButton(text=item[0], url=item[1]))
        choice.add(InlineKeyboardButton(
            text=emoji.emojize(':arrow_left:') + ' К списку категорий',
            callback_data='back')
        )
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            text='Вот что удалось найти по твоему запросу:',
            reply_markup=choice
        )


def search_movie(style):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        cursor = conn.cursor()
        cursor.execute('SELECT name, link FROM movie WHERE style = %s', (style,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except (Exception, psycopg2.Error) as error:
        logger.error(error, exc_info=True)


if __name__ == '__main__':
    executor.start_polling(dp)
