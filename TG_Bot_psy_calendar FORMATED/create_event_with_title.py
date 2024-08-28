from telebot import types
from token_and_credentials import bot
from datetime import datetime, timedelta
from create_event_with_date import create_event_with_date
from create_or_cancel_buttons import create_start_event_keyboard


def create_event_with_title(message):

    global event_title, cancelling_event
    event_title = message.text
    event_chat_id = message.chat.id


    # check if event_chat_id IS NOT None
    if not event_chat_id:
        event_chat_id = message.chat.id

    #Check if users input : "Cancel event"
    if event_title.lower() == "відмінити створення події":
        event_chat_id = message.chat.id
        # changing cancelling event var value to True
        # show keyboard with button "Create event"
        markup = create_start_event_keyboard()
        cancelling_event = True
        bot.send_message(event_chat_id, "🙅Створення події відмінено🙅‍♂️. Натисніть кнопку Створити подію для створення нової події у календарі.👇👇👇",  reply_markup=markup)
        
        
        return
        
    else:
        #create keyboard with date choice buttons(3 in row)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        today = datetime.today()
        days = []
        row = []
        for i in range(15):
            day = today + timedelta(days=i)
            # check if choicen day is not Sunday(rest day)
            if day.weekday() != 6:
                row.append(types.KeyboardButton(day.strftime('%d.%m')))
            if len(row) == 3 or i == 14:
                markup.row(*row)
                row = []

        # send message with date choice buttons
        bot.send_message(event_chat_id, "📅Оберіть дату події :", reply_markup=markup)

    # call another handler where we choice the date . we send chat id and our event title.
    bot.register_next_step_handler(message, create_event_with_date, event_chat_id, event_title)
