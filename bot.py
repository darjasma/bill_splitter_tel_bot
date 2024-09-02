import telebot
import logging

from db_controller import add_bill, add_person, remove_person
from utils import parse_new, parse_add_person, parse_remove_person

BOT_TOKEN = '7524865491:AAG7wO8bY-uCvUTNy4_RRgdyyDHDED3F3_A'


bot = telebot.TeleBot(BOT_TOKEN)


# @bot.message_handler(func=lambda message: True)
# def print_message_link(message):
#     link = f"https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}{message.chat.type}"
#     print(link)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, message.chat.id)




@bot.message_handler(func=lambda msg: msg.chat.type == "supergroup" or msg.chat.type == "group")
def echo_all(message):
    org_msg = message
    message = message.text.lower()
    command = message.split(maxsplit=1)[0]

    try:
        if command == "new":
            parsed = parse_new(message)
            link = f"https://t.me/c/{str(org_msg.chat.id)[4:]}/{org_msg.message_id}"
            add_bill(parsed, link)
            logging.info(f"new {parsed} {link}")
        elif command == "add_person":
            parsed = parse_add_person(message)
            add_person(parsed)
        elif command == "remove_person":
            parsed = parse_remove_person(message)
            remove_person(parsed)
    except Exception:
        return
    bot.reply_to(org_msg, 'done')


