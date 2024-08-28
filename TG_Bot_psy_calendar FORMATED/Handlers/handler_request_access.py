import sys
sys.path.insert(0, 'path_to_bot') #insert path to ur bot
from token_and_credentials import bot
from user_statuses import check_user_status
from user_statuses import insert_user, update_user_status

@bot.message_handler(commands=['request_access'])
def request_access(message):
    user_id = message.from_user.id
    user_status = check_user_status(user_id)

    if user_status == 'approved':
        bot.send_message(user_id, "Ви вже авторизувались та можете записатись на консультацію.")
    elif user_status == 'pending':
        bot.send_message(user_id, "Ваш запит на авторизацію ще розглядається.")
    else:
        admin_id = 'tg_id'  # admin telegram_user_id
        bot.send_message(admin_id, f"Користувач @{message.from_user.username} запитує доступ до бота. "
                                   f"Для схвалення чи відмові у доступі користувачу @{message.from_user.username} напишіть /access, потім відправте його user id: {user_id} у чат та виберіть потрібну опцію")
        bot.send_message(user_id, "Ваш запит на вторизацію відправлено адміністратору.")

        # Check if the user already exists in the database
        existing_user_status = check_user_status(user_id)

        if existing_user_status is None:
            # If the user does not exist, insert them with status 'pending'
            insert_user(user_id, 'pending')
        else:
            # If the user exists, update their status to 'pending'
            update_user_status(user_id, 'pending')
