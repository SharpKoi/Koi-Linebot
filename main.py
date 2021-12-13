import os
import json
import threading
import time
from datetime import datetime

from abc import ABC
from typing import List

from gunicorn.app.base import BaseApplication
from linebot.models import *

from linebot_app import app, db
from linebot_app import thread_manager
from linebot_app.tasks import schedule
from linebot_app.bot_config import (config,
                                    line_bot_api, handler,
                                    TIMEZONE,
                                    COMMAND_ISSUED_SUCCESS, COMMAND_ISSUED_FAILED, FLEX_ALTER, SETTING_FOLDER_PATH)
from linebot_app.flex import flex_config
from linebot_app.commands import registered_commands, command_shortcuts
from linebot_app.handlers import EventHandler, NotificationHandler

event_handlers: List[EventHandler] = list()


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    msg: str = event.message.text
    source: Source = event.source

    for _handler in event_handlers:
        _handler.handle_text(event)

    msg = msg.strip()
    segments = msg.split()
    if segments[0].startswith(';;'):
        if segments[0] == ';;':
            # a space between ;; and label
            label = segments[1]
            args = segments[2:]
        else:
            label = segments[0][2:]
            args = segments[1:]
        print(f'User {line_bot_api.get_profile(source.user_id).display_name} issued a command: "{msg}"')
        if label in registered_commands:
            if registered_commands[label](source, event.reply_token, args):
                print(COMMAND_ISSUED_SUCCESS)
                return

    else:
        if segments[0] in command_shortcuts:
            usr_args = segments[1:]
            segments = command_shortcuts[segments[0]].split()
            label = segments[0]
            args = segments[1:]
            args.extend(usr_args)
            command_str = ';;' + ' '.join([label] + args)
            print(f'User {line_bot_api.get_profile(source.user_id).display_name} issued a command: "{command_str}"')
            if registered_commands[label](source, event.reply_token, args):
                print(COMMAND_ISSUED_SUCCESS)
                return

        print(COMMAND_ISSUED_FAILED)


@handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):
    for _handler in event_handlers:
        _handler.handle_postback(event)


@handler.add(JoinEvent)
def handle_join(event: JoinEvent):
    with open(flex_config['home-menu'], 'r') as f:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text=FLEX_ALTER, contents=json.load(f))
        )


def setup_environment():
    if not os.path.exists(SETTING_FOLDER_PATH):
        os.makedirs(SETTING_FOLDER_PATH)


def register_handler(event_handler: EventHandler):
    event_handlers.append(event_handler)


@thread_manager.thread(daemon=False)
def run_schedule(stop_event: threading.Event):
    with app.app_context():
        while not stop_event.wait(1):
            schedule.run_pending()


class GunicornApp(BaseApplication, ABC):
    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application

        print('setup environment...')
        setup_environment()

        print('registering default handler...')
        register_handler(NotificationHandler())

        super().__init__()

    def load_config(self):
        cfg = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in cfg.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self):
        thread_manager.run_all()
        super().run()


if __name__ == "__main__":
    wsgi_app = GunicornApp(app)
    # Note:
    # During the master process of gunicorn app being initialized, the sqlalchemy engine allocates a pool of connections
    # and then gunicorn workers forks them.
    # Which will cause "SSL error: decryption failed or bad record mac" when some queries are executed.
    # To avoid above exception, execute `engine.dispose()` after app being initialized
    # to close the current connection pool
    # and then new connections will come up as soon as some queries are executed.
    # So that the gunicorn workers would not fork the same connection of the master process.
    db.engine.dispose()
    wsgi_app.run()
