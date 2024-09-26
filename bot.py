import telebot
import logging
from telebot.types import ReactionTypeEmoji
import threading
import time

from db_controller import add_bill, add_person, remove_person, get_person_summary, get_all_person_names, pay_off
from utils import parse_new, parse_add_person, parse_remove_person, parse_check, parse_pay_off

from token_api import TOKEN as BOT_TOKEN

DELETE_MESSAGE_TIME = 60

bot = telebot.TeleBot(BOT_TOKEN)


def delete_message_after_delay(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)



# @bot.message_handler(func=lambda msg: True)
def ed(message):
    link = f"https://t.me/c/{str(message.chat.id)[4:]}/{message.message_thread_id}/{message.message_id}"
    print(link)
    print(message.chat)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, message.chat.id)


@bot.message_handler(func=lambda msg: msg.chat.type=="supergroup" and msg.chat.id==-1002165866143)
def echo_all(message):
    org_msg = message
    message = message.text.lower()
    command = message.split(maxsplit=1)[0]
    try:
        if command == "new":
            parsed = parse_new(message)
            link = f"https://t.me/c/{str(org_msg.chat.id)[4:]}/{org_msg.message_thread_id}/{org_msg.message_id}"
            print(link)
            add_bill(parsed, link)
            logging.info(f"new {parsed} {link}")
            bot.set_message_reaction(org_msg.chat.id, org_msg.id, [ReactionTypeEmoji('💯')], is_big=False)
            parsed = parse_add_person(message)
            add_person(parsed)
        elif command == "remove_person":
            parsed = parse_remove_person(message)
            remove_person(parsed)
            bot.set_message_reaction(org_msg.chat.id, org_msg.id, [ReactionTypeEmoji('💯')], is_big=False)
        elif command == "add_person":
            parsed = parse_add_person(message)
            add_person(parsed)
            bot.set_message_reaction(org_msg.chat.id, org_msg.id, [ReactionTypeEmoji('💯')], is_big=False)
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
                for entry in summary:
                    msg += f"{entry['amount']}, {entry['link_to_msg']}\n"
                msg += f"Total sum: {total}\n"
            sent_message = bot.reply_to(org_msg, msg)
            threading.Thread(target=delete_message_after_delay, args=(org_msg.chat.id, sent_message.message_id, DELETE_MESSAGE_TIME)).start()
            threading.Thread(target=delete_message_after_delay, args=(org_msg.chat.id, org_msg.message_id, DELETE_MESSAGE_TIME)).start()

        elif command == "all_users":
            msg = ""
            names = get_all_person_names()
            for i in range(len(names)-1):
                msg += names[i]+'-'
            msg += names[-1]
            sent_message = bot.reply_to(org_msg, msg)
            threading.Thread(target=delete_message_after_delay, args=(org_msg.chat.id, sent_message.message_id, DELETE_MESSAGE_TIME)).start()
            threading.Thread(target=delete_message_after_delay, args=(org_msg.chat.id, org_msg.message_id, DELETE_MESSAGE_TIME)).start()
        elif command == "pay_off":
            parsed = parse_pay_off(message)
            pay_off(parsed)
            bot.set_message_reaction(org_msg.chat.id, org_msg.id, [ReactionTypeEmoji('💯')], is_big=False)
    except Exception as e:
        print(e)
        return
