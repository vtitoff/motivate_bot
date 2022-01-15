# import main
import os
import sqlite3
import time
import uuid

# print(os.environ["motivate_bot_token"])
db = sqlite3.connect("bot_database.db")
sql = f"SELECT * FROM rewards"
cursor = db.cursor()
cursor.execute(sql)
s=cursor.fetchall()
print(s)
# db.commit()

print(str(uuid.uuid4()).replace('-',''))