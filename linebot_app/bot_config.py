import os
import configparser

import pytz
from linebot import LineBotApi, WebhookHandler

import utils

# set the default env (i.e. channel_access_token, channel_secret, ...)
print('parsing arguments...')
utils.parse_args()

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN').strip())
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET').strip())
database_url = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://').strip()

config = configparser.ConfigParser()
config.read('linebot_app/data/config/config.ini', encoding='utf-8')

# default
TIMEZONE = pytz.timezone(config.get('DEFAULT', 'TIMEZONE'))
CACHE_FOLDER_PATH = config.get('DEFAULT', 'CACHE_FOLDER_PATH')
SETTING_FOLDER_PATH = config.get('DEFAULT', 'SETTING_FOLDER_PATH')

# message
FLEX_ALTER = config.get('message.user', 'FLEX_ALTER_MESSAGE')
QUIT_MESSAGE = config.get('message.user', 'QUIT_MESSAGE')
NOTIFICATION_HEADER = config.get('message.user', 'NOTIFICATION_HEADER')
COMMAND_ISSUED_SUCCESS = config.get('message.system', 'COMMAND_ISSUED_SUCCESS')
COMMAND_ISSUED_FAILED = config.get('message.system', 'COMMAND_ISSUED_FAILED')
