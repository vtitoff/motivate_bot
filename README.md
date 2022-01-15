# motivate_bot
@vt_motivate_bot


db.execute('''
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    coins INTEGER
);
''')
db.commit()


db.execute('''
CREATE TABLE rewards (
    reward_id PRIMARY KEY
    user_id TEXT,
    reward_name TEXT
    reward_cost INTEGER
);
''')
db.commit()



>>> import uuid
>>> str(uuid.uuid4()).replace('-','')