import re, sqlite3, photo_file

def open_db():
    conn = sqlite3.connect(photo_file.DATA_FILE)
    conn.row_factory = dict_factory
    return conn

#get the result with dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Exec SQL
def exec(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    db.commit()
    return c.lastrowid


#Exec SQL and get the result
def select(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    return c.fetchall()