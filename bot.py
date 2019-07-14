__author__ = 'Maks_El_Diablo'
# This Python file uses the following encoding: utf-8
from logic import get_out_text
import misc
import database
import telegram

this_bot = telegram.Bot(misc.token)
last_update = database.get_constant("last_update_id")
is_tg_work = True


def get_updates():
    try:
        return this_bot.get_updates()
    except telegram.error.TimedOut:
        return None


def get_message():
    upd = get_updates()
    if upd is None or len(upd) == 0:
        return None, None, None
    update_id = upd[-1]["update_id"]
    global last_update
    if update_id == last_update:
        return None, None, None
    last_update = update_id
    database.update_constant("last_update_id", last_update)
    chat_id = upd[-1]['message']['chat']['id']
    name = upd[-1]['message']['chat']['username']
    if name is None:
        import random
        name = upd[-1]['message']['chat']['first_name'] + str(random.randint(100000, 999999)) + '\t'
    text = upd[-1]['message']['text']
    return chat_id, name, text


def send_message(chat_id, text, reply=None):
    if is_tg_work:
        this_bot.send_message(chat_id=chat_id, text=text, reply_markup=reply)
    else:
        print(text)
        print(reply)


def main():
    bb = 0
    while True:
        if is_tg_work:
            chat_id, name, text = get_message()
        else:
            chat_id = [313949432, 767275247][bb]
            name = [__author__, "EL_DIABLO"][bb]
            text = input("\t")
        if text == "-" and is_tg_work:
            bb ^= 1
            continue
        if chat_id is None:
            import time
            time.sleep(misc.time_to_sleep)
            continue
        print(chat_id, name, text)
        d = get_out_text(chat_id, text, name)
        if d == "":
            continue
        if type(d) is str:
            send_message(chat_id, d)
        else:
            send_message(chat_id, d[0], d[1])
    pass


if __name__ == "__main__":
    main()
