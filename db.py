from config import FIRESTORE_CERT

import sqlite3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(FIRESTORE_CERT)
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    text TEXT,
    created TEXT,
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


def insert(t_id, text, created, rt_count, fav_count):
    conn, c = get_cursor()

    if not check_duplicate(text):
        print('Duplicate')
        return

    # SQL command to insert the data in the table
    try:
        sql_command = """INSERT INTO tweets VALUES (%d, '%s', '%s', %d, %d, %f, %f);""" % (t_id, text.replace("'", "''"), created, rt_count, fav_count, 0, 0)
        c.execute(sql_command)
        conn.commit()

        doc_ref = db.collection('tweets').document(str(t_id))
        doc_ref.set({
            'text': text,
            'created': created,
            'rt_count': rt_count,
            'fav_count': fav_count,
            'score': 0,
            'magnitude': 0
        })

    except sqlite3.IntegrityError:
        print('Already exists')

    conn.close()

def main():
    db_setup()

if __name__ == "__main__":
    main()