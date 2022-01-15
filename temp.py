# import main
import os
import sqlite3
import time

# print(os.environ["motivate_bot_token"])
db = sqlite3.connect("bot_database.db")
# sql = f"CREATE TABLE rewards (reward_id PRIMARY KEY, reward_name TEXT, reward_cost INTEGER, user_id TEXT);"
# sql = f"INSERT INTO rewards (user_id, reward_name, reward_cost) VALUES ('603970011', 'Тест', 15)"
cursor = db.cursor()
cursor.execute(sql)
s=cursor.fetchall()
print(s)
# db.commit()
