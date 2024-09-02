import telebot
import logging

from db_controller import add_bill, add_person, remove_person, get_person_summary, get_all_person_names
from utils import parse_new, parse_add_person, parse_remove_person, parse_check

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
            bot.reply_to(org_msg, 'done')
        elif command == "add_person":
            parsed = parse_add_person(message)
            add_person(parsed)
            bot.reply_to(org_msg, 'done')
        elif command == "remove_person":
            parsed = parse_remove_person(message)
            remove_person(parsed)
            bot.reply_to(org_msg, 'done')
        elif command == "check":
            parsed = parse_check(message)
            msg = ""
            if parsed == "all":
                all_users = get_all_person_names()
                for user in all_users:
                    summary, total = get_person_summary(user)
                    msg += f"{user}:\n"
                    for entry in summary:
                        msg += f"{entry['amount']}, {entry['link_to_msg']}\n"
                    msg += f"Total sum: {total}\n\n"
            else:
                summary, total = get_person_summary(parsed)
                msg += f"{parsed}:\n"
                msg += f"{summary['amount']}, {summary['link_to_msg']}\n"
                msg += f"Total sum: {total}\n"
            bot.reply_to(org_msg, msg)

        elif command == "all_users":
            msg = ""
            names = get_all_person_names()
            for i in range(len(names)-1):
                msg += names[i]+'-'
            msg += names[-1]
            bot.reply_to(org_msg, msg)



    except Exception:
        return
