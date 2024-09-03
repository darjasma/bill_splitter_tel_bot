from bot import bot
from db_controller import create_db

create_db()
bot.infinity_polling()

