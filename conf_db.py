import sqlite3

# basic db setup and edit commands 

'''
my_conn = sqlite3.connect('dictionary.db')
csr = my_conn.cursor()

csr.execute("INSERT INTO dictionary VALUES (?, ?, ?, ?)", ("hello","2022-05-06","3","0"))
csr.execute("DELETE from dictionary")
csr.execute("DROP TABLE messages")

csr.execute("""CREATE TABLE messages(
                chay_id text,
                message_id text
)""")
csr.execute("""CREATE TABLE dictionary(
                word text,
                datec text,
                weight integer,
                count integer,
                user_id text,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )""")
           
csr.execute("SELECT rowid, * FROM dictionary")

items = csr.fetchone()
items = csr.fetchall()

my_conn.commit()
my_conn.close()
'''