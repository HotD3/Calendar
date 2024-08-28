#FINAL VERSION. Работает генерация ссылки на событие в календарь. Но пока без учета часового пояса.
#дублируется генерация клавиатуры с датами, вынести  ее в отдельную функцию и просто вызывать. Так же сделать отдельную функцию для кнопки types.KeyboardButton("Создать событие"), а может запихнуть все в одну функцию
#копипаст кнопки заменен вызовом функции в момент написания любого текста
#нужно добавить кнопку создать событие после того, как админ нажмет кнопке Відміна после ввода команды /access


import telebot
from telebot import types 
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import re
import sqlite3
import logging
logging.getLogger().setLevel(logging.DEBUG)

import urllib.parse
from urllib.parse import quote

from database import check_database_connection
from create_or_cancel_buttons import create_start_event_keyboard, create_cancel_event_keyboard
from user_statuses import check_user_exists, update_user_status, check_user_status, authorized_only
from token_and_credentials import bot, credentials_path, credentials, service
from admin_panel import process_action, process_user_id
from handler_request_access import request_access
from handle_start import start
from handle_send_request import send_request
from handle_create_event import create_event
from handle_access import handle_admin_commands
from create_event_with_title import create_event_with_title
from global_vars import event_title,event_datetime, event_chat_id, cancelling_event
from handle_create_or_cancel_event_button import handle_create_or_cancel_event_button, process_user_message
from handle_all_messages import handle_default

logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Запуск бот
bot.polling()
