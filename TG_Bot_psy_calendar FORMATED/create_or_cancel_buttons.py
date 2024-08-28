
#module of creating Create?Cancel event buttons

from telebot import types
import telebot


# create keyboard with button  "Create event"
def create_start_event_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Створити подію"))
    return markup

# create keyboard with button"Cancel event"
def create_cancel_event_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Відмінити створення події"))
    return markup