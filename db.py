import sqlite3

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


def insert(t_id, text, created, rt_count, fav_count):
    conn, c = get_cursor()

    # SQL command to insert the data in the table
    try:
        sql_command = """INSERT INTO tweets VALUES (%d, '%s', '%s', %d, %d, %f, %f);""" % (t_id, text.replace("'", "''"), created, rt_count, fav_count, 0, 0)
        print sql_command
        c.execute(sql_command)

        conn.commit()

    except sqlite3.IntegrityError:
        print 'Could not add'

    conn.close()

def main():
    db_setup()

if __name__ == "__main__":
    main()
