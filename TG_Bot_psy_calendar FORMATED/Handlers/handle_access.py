#access message handler
import sys
sys.path.insert(0, 'path_to_bot') #insert path to ur bot
from telebot import types
from token_and_credentials import bot
from admin_panel import process_user_id

# admin usernames var, add other admin id to the list if needed
admin_usernames = ['admin_nickname from tg']  #insert ur admin nick from tg

@bot.message_handler(commands=['access'])
def handle_admin_commands(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # check if admin send a message
    if username in admin_usernames:
        # create keyboard with reject_button and can enter user_id and 'enter' to approve user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        item = types.KeyboardButton("Відміна")
        markup.add(item)
        msg = bot.send_message(user_id, "Введіть user_id користувача, якому треба змінити статус або натисніть 'Відміна':", reply_markup=markup)

        # processing user_id
        bot.register_next_step_handler(msg, process_user_id, user_id)
    else:
        bot.send_message(user_id, "Что ты здесь забыл, давай до свидания. 🖕🖕🖕")