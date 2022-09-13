import sqlite3

# dictionary_db functions

def delete_one_message(chat):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("DELETE FROM messages WHERE chay_id = (?)", (chat,))
    my_conn.commit()
    my_conn.close()

def add_message(chat, message):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("INSERT INTO messages VALUES (?,?)", (chat,message))
    my_conn.commit()
    my_conn.close()

def add_user(user):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("INSERT OR IGNORE INTO users VALUES (?)", (user,))
    my_conn.commit()
    my_conn.close() 

def add_one(word):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    word_0 = word[0]
    csr.execute("INSERT INTO dictionary VALUES (?,?,?,?,?)", word_0)
    my_conn.commit()
    my_conn.close() 

def show_all(table):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute(f"SELECT rowid, * FROM {table}")
    items = csr.fetchall()
    for i in items:
        print(i)
    my_conn.commit()
    my_conn.close()
    
def list_of_words(user):
    l = []
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("SELECT rowid, * FROM dictionary WHERE user_id = (?)", (user,))
    items = csr.fetchall()
    for i in items:
        (a,b,c) = (i[1],i[4],i[3])
        l.append((a,b,c)) 
    my_conn.commit()
    my_conn.close() 
    return l

def lookup(new_word, user):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("SELECT * from dictionary WHERE word = (?) AND user_id = (?)", (new_word,user))
    items = csr.fetchall()
    l = len(items)
    print(l)
    if l == 0:
        my_conn.commit()
        my_conn.close()
        return False
    else:
        my_conn.commit()
        my_conn.close()
        return True

def add_count(new_word,user):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute(f"SELECT count FROM dictionary WHERE word = (?) AND user_id = (?)", (new_word,user))
    count = csr.fetchone()[0]
    print(count)
    count_add = count + 1
    csr.execute(f"UPDATE dictionary SET count = (?) WHERE word = (?) AND user_id = (?)", (count_add,new_word,user))
    my_conn.commit()
    my_conn.close()

def update_weight(new_word,user):
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("SELECT weight FROM dictionary WHERE word = (?) AND user_id = (?)", (new_word,user))
    weight = csr.fetchone()[0]
    print(weight)
    weight_pop = weight - 1
    csr.execute("UPDATE dictionary SET weight = (?) WHERE word = (?) AND user_id = (?)", (weight_pop,new_word,user))
    my_conn.commit()
    my_conn.close()

def list_of_messages(chat_id):
    list = []
    my_conn = sqlite3.connect('dictionary.db')
    csr = my_conn.cursor()
    csr.execute("SELECT message_id FROM messages WHERE chay_id = (?)", (chat_id,))
    messages = csr.fetchall()
    for i in messages:
        list.append(i[0])
    my_conn.commit()
    my_conn.close() 
    return list
    