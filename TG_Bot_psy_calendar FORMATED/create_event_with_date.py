from token_and_credentials import bot, service
from datetime import datetime, timedelta
from telebot import types
import re
from global_vars import event_title,event_datetime, event_chat_id, cancelling_event




from create_or_cancel_buttons import create_start_event_keyboard



times = [
    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
    '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
    '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
    '19:00', '19:30', '20:00'
]


def create_event_with_date(message, event_chat_id, event_title):
    global event_datetime, cancelling_event
    event_date = message.text
    event_datetime = event_date

    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    if cancelling_event:
        cancelling_event = False
        event_title = None
        event_datetime = None

        markup = types.ReplyKeyboardRemove()
        bot.send_message(event_chat_id, "🙅‍♂️Створення події відмінено.🙅", reply_markup=markup)
        return

    try:
        if not re.match(r'^\d{2}\.\d{2}$', event_date):
            bot.send_message(event_chat_id, "Неправильний формат дати. Використовуйте формат ДД.ММ (наприклад, 29.09).")
            return

        event_date = f"{current_datetime.year}-{event_date.split('.')[1]}-{event_date.split('.')[0]}"
        time_min = f"{event_date}T00:00:00Z"
        time_max = f"{event_date}T23:59:59Z"

        calendar_id = 'calendar id' #from google cloud/google calendar api
        events = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute()
        busy_intervals = set()

        for event in events.get('items', []):
            start_time = event['start'].get('dateTime', None)
            end_time = event['end'].get('dateTime', None)
            if start_time and end_time:
                busy_intervals.add((start_time, end_time))

        #creating time intervals
        if current_date.strftime('%Y-%m-%d') == event_date:
            current_time_str = current_time.strftime('%H:%M')  #converting current time in correct format
            print(f"Пользователь выбрал текущую дату ({current_date}), текущее время: {current_time_str}.")

            # converting current time to str
            current_time_str = current_time.strftime('%H:%M')

            # get only intervals > then curent time
            available_times = [time for time in times if time >= current_time_str]

        else:
            print(f"Пользователь выбрал дату: {current_date.strftime('%Y-%m-%d')}, текущее время: {current_time.strftime('%H:%M')}.")
            
            available_times = [time for time in times if time >= '10:00']

        #create busy intervals
        busy_intervals = set()

        for event in events.get('items', []):
            start_time = event['start'].get('dateTime', None)
            end_time = event['end'].get('dateTime', None)
            if start_time and end_time:
                busy_intervals.add((start_time, end_time))

        # add available time intervals
        available_intervals = []
        for i in range(len(available_times)):
            time_start = available_times[i]
            time_end = (datetime.strptime(time_start, '%H:%M') + timedelta(minutes=90)).strftime('%H:%M')

            #  check if available interval doesnt cross with busy intervals
            is_available = True
            for busy_interval in busy_intervals:
                busy_start = busy_interval[0].split('T')[1][:5]
                busy_end = busy_interval[1].split('T')[1][:5]

                if (time_start <= busy_start < time_end) or (time_start < busy_end <= time_end):
                    is_available = False
                    break

            if is_available:
                available_intervals.append(f"{time_start} - {time_end}")

        # show available intervals if possible
        if available_intervals:
            new_date_message = process_event_data(message, available_intervals, event_chat_id)
            
            from process_event_time import process_event_time
            bot.register_next_step_handler(new_date_message, process_event_time, event_chat_id, event_title, event_datetime, cancelling_event)
            
        else:   
            bot.send_message(event_chat_id, "☹️На обрану дату більше нема вільних місць.")
            from create_event_with_title import create_event_with_title
            # create keyboard with date choice buttons
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            today = datetime.today()
            days = []
            row = []
            for i in range(15):
                day = today + timedelta(days=i)
                # check if day is not Sunday(rest day)
                if day.weekday() != 6:
                    row.append(types.KeyboardButton(day.strftime('%d.%m')))
                if len(row) == 3 or i == 14:
                    markup.row(*row)
                    row = []

            bot.register_next_step_handler(message, create_event_with_date, event_chat_id, event_title)

            # send message with date choice buttons
            bot.send_message(event_chat_id, "📅Оберіть іншу дату події:", reply_markup=markup)
            
            
           
    except Exception as e:
        bot.send_message(event_chat_id, f'Сталась помилка: {str(e)}')

def process_event_data(message, available_intervals, event_chat_id):
     
     return bot.send_message(
                event_chat_id,
                "⏰Оберіть час початку події:",
                reply_markup=types.ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    one_time_keyboard=True,
                    row_width=2
                ).add(
                    *available_intervals
                ).add(
                    types.KeyboardButton("Відмінити створення події"),
                    types.KeyboardButton("Вибрати іншу дату")
                )
            )
     
#generating time intervals for choicen date, then gererating busy intervals and then shows available intervals.
# then 2 conditions : we have available interval : can choice it/cancel the event/choice another date, no intervals.        

