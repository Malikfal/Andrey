import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from parsers import get_map_first, get_map_second, get_russia_news, get_ukraine_news, transliterate
import datetime

my_secret = os.environ['Token']
bot = Bot(token=my_secret)
dp = Dispatcher(bot,storage=MemoryStorage())

class FSMadmin(StatesGroup):
	input = State()
 
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("👋 Дарова бот")
	btn2 = types.KeyboardButton("⚔️ Карта")
	btn4 = types.KeyboardButton("🇬🇧 Транслитерация")
	btn3 = types.KeyboardButton("📰 Новости")
	markup.add(btn1, btn2, btn4).row(btn3)
	await message.answer(text="Привет, что хочешь", reply_markup = markup)
	
@dp.message_handler(text='🇬🇧 Транслитерация',state=None)
async def translation(message: types.Message):
	await FSMadmin.input.set()
	await message.answer(text="Введи текст")

@dp.message_handler(state=FSMadmin.input)
async def end_translit(message: types.Message, state: FSMContext):
	await message.answer(transliterate(message.text))
	await state.finish()
	
@dp.message_handler(content_types=['text'])
async def func(message):
	if(message.text == "👋 Дарова бот"):
		await message.reply(text="Привет")
	elif(message.text == '⚔️ Карта'):
		image = get_map_first(str(datetime.datetime.now().date() - datetime.timedelta(days=2)))
		try:
			if image[-1] == 'g':
				listik = list(image)
				listik[-10] = '1'
				inline_btn_3 = types.InlineKeyboardButton('Карта неделю назад', callback_data='week ago')
				inline_kb = types.InlineKeyboardMarkup()
				inline_kb.add(inline_btn_3)
				await message.answer(text=''.join(listik), reply_markup = inline_kb)
			else:
				await message.answer(text='Новую карту ещё не завезли.')
		except:
			await message.answer(text='Новую карту ещё не завезли.')
	elif(message.text == '📰 Новости'):
		inline_btn_1 = types.InlineKeyboardButton('🇷🇺 Россия', callback_data='russia')
		inline_btn_2 = types.InlineKeyboardButton('🇺🇦 Украина', callback_data='ukraine')
		inline_kb = types.InlineKeyboardMarkup()
		inline_kb.add(inline_btn_1,inline_btn_2)
		await message.answer(text='Выберите новости:',reply_markup = inline_kb)

@dp.callback_query_handler(text='russia')
async def process_callback_button1(callback_query: types.CallbackQuery):
	await callback_query.message.answer(get_russia_news())
	await callback_query.answer()
	
@dp.callback_query_handler(text='ukraine')
async def process_callback_button2(callback_query: types.CallbackQuery):
	await callback_query.message.answer(get_ukraine_news())
	await callback_query.answer()

@dp.callback_query_handler(text='week ago')
async def process_callback_button3(callback_query: types.CallbackQuery):
	image = get_map_first(str(datetime.datetime.now().date() - datetime.timedelta(days=7)))
	try:
		if image[-1] == 'g':
			listik = list(image)
			listik[-10] = '1'
			inline_btn_3 = types.InlineKeyboardButton('Карта неделю назад', callback_data='week ago')
			inline_kb = types.InlineKeyboardMarkup()
			inline_kb.add(inline_btn_3)
			await callback_query.message.answer(text=''.join(listik), reply_markup = inline_kb)
		else:
			await callback_query.message.answer(text='Карты уже нету.')
	except:
		await callback_query.message.answer(text='Карты уже нету.')
	await callback_query.answer()
	
executor.start_polling(dp, skip_updates=True)
