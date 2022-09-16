import time

import telebot
import os
import random

from telebot import types

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)


test_list = ["d6287ca146f235564732a78ea9ad0a3665830f5d6cd71ea7f0e98e901ccc97a2",
			 "3ca701cbe6027ad9d882dd794a4421956648dcb1d284b79cfc65ba74a9e2fa7a",
			 "fb10f00379ee39ba194b1e632cf756e64dd5cfa0cdb4eb88e03ee7a977292616",
			 "2df5c6319d6086633e90955f833cf52083863a1efe6b16c0c33fade14b3dba7f"]

def prepare_list_of_links(tx_list: list) -> str:
	result_list = ''
	for tx in tx_list:
		result_list += f'[{tx[0:8]}](https://waxblock.io/transaction/{tx})\n'
	return result_list


@bot.message_handler(commands=['link'])
def send_link(message):
	bot.send_message(message.chat.id,
		f"NFTs were sent. Here are TX links:\n"
		f"{prepare_list_of_links(test_list)}",
		parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['timer'])
def timer(message):
	bot.send_message(message.chat.id,
		f"started timer for 5 seconds",)
	time.sleep(5)
	bot.send_message(message.chat.id,
		f"timer stopped",)

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/welcome.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)

	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("🎲 Рандомное число")
	item2 = types.KeyboardButton("😊 Как дела?")

	markup.add(item1, item2)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == '🎲 Рандомное число':
			bot.send_message(message.chat.id, str(random.randint(0,100)))
		elif message.text == '😊 Как дела?':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
			item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

			markup.add(item1, item2)

			bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
		else:
			bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Бывает 😢')

			# remove inline buttons
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
				reply_markup=None)

			# show alert
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

	except Exception as e:
		print(repr(e))


# RUN
print("Running the bot")
bot.polling(none_stop=True)
