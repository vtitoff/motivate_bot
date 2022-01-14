# import main
import os
import sqlite3
import time

# print(os.environ["motivate_bot_token"])

db = sqlite3.connect("bot_database.db")
sql = f"SELECT * FROM rewards"
cursor = db.cursor()
cursor.execute(sql)
s=cursor.fetchall()
print(s)