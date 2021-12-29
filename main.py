import requests as r
import json
import telebot
import os

token = os.environ['motivate_bot_token']
bot = telebot.TeleBot(token)

with open('coins.txt') as f:
    coins = f.read()
    print(f'{coins=}')

def write_coins(coins):
    f = open('coins.txt', 'w')
    f.write(str(int(coins)+1))
    f.close()
    return coins

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['button'])
def button(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_add_score = telebot.types.InlineKeyboardButton('Добавить баллы', callback_data='button_add_score')
    button_list_awards = telebot.types.InlineKeyboardButton('Список наград', callback_data='button_list_awards')
    button_add_award = telebot.types.InlineKeyboardButton('Добавить награду', callback_data='button_add_award')
    button_info = telebot.types.InlineKeyboardButton('Инфо', callback_data='button_info')
    markup.add(button_add_score, button_list_awards, button_add_award, button_info)
    bot.send_message(message.chat.id, "Howdy, how are you doing?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'button_list_awards':
            bot.send_message(call.message.chat.id, str(coins))
        elif call.data == 'button_add_score':
            write_coins(coins)
            bot.send_message(call.message.chat.id, 'coin added')



bot.infinity_polling()