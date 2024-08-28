import sys
sys.path.insert(0, 'path_to_bot') #insert path to ur bot
from global_vars import event_title,event_datetime, event_chat_id, cancelling_event
from telebot import types
from token_and_credentials import bot
from create_or_cancel_buttons import create_start_event_keyboard
from user_statuses import check_user_status

@bot.message_handler(func=lambda message: True)  # handler for processing all messages
def handle_default(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = check_user_status(user_id)

    if user_status == 'approved':
        markup = create_start_event_keyboard()
        bot.send_message(chat_id, "Будь ласка, почніть створення події спочатку. Щоб створити подію, натисніть кнопку нижче:👇👇👇", reply_markup=markup)
    else:
        # if user does not authorized - send him a message that authorization is requeired
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        request_access = types.KeyboardButton("Відправити запит")
        cancel_button = types.KeyboardButton("Відміна")
        markup.add(request_access, cancel_button)
        bot.send_message(chat_id, "Для створення події вам необхідно авторизуватись.", reply_markup=markup)
        
        bot.send_message(user_id, "Для отримання доступу відправте запрос до адміністратора за допомогою кнопки нижче або нажміть кнопку 'Відміна':", reply_markup=markup)