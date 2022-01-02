# motivate_bot
@vt_motivate_bot


db.execute('''
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    coins INTEGER
);
''')
db.commit()