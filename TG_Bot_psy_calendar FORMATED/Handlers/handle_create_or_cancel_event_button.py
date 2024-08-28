import sys
sys.path.insert(0, 'path_to_bot') #insert path to ur bot
from telebot import types
from token_and_credentials import bot
from user_statuses import check_user_status
from create_event_with_title import create_event_with_title
from create_or_cancel_buttons import create_cancel_event_keyboard
from global_vars import event_title,event_datetime, event_chat_id, cancelling_event

@bot.message_handler(func=lambda message: message.text in ["Створити подію", "Відмінити створення події"])
def handle_create_or_cancel_event_button(message):
    global cancelling_event

    chat_id = message.chat.id

    # Проверяем, авторизован ли пользователь
    user_id = message.from_user.id
    user_status = check_user_status(user_id)

    if user_status != 'approved':
        bot.send_message(chat_id, "Для створення події вам необхідно авторизуватись.")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        request_access = types.KeyboardButton("Відправити запит")
        cancel_button = types.KeyboardButton("Відміна")
        markup.add(request_access, cancel_button)
        bot.send_message(user_id, "Для отримання доступу відправте запрос до адміністратора за допомогою кнопки нижче або нажміть кнопку 'Відміна':", reply_markup=markup)
        return
    process_user_message(message, user_id)






def process_user_message(message, user_id):
    global cancelling_event

    chat_id = message.chat.id
    if message.text == "Відмінити створення події":
        # If user choiced "Cancel event", setting canceling_event value to True
        cancelling_event = True
        bot.send_message(chat_id, "❌❌❌Створення події відмінено. Выберите дату для создания нового события:")
        create_event_with_title(message)
    elif message.text == "Створити подію":
        # If user choiced "Create event", setting canceling_event to False and start creating new event
        cancelling_event = False

        # update event_chat_id and user_id
        global event_chat_id
        event_chat_id = user_id  # saving user_id

        # bot.send_message(chat_id, "Введите название события:")
        bot.register_next_step_handler(message, create_event_with_title)
        

        # create keyboard w buttons "Cancel event" и "Choice another date"
        markup = create_cancel_event_keyboard()
        
        bot.send_message(chat_id, "✍✍✍Введіть назву події або натисніть кнопку 'Відмінити створення події' ", reply_markup=markup)
        
        