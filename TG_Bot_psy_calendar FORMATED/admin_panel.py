#admin panel. aproove or reject users for creating events in calendar
import sys
sys.path.insert(0, 'path to handlers')
from telebot import types 
from create_or_cancel_buttons import create_start_event_keyboard
from user_statuses import check_user_exists, update_user_status
from token_and_credentials import bot

def process_user_id(message, admin_id):
    user_id = message.text

    if user_id.lower() == 'відміна':
        bot.send_message(admin_id, "Редагування доступу відмінено.")
        
        
        markup = create_start_event_keyboard()
        bot.send_message(message.chat.id, "Чтобы создать событие, нажмите на кнопку ниже:", reply_markup=markup)
        return

    # check if user with user_id exists
    if check_user_exists(user_id):
        # send message to admin with (approve или reject) buttons
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        item_approve = types.KeyboardButton("Approve")
        item_reject = types.KeyboardButton("Reject")
        markup.add(item_approve, item_reject)

        msg = bot.send_message(admin_id, f"Виберіть дію до користувача з user_id {user_id}:", reply_markup=markup)

        # call another handler
        bot.register_next_step_handler(msg, process_action, user_id, admin_id)
    else:
        bot.send_message(admin_id, f"Користувача з user_id {user_id} не існує.")
        return


def process_action(message, user_id, admin_id):
    action = message.text.lower()
    markup = None  # Define markup outside the if-else block
    
    if action == "approve":
        # update user status to 'approved'
        if update_user_status(user_id, 'approved'):
            bot.send_message(admin_id, f"Користувач {user_id} отримав доступ до бота.")
            
            # send message with button "Create event
            markup = create_start_event_keyboard()
            # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            # create_event_button = types.KeyboardButton("Создать событие")
            # markup.add(create_event_button)
            bot.send_message(user_id, f"Вам надано доступ до онлайн-запису на консультацію. Щоб создать событие, нажмите на кнопку ниже:", reply_markup=markup)
        else:
            bot.send_message(admin_id, "Не вдалося надати доступ. Сталася помилка в базі даних.")
    elif action == "reject":
        # Check if the administrator initiated the command
        if admin_id != user_id:
            # update user status to 'rejected' only if the admin initiated the command
            if update_user_status(user_id, 'rejected'):
                bot.send_message(user_id, f"Вам відказано у доступі до бота.")
            else:
                bot.send_message(admin_id, "Не вдалось відхилити доступ. Сталася помилка в базі даних.")
        else:
            bot.send_message(admin_id, "Ви не можете відхилити доступ самому собі.")
    else:
        bot.send_message(admin_id, "Невірна дія. Використайте 'Approve' або 'Reject'.")

    # remove keyboard
    # markup = types.ReplyKeyboardRemove()
    bot.send_message(admin_id, "Редагування доступу завершене.", reply_markup=markup)


    #after user first time start bot , he can send the request to admin. if admin approve it - user can create events in calendar, else - no.