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
    user_id TEXT PRIMARY KEY,
    reward_name TEXT
    reward_cost INTEGER
);
''')
db.commit()