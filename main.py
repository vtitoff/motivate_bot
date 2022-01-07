import requests as r
import json
import telebot
import os
import sqlite3

token = os.environ['motivate_bot_token']
bot = telebot.TeleBot(token)


def get_coins(id):
    db = sqlite3.connect("bot_database.db")
    sql = f"SELECT coins FROM users WHERE user_id={id}"
    cursor = db.cursor()
    cursor.execute(sql)
    for x in cursor.fetchone():
        return x


def add_coins(id):
    db = sqlite3.connect("bot_database.db")
    cursor = db.cursor()
    sql = f"SELECT coins FROM users WHERE user_id={id}"
    cursor = db.cursor()
    cursor.execute(sql)
    for x in cursor.fetchone():
        sql = f"UPDATE users SET coins=coins+1 WHERE user_id = {id};"
        cursor.execute(sql)
        db.commit()
        break
    return 'Добавлена монетка'


@bot.message_handler(commands=['start'])
def button(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_add_score = telebot.types.InlineKeyboardButton('Добавить баллы', callback_data='button_add_score')
    button_list_awards = telebot.types.InlineKeyboardButton('Список наград', callback_data='button_list_awards')
    button_add_award = telebot.types.InlineKeyboardButton('Добавить награду', callback_data='button_add_award')
    button_info = telebot.types.InlineKeyboardButton('Инфо', callback_data='button_info')
    markup.add(button_add_score, button_list_awards, button_add_award, button_info)
    bot.send_message(message.chat.id, f"Главное меню \nВ наличии {get_coins(message.chat.id)} баллов",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'button_add_score':
            print(call.message)
            bot.send_message(call.message.chat.id, add_coins(call.message.chat.id))
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            button_1 = telebot.types.InlineKeyboardButton('1', callback_data='button_add_1')
            button_2 = telebot.types.InlineKeyboardButton('2', callback_data='button_add_2')
            button_3 = telebot.types.InlineKeyboardButton('3', callback_data='button_add_3')
            button_4 = telebot.types.InlineKeyboardButton('4', callback_data='button_add_4')
            button_5 = telebot.types.InlineKeyboardButton('5', callback_data='button_add_5')
            menu = telebot.types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu')
            markup.add(button_1, button_2, button_3, button_4, button_5, menu)
            bot.send_message(call.message.chat.id, f"Главное меню \nВ наличии {get_coins(call.message.chat.id)} баллов",
                             reply_markup=markup)
        elif call.data == 'button_list_awards':
            bot.edit_message_text(text='тест', chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif call.data == 'button_add_1':
            bot.send_message(call.message.chat.id, f"Тест кнопки")
        elif call.data == 'back_to_menu':
            button(call.message)

bot.infinity_polling()
