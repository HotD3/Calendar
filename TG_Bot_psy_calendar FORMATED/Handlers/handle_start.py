# start_message_handler
import sys
sys.path.insert(0, 'path_to_bot') #insert path to ur bot
from telebot import types
from token_and_credentials import bot
from user_statuses import check_user_status
from create_or_cancel_buttons import create_start_event_keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_status = check_user_status(user_id)

    if user_status == 'approved':
        markup = create_start_event_keyboard()
        # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        # create_event_button = types.KeyboardButton("Создать событие")
        # markup.add(create_event_button)
        bot.send_message(user_id, "Вы вже авторизовулись та можете записатись на консультацію.", reply_markup=markup)
    elif user_status == 'pending':
        bot.send_message(user_id, "Ваш запит на авторизацію ще розглядається.")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        request_access = types.KeyboardButton("Відправити запит")
        cancel_button = types.KeyboardButton("Відміна")
        markup.add(request_access, cancel_button)
        bot.send_message(user_id, " Для отримання доступу відправте запрос до адміністратора за допомогою кнопки нижче або нажміть кнопку 'Відміна':", reply_markup=markup)
