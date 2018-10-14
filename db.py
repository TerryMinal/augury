# from config import FIRESTORE_CERT

import sqlite3
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# cred = credentials.Certificate(FIRESTORE_CERT)
# firebase_admin.initialize_app(cred)
# db = firestore.client()

def get_cursor():
    # connecting to the database
    conn = sqlite3.connect("tweets.db")

    # cursor
    return conn, conn.cursor()

def db_setup():
    conn, c = get_cursor()

    # SQL command to create a table in the database
    sql_command = """CREATE TABLE tweets (
    id INTEGER PRIMARY KEY,
    company TEXT,
    text TEXT,
    created TEXT,
    q_type TEXT,
    rt_count INTEGER,
    fav_count INTEGER,
    score DOUBLE,
    magnitude DOUBLE);"""

    # execute the statement
    c.execute(sql_command)

    conn.commit()
    conn.close()


def check_duplicate(text):
    conn, c = get_cursor()

    sql_command = """SELECT * FROM tweets WHERE text = '%s';""" % (text.replace("'", "''"))
    c.execute(sql_command)

    return len(c.fetchall()) > 0


def insert(company, t_id, text, created, q_type, rt_count, fav_count):
    conn, c = get_cursor()

    if check_duplicate(text):
        print('Duplicate')
        return

    # SQL command to insert the data in the table
    try:
        sql_command = """INSERT INTO tweets VALUES (%d, '%s', '%s', '%s', '%s', %d, %d, %f, %f);""" % (t_id, company, text.replace("'","''"), created, q_type, rt_count, fav_count, 0, 0)
        c.execute(sql_command)
        conn.commit()

        doc_ref = db.collection(company).document(str(t_id))
        doc_ref.set({
            'text': text,
            'created': created,
            'q_type': q_type,
            'rt_count': rt_count,
            'fav_count': fav_count,
            'score': 0,
            'magnitude': 0
        })

    except sqlite3.IntegrityError:
        print('Already exists')

    conn.close()

def get_tweets():
    conn, c = get_cursor()
    sql_command = """SELECT * FROM tweets;"""
    c.execute(sql_command)

    data = c.fetchall()

    conn.close()

    return data

def main():
    #db_setup()
    print(get_tweets())

if __name__ == "__main__":
    x = get_tweets()
    print(x[45][2])
    #1: company name
    
