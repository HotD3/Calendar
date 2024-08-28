from create_or_cancel_buttons import create_start_event_keyboard
from token_and_credentials import bot, service
from telebot import types
from datetime import datetime, timedelta

from global_vars import event_title,event_datetime, event_chat_id, cancelling_event
import urllib
from urllib.parse import quote
import urllib.parse
import telebot






def process_event_time(message, event_chat_id, event_title, event_datetime, cancelling_event):
    # global event_datetime, cancelling_event
    # chat_id = message.event_chat.id
    # chat_id = message.chat.id
    event_time = message.text

    try:
        if event_time == "Відмінити створення події":
            cancelling_event = False
            event_title = None
            event_datetime = None

            # Create keyboard with a "Create event" button
            markup = create_start_event_keyboard()
            bot.send_message(event_chat_id, "🙅Створення події відмінено🙅‍♂️. Натисніть кнопку Створити подію для створення нової події у календарі.👇👇👇", reply_markup=markup)
        elif event_time == "Вибрати іншу дату":
            from create_event_with_date import create_event_with_date
            bot.register_next_step_handler(message, create_event_with_date, event_chat_id, event_title)
            # Create keybord w date choicing(3 in raw)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            today = datetime.today()
            days = []
            row = []
            for i in range(15):
                day = today + timedelta(days=i)
                # check if day is not Sunday
                if day.weekday() != 6:
                    row.append(types.KeyboardButton(day.strftime('%d.%m')))
                if len(row) == 3 or i == 14:
                    markup.row(*row)
                    row = []

            # send message with date choice buttons
            bot.send_message(event_chat_id, "Выберіть іншу дату: :", reply_markup=markup)
        else:
            # split time on start and end
            event_start_time, event_end_time = event_time.split(' - ')

            # convert selected time to Google Calendar API
            event_start_time = f"{datetime.now().year}-{event_datetime.split('.')[1]}-{event_datetime.split('.')[0]}T{event_start_time}:00"
            event_end_time = f"{datetime.now().year}-{event_datetime.split('.')[1]}-{event_datetime.split('.')[0]}T{event_end_time}:00"

            # convert event_start_time to datetime object
            event_start_time_datetime = datetime.strptime(event_start_time, '%Y-%m-%dT%H:%M:%S')
            event_end_time_datetime = datetime.strptime(event_end_time, '%Y-%m-%dT%H:%M:%S')

            # create var event_start_time_correct in correct format
            event_start_time_correct = event_start_time_datetime.strftime('%Y%m%dT%H%M%S')
            event_end_time_correct = event_end_time_datetime.strftime('%Y%m%dT%H%M%S')

            calendar_id = 'calendar id' #google cloud/calendar id

            event = {
                'summary': event_title,
                'description': 'Описание события',
                'start': {
                    'dateTime': event_start_time,
                    'timeZone': 'Europe/Warsaw',
                },
                'end': {
                    'dateTime': event_end_time,
                    'timeZone': 'Europe/Warsaw',
                },
            }

            # creating event in
            event = service.events().insert(calendarId=calendar_id, body=event).execute()

            # generating a ,message with created event
            event_date = event_start_time.split('T')[0]
            event_time_start = event_start_time.split('T')[1][:5]
            event_time_end = event_end_time.split('T')[1][:5]
            event_info = f'Подія 📅"{event_title}" створена:\nДата: {event_date}\nЧас: з {event_time_start} до {event_time_end}'
            event_description = "Перевірте час та часовий пояс вашої події."

            # generating link for user to add this event to his own calendar
            encoded_title = urllib.parse.quote(event_title)
            encoded_description = urllib.parse.quote(event_description)  # converting event description

            # link with converted description
            calendar_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={encoded_title}&dates={event_start_time_correct}/{event_end_time_correct}&details={encoded_description}&location=Место+события&ctz=Europe/Warsaw"
            #sending a message about created event and link on it
            bot.send_message(event_chat_id, event_info)
            bot.send_message(event_chat_id, f"🔗🔗🔗Посилання на додавання події у свій календар: {calendar_link}")
            # craeting keyboard with "Create event" button
            markup = create_start_event_keyboard()
            bot.send_message(event_chat_id, "☺️☺️☺️Подія створена. Чи Ви хочете стровити ще одну?", reply_markup=markup)
    except Exception as e:
        bot.send_message(event_chat_id, f'Сталась помилка: {str(e)}')
