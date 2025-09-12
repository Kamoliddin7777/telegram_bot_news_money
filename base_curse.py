import sqlite3
def create_table_users():
    db=sqlite3.connect('curse_base.db')
    cursor=db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(100) DEFAULT 'No username',
    phone VARCHAR(30) UNIQUE,
    chat_id BIGINT UNIQUE,
    full_name VARCHAR(100) DEFAULT 'No info'
    )
    ''')
    db.commit()
    db.close()

create_table_users()
def get_user(chat_id):
    db = sqlite3.connect('curse_base.db')
    cursor = db.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE chat_id=?
    ''',(chat_id,))
    user=cursor.fetchone()
    db.close()
    return user
def save_info(*args):
    db = sqlite3.connect('curse_base.db')
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO users(user_name,full_name,phone,chat_id) 
        VALUES(?,?,?,?)
        ''', args)
    db.commit()
    db.close()
def create_table_history():
    db = sqlite3.connect('curse_base.db')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         chat_id BIGINT,
         text TEXT,
         src VARCHAR(50),
         desc VARCHAR(50),
         result TEXT
    )
    ''')
    db.commit()
    db.close()
create_table_history()
def save_translate_data(*args):
    db = sqlite3.connect('curse_base.db')
    cursor = db.cursor()
    cursor.execute('''
    INSERT INTO history(chat_id,text,src,desc,result)
    VALUES(?,?,?,?,?)
    ''',args)
    db.commit()
    db.close()
def get_history(chat_id):
    db = sqlite3.connect('curse_base.db')
    cursor = db.cursor()
    cursor.execute('''
     SELECT text,src,desc,result FROM history WHERE chat_id=?
    ORDER BY id ASC 
    ''',(chat_id,))
    history_translate=cursor.fetchall()
    db.close()
    return history_translate
