import requests as r
import json
import telebot
import os
import sqlite3

conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()

token = os.environ['motivate_bot_token']
bot = telebot.TeleBot(token)

with open('coins.txt') as f:
    coins = f.read()

def write_coins(coins):
    with open('coins.txt', 'w') as f:
        f.write(str(int(coins)+1))


@bot.message_handler(commands=['start'])
def button(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_add_score = telebot.types.InlineKeyboardButton('Добавить баллы', callback_data='button_add_score')
    button_list_awards = telebot.types.InlineKeyboardButton('Список наград', callback_data='button_list_awards')
    button_add_award = telebot.types.InlineKeyboardButton('Добавить награду', callback_data='button_add_award')
    button_info = telebot.types.InlineKeyboardButton('Инфо', callback_data='button_info')
    markup.add(button_add_score, button_list_awards, button_add_award, button_info)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'button_list_awards':
            bot.send_message(call.message.chat.id, str(coins))
        elif call.data == 'button_add_score':
            write_coins(coins)
            bot.send_message(call.message.chat.id, 'coin added')



bot.infinity_polling()