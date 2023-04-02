import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from parsers import Parsers

#my_secret = os.environ['Token']

pars = Parsers()
pars.get_map()

bot = Bot(token="TOKEN")
dp = Dispatcher(bot,storage=MemoryStorage())

class FSMadmin(StatesGroup):
    input = State()
    input2 = State()
    

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Привет Андрей")
    btn2 = types.KeyboardButton("⚔️ Карта")
    btn4 = types.KeyboardButton("📰 Новости")
    btn3 = types.KeyboardButton("🐱 Опа")
    markup.add(btn1, btn2, btn4).row(btn3)
    await message.answer(text="Привет, что хочешь?", reply_markup = markup)


@dp.message_handler(content_types=['text'])
async def func(message):
    if (message.text == "👋 Привет Андрей"):
        await message.reply(text="Привет")

    elif (message.text == '⚔️ Карта'):
        try:
            photo = open('images/map2.png', 'rb')
            await bot.send_photo(message.chat.id,photo)
            photo.close()
        except Exception as exc:
            print(exc)
            await message.answer(text='Новую карту ещё не завезли.')

    elif (message.text == '🐱 Опа'):
        inline_btn_1 = types.InlineKeyboardButton('Хочу ещё', callback_data='next_image')
        inline_kb = types.InlineKeyboardMarkup()
        inline_kb.add(inline_btn_1)
        pars.cotochel()
        photo= open('images/cotochel.png', 'rb')
        await bot.send_photo(photo=photo, chat_id=message.chat.id ,reply_markup=inline_kb)
        photo.close()

    elif (message.text == "📰 Новости"):
        inline_btn_1 = types.InlineKeyboardButton('Следующая новость', callback_data='next_news')
        inline_kb = types.InlineKeyboardMarkup()
        inline_kb.add(inline_btn_1)
        await message.answer(text=pars.news(), reply_markup=inline_kb)


@dp.callback_query_handler(text='next_image')
async def process_callback_button1(callback_query: types.CallbackQuery):
    inline_btn_1 = types.InlineKeyboardButton('Нужно больше кошек', callback_data='next_image')
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(inline_btn_1)
    pars.cotochel()
    photo= open('images/cotochel.png', 'rb')
    await callback_query.bot.send_photo(photo=photo, chat_id=callback_query.message.chat.id ,reply_markup=inline_kb)
    await callback_query.answer()

@dp.callback_query_handler(text='next_news')
async def process_callback_button1(callback_query: types.CallbackQuery):
    inline_btn_1 = types.InlineKeyboardButton('Следующая новость', callback_data='next_news')
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(inline_btn_1)
    await callback_query.bot.send_message(text=pars.next_news(), chat_id=callback_query.message.chat.id ,reply_markup=inline_kb)
    await callback_query.answer()


executor.start_polling(dp, skip_updates=True)
