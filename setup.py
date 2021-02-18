import logging
import states as state
import graph
import requests
import config
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

response = ''
base = 'USD' #our base currency.this is the default dollar

resp_history = requests.get(config.urlhistory).json()

def get_request():
	global response
	response = requests.get(config.urlbase + base).json()

# handler for converting of currency with states. it waits for our message.
@dp.message_handler(lambda message: state.get_current_state(message.chat.id) == state.States.S_ENTER_CURRENCY.value)
async def currency_convert(message: types.Message):
	if message.text == '/cancel':
		await message.answer("OK\nTry /start")
		state.set_state(message.chat.id, state.States.S_START.value)
	else:
		global response
		global base
		lst = message.text.split() # 10 USD to CAD
		try:
			num = float(lst[0])
			curr = lst[3].upper()

			flag = False
			if base != lst[1].upper():
				base = lst[1].upper()
				get_request()
			for rate in response['rates']:
				if (curr == rate):
					value = response['rates'][curr] * num
					await message.answer(float('{:.3}'.format(value)))
					flag = True
					break
			if flag is False:
				await bot.send_message(message.chat.id, "This currency doesn't exist! Try again following the example:\
			\n10.3 USD to CAD\nOr /cancel")
		except Exception as e:
			await bot.send_message(message.chat.id, "Try again following the example:\
			\n10.3 USD to CAD\nOr /cancel")

#the same handler for currency list
@dp.message_handler(lambda message: state.get_current_state(message.chat.id) == state.States.S_BASE_CURRENCY.value)
async def list_indication(message: types.Message):
	if message.text == '/cancel':
		await message.answer("OK\nTry /start")
		state.set_state(message.chat.id, state.States.S_START.value)
	else:
		global response
		global base
		try:
			base = message.text.upper()
			get_request()
			msg = "1 " + response['base'] + " is:\n"
			for curr in response['rates']:
				msg += '\n' + curr + ': ' + str(float('{:.3}'.format(response['rates'][curr])))
			await message.answer(msg)
		except Exception as e:
			await bot.send_message(message.chat.id,"This currency doesn't exist!\nExample: EUR\
				\nType /cancel if you changed your mind")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.answer("Hi, I'm currency exchanger🤑\nCommand list:\
		\n/list - list of all available exchange rates\
		\n/exchange  - converts to the second currency with two decimal precision(choose to check)\
		\n/history -  return an image graph chart which shows the exchange rate graph/chart of the selected currency for the last 7 days\
		(Now just USD/CAD for 5 days)\
		\n/help - user's support.")

@dp.message_handler(commands=['list'])
async def send_list(message: types.Message):
	await message.answer("Please, indicate the currency☺️\
		\nType /cancel if you changed your mind")
	state.set_state(message.chat.id, state.States.S_BASE_CURRENCY.value)

@dp.message_handler(commands=['exchange'])
async def send_exchanger(message: types.Message):
	await bot.send_message(message.chat.id, "Specify the currency for conversion💶\
		\nExample:\n10 USD to CAD\
		\nType /cancel if you changed your mind")
	state.set_state(message.chat.id, state.States.S_ENTER_CURRENCY.value)

@dp.message_handler(commands=['history'])
async def send_graph(message: types.Message):
	await bot.send_photo(message.chat.id, photo=open('Graph.jpg', 'rb'))
	await bot.send_message(message.chat.id, "history USD/CAD for 5 days")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	await message.answer("Comming soon..")

@dp.message_handler()
async def send_unknown_message(message: types.Message):
	await message.answer("I don't know such a command🤷\nTry /start")

if __name__ == '__main__':
	get_request()
	executor.start_polling(dp, skip_updates=True)
