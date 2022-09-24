from googletrans import Translator
import requests
import urllib
import json
import dictionary_db
import time
from datetime import date
import random

#define token, URL main body, Bot name, initiate translator
token = '5379724236:AAHY9y9Z3LQ8jGHxp5pNJuMGMIoulnU4EUM'
URL = f'https://api.telegram.org/bot{token}/'
USERNAME_BOT = 'Jinglish_bot'
translator = Translator()

#-------------------------------------------------------------------------

def neww_tg(text_tg, user):
    date_today_tg = date.today()
    return (text_tg, str(date_today_tg), '3', '0', user)

# update functions-------------------------------------------------------------------------

#function returns decoded 
def get_url(url):
    r = requests.get(url)
    content = r.text
    return content

#function returns json of ger_url()
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

#check if someone contacted the bot
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#function adds chat_id and message_id to messages table
def get_messages_id(url):
    js = get_json_from_url(url)
    print(js)
    chat_id = js["result"]["chat"]["id"]
    message_id = js["result"]["message_id"]
    print(chat_id, message_id)
    dictionary_db.add_message(chat_id, message_id)
    return js

def clear(url, chat_id):
    for message_id in dictionary_db.list_of_messages(chat_id):
        print(message_id)
        requests.get(f'{url}deleteMessage?chat_id={chat_id}&message_id={message_id}')
        time.sleep(0.002)
    dictionary_db.delete_one_message(chat_id)
    return

# send functions----------------------------------------------------------------------------------------

def send_translation(translation, chat_id):
    tot = urllib.parse.quote_plus(translation)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(tot, chat_id)
    get_messages_id(url)
    
def send_dictionary_db(user_id, chat_id):
    list_of_w = dictionary_db.list_of_words(user_id)
    text = '<b>There are your last 20 words:</b>\n\n'
    #choose book category (red, orange, green) depending on weight
    for i in list_of_w[0:20]:
        if i[2] == 3:
            symbol = '\U0001F4D5'
        elif i[2] == 2:
            symbol = '\U0001F4D9'
        else: 
            symbol = '\U0001F4D7'

        text += ('<i>' + str(i[1]) + '</i>' +' '+ symbol + '<b>' + str(i[0]) + '</b>' + ' ' + '\n')
            
    tot = urllib.parse.quote_plus(text)
    keyboard1 = json.dumps({'inline_keyboard': [[{'text': 'my stats', 'url': 'http://ya.ru'}]]})
    keyboard = keyboard1
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML&reply_markup={}".format(tot, chat_id, keyboard)
    get_messages_id(url)

def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(tot, chat_id)
    get_messages_id(url)

def send_word_onrequest(user_id, chat_id):
    l = dictionary_db.list_of_words(user_id) 
    list = [k[0] for k in l]
    rand_word = random.choice(list)
    print(rand_word)
    keyboard = json.dumps({'keyboard': [['/yes'], ['/no']], 'resize_keyboard': True, 'one_time_keyboard': True})
    url = URL + "sendMessage?text=Remember the meaning?\n<b>{}</b>&chat_id={}&parse_mode=HTML&reply_markup={}".format(rand_word, chat_id, keyboard)
    get_messages_id(url)

# echo function------------------------------------------------------------------------------------------

def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                message = update["message"]["message_id"]
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                user_id = update["message"]["from"]["id"]
                user_name = update["message"]["from"]["first_name"]

                dictionary_db.add_user(user_id)
                dictionary_db.add_message(chat,message)

                if text == "/start":
                    send_message(f"Welcome, {user_name}! \n\nI am " + "<b>Jingle</b>" + 
                    " - a smart bot designed to help you memorize new words using well-proven methodologies", chat)

                elif text == "/yes":
                    send_message('Great! I will note that', chat)
                elif text == '/no':
                    send_message('Ok, we will get that word later', chat)
                
                elif text == "/mywords":
                    send_dictionary_db(user_id, chat)

                # delete all the messages in the chat (should be faster ideally!!!)
                elif text == "/clear":
                    clear(URL, chat)
                
                elif text == "/random":
                    send_word_onrequest(user_id, chat)

                else:
                    text = text.lower().replace(' ', '')
                    translation = translator.translate(text, dest='ru').text
                    send_translation(translation, chat)
                    line = [neww_tg(text, user_id)]
                    if dictionary_db.lookup(line[0][0], user_id):
                        dictionary_db.add_count(line[0][0], user_id)
                    else:
                        dictionary_db.add_one(line)