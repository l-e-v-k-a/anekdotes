import sqlite3

def table():
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    info = list(cur.execute(f"""SELECT * FROM anekdotes"""))
    db.close()
    res = []
    for i in range(len(info)):
        s = list(info[i])
        s[3] = get_fond_by_num(s[3])
        res.append(s)
    return res

def get_fond_by_num(num):
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    fond = list(cur.execute(f"""SELECT name FROM fonds WHERE num = {num}"""))[0][0]
    db.close()
    return fond

def get_fond_by_name(name):
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    fond = list(cur.execute(f"""SELECT num FROM fonds WHERE name = '{name}'"""))[0][0]
    db.close()
    return fond

def get_joke_by_id(id):
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    info = list(cur.execute(f"""SELECT * FROM anekdotes WHERE num = {id}"""))[0]
    db.close()
    return info

def create_new_anek(num, text, tags, fond):
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    cur.execute(f"""INSERT INTO anekdotes (num, text, tags, fond) VALUES ({num}, '{text}', '{tags}', {fond})""")
    db.commit()
    db.close()

def get_last_anek():
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    info = list(cur.execute(f"""SELECT * FROM anekdotes ORDER BY num DESC LIMIT 1"""))[0]
    db.close()
    return info

def edit_anek(id, text, tags, fond):
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    cur.execute(f"""UPDATE anekdotes SET text='{text}', tags='{tags}', fond={fond} WHERE num = {id}""")
    db.commit()
    db.close()

def delete_anek(id):
    db = sqlite3.connect("./static/db/db.db")
    cur = db.cursor()
    cur.execute(f"""DELETE FROM anekdotes WHERE num={id}""")
    db.commit()
    db.close()