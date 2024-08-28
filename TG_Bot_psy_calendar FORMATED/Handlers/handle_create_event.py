#createevent message handler, checking authorized user
import sys
sys.path.insert(0, 'path_to_bot') #insert path to ur bot
from user_statuses import check_user_status, authorized_only
from token_and_credentials import bot
from create_or_cancel_buttons import create_start_event_keyboard
import telebot

# processing commant/createevent
@bot.message_handler(commands=['createevent'])
@authorized_only
def create_event(message):
    chat_id = message.chat.id
    
    # checking user_status(approve/pending/rejected or no in db)
    user_id = message.from_user.id
    user_status = check_user_status(user_id)

    if user_status != 'approved':
        bot.send_message(chat_id, "Для створення події вам необхідно авторизуватись.❗❗❗")
        return

    # reset all global vars before start of creating new event
    global event_title, event_datetime, event_chat_id
    event_title = None
    event_datetime = None
    event_chat_id = chat_id  # saving chat_id

    # create keyboard with a button "Create event"
    markup = create_start_event_keyboard()
    
    bot.send_message(chat_id, "Щоб створити подію натисніть кнопку нижче👇👇👇:", reply_markup=markup)
    
    