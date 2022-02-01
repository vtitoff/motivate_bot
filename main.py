import requests as r
import json
import telebot
import os
import sqlite3
import uuid

token = os.environ['motivate_bot_token']
bot = telebot.TeleBot(token)

instruction = 'Информация'


class Rewards_List():
    dict_rewards = {}
    dict_del_rewards = {}


reward_list = Rewards_List()


def get_coins(id):
    db = sqlite3.connect("bot_database.db")
    sql = "SELECT coins FROM users WHERE user_id={}".format(id)
    cursor = db.cursor()
    cursor.execute(sql)
    for x in cursor.fetchone():
        return x


def add_coins(id, coin):
    db = sqlite3.connect("bot_database.db")
    sql = "SELECT coins FROM users WHERE user_id={}".format(id)
    cursor = db.cursor()
    cursor.execute(sql)
    for x in cursor.fetchone():
        sql = "UPDATE users SET coins=coins+{} WHERE user_id={}".format(coin, id)
        cursor.execute(sql)
        db.commit()
        return f"Добавлено {coin} балла"


def add_reward(name, cost):
    pass


def register_new_reward(message):
    reward_object_name = message.text
    bot.send_message(message.chat.id, "Введи стоимость награды")
    # TODO написать проверку на число
    bot.register_next_step_handler(message, register_cost_reward, reward_object_name)


def register_cost_reward(message, reward_object_name):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Что-то не так, попробуй добавить награду заново")
        return
    reward_object_cost = int(message.text)
    db = sqlite3.connect("bot_database.db")
    sql = f"INSERT INTO rewards (reward_id, reward_name, reward_cost, user_id) VALUES (?, ?, ?, ?)"
    cursor = db.cursor()
    cursor.execute(sql, (str(uuid.uuid4()).replace('-', ''), reward_object_name, reward_object_cost, message.chat.id))
    db.commit()
    markup = telebot.types.InlineKeyboardMarkup(row_width=2).add(
        telebot.types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu'))
    bot.send_message(message.chat.id, text='Награда добавлена',
                     reply_markup=markup)


def reset_coins(id):
    db = sqlite3.connect("bot_database.db")
    sql = "UPDATE users SET coins=0 WHERE user_id = {};".format(id)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    return "Баллы сброшены"


@bot.message_handler(commands=['start'])
def button(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_add_score = telebot.types.InlineKeyboardButton('Добавить баллы', callback_data='button_add_score')
    button_list_awards = telebot.types.InlineKeyboardButton('Список наград', callback_data='button_list_awards')
    button_info = telebot.types.InlineKeyboardButton('Инфо', callback_data='button_info')
    markup.add(button_add_score, button_list_awards, button_info)
    bot.send_message(message.chat.id, f"Главное меню \nВ наличии {get_coins(message.chat.id)} баллов",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'button_add_score':
            print(call.message)
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
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            choose_button = telebot.types.InlineKeyboardButton('Выбрать награду', callback_data='choose_reward')
            add_reward_button = telebot.types.InlineKeyboardButton('Добавить награду', callback_data='add_reward')
            delete_reward_button = telebot.types.InlineKeyboardButton('Убрать награду', callback_data='del_reward')
            menu = telebot.types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu')
            markup.add(choose_button, add_reward_button, delete_reward_button, menu)
            bot.send_message(call.message.chat.id, f"Меню наград",
                             reply_markup=markup)
        elif call.data == 'add_reward':
            message = bot.send_message(call.message.chat.id, "Введи название награды")
            bot.register_next_step_handler(message, register_new_reward)
        elif call.data == 'button_add_1':
            bot.send_message(call.message.chat.id, add_coins(call.message.chat.id, 1))
        elif call.data == 'button_add_2':
            bot.send_message(call.message.chat.id, add_coins(call.message.chat.id, 2))
        elif call.data == 'button_add_3':
            bot.send_message(call.message.chat.id, add_coins(call.message.chat.id, 3))
        elif call.data == 'button_add_4':
            bot.send_message(call.message.chat.id, add_coins(call.message.chat.id, 4))
        elif call.data == 'button_add_5':
            bot.send_message(call.message.chat.id, add_coins(call.message.chat.id, 5))
        elif call.data == 'back_to_menu':
            button(call.message)
        elif call.data == 'button_info':
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            menu = telebot.types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu')
            button_reset = telebot.types.InlineKeyboardButton('Сбросить баллы', callback_data='button_reset')
            markup.add(menu, button_reset)
            bot.send_message(call.message.chat.id, instruction, reply_markup=markup)
        elif call.data == 'button_reset':
            bot.send_message(call.message.chat.id, reset_coins(call.message.chat.id))
        elif call.data in reward_list.dict_rewards:
            print(reward_list.dict_rewards[call.data])
            db = sqlite3.connect("bot_database.db")
            sql = "UPDATE users SET coins=coins-{} WHERE user_id={}".format(reward_list.dict_rewards[call.data],
                                                                            call.message.chat.id)
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            markup = telebot.types.InlineKeyboardMarkup(row_width=2).add(
                telebot.types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu'))
            bot.send_message(call.message.chat.id,
                             text=f'Награда использована \nВ наличии {get_coins(call.message.chat.id)} баллов',
                             reply_markup=markup)
        elif call.data in reward_list.dict_del_rewards:
            print(f'{reward_list.dict_del_rewards[call.data]=}')
            db = sqlite3.connect("bot_database.db")
            sql = "DELETE FROM rewards WHERE reward_name='{}' AND user_id={}".format(
                reward_list.dict_del_rewards[call.data], call.message.chat.id)
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            markup = telebot.types.InlineKeyboardMarkup(row_width=2).add(
                telebot.types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu'))
            bot.send_message(call.message.chat.id, text='Награда убрана из списка',
                             reply_markup=markup)
        elif call.data == 'choose_reward':
            print('choose_reward')
            db = sqlite3.connect("bot_database.db")
            sql = "SELECT reward_name, reward_cost FROM rewards WHERE user_id={}".format(call.message.chat.id)
            cursor = db.cursor()
            cursor.execute(sql)
            button_id = 0
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            for i, j in cursor.fetchall():
                button_id += 1
                markup.add(telebot.types.InlineKeyboardButton(f'{i} - {j} coins', callback_data=f'button {button_id}'))
                reward_list.dict_rewards[f'button {button_id}'] = j
            markup.add(telebot.types.InlineKeyboardButton('Назад', callback_data='back_to_menu'))
            bot.send_message(call.message.chat.id, 'Список наград', reply_markup=markup)
        elif call.data == 'del_reward':
            db = sqlite3.connect("bot_database.db")
            sql = "SELECT reward_name, reward_cost FROM rewards WHERE user_id={}".format(call.message.chat.id)
            cursor = db.cursor()
            cursor.execute(sql)
            button_id = 0
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            for i, j in cursor.fetchall():
                button_id += 1
                markup.add(
                    telebot.types.InlineKeyboardButton(f'{i} - {j} coins', callback_data=f'button_del {button_id}'))
                reward_list.dict_del_rewards[f'button_del {button_id}'] = i
            markup.add(telebot.types.InlineKeyboardButton('Назад', callback_data='back_to_menu'))
            bot.send_message(call.message.chat.id, 'Список наград', reply_markup=markup)


bot.infinity_polling()
