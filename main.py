import requests as r
import json
import telebot
import os
import sqlite3

db = sqlite3.connect("bot_database.db")


token = os.environ['motivate_bot_token']
bot = telebot.TeleBot(token)


# sql = "INSERT INTO users VALUES ('603970011', 0)"
# cursor.execute(sql)

def get_coins(id):
    sql = f"SELECT coins FROM users WHERE user_id={id}"
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

@bot.message_handler(commands=['start'])
def button(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_add_score = telebot.types.InlineKeyboardButton('Добавить баллы', callback_data='button_add_score')
    button_list_awards = telebot.types.InlineKeyboardButton('Список наград', callback_data='button_list_awards')
    button_add_award = telebot.types.InlineKeyboardButton('Добавить награду', callback_data='button_add_award')
    button_info = telebot.types.InlineKeyboardButton('Инфо', callback_data='button_info')
    markup.add(button_add_score, button_list_awards, button_add_award, button_info)
    bot.send_message(message.chat.id, "Главное меню", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'button_list_awards':
            print(call.message.chat.id)
            bot.send_message(call.message.chat.id, get_coins(call.message.chat.id))
        elif call.data == 'button_add_score':
            bot.send_message(call.message.chat.id, 'coin added')



bot.infinity_polling()