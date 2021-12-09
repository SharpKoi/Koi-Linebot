import json
import os
from datetime import datetime

import pytz
from linebot.models import (Event, MessageEvent,
                            TextSendMessage, FlexSendMessage, PostbackEvent)

from linebot_app.app import db
from linebot_app.flex import flex_config
from linebot_app.bot_config import line_bot_api, config, TIMEZONE, SETTING_FOLDER_PATH, FLEX_ALTER
from linebot_app.models import Notification

registered_handlers = list()


class EventHandler:
    def __init__(self):
        pass

    def handle(self, event: Event):
        pass

    def handle_text(self, event: MessageEvent):
        pass

    def handle_postback(self, event: PostbackEvent):
        pass


class NotificationHandler(EventHandler):
    def __init__(self):
        super().__init__()

    def handle_text(self, event: MessageEvent):
        user_setting_path = os.path.join(SETTING_FOLDER_PATH, f'{event.source.user_id}.json')

        if os.path.exists(user_setting_path):
            with open(user_setting_path, mode='r', encoding='utf-8') as f:
                setting = json.load(f)
            if setting['step'] == 1:
                # set notification content
                setting['content'] = event.message.text
                with open(flex_config['notify-settime-ui'], 'r', encoding='utf-8') as flex_file:
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text=FLEX_ALTER,
                                        contents=json.load(flex_file)))
                # update step
                setting['step'] += 1
                # update setting file
                with open(user_setting_path, mode='w', encoding='utf-8') as f:
                    json.dump(setting, f, indent=4, ensure_ascii=False)

    def handle_postback(self, event: PostbackEvent):
        user_setting_path = os.path.join(SETTING_FOLDER_PATH, f'{event.source.user_id}.json')

        if os.path.exists(user_setting_path):
            with open(user_setting_path, mode='r', encoding='utf-8') as f:
                setting: dict = json.load(f)
            if setting['step'] == 2:
                notify_time = event.postback.params['datetime'].replace('T', ' ')
                setting['notify_time'] = notify_time
                # confirm
                notify_confirm_ui = self.notification_confirm_ui(setting['content'], setting['notify_time'])
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text=FLEX_ALTER,
                                    contents=notify_confirm_ui)
                )
                # update step
                setting['step'] += 1
                # update setting file
                with open(user_setting_path, mode='w', encoding='utf-8') as f:
                    json.dump(setting, f, indent=4, ensure_ascii=False)
            elif setting['step'] == 3:
                # force the establish time using utc timezone.
                setting['establish_time'] = datetime.utcnow()
                # The timezone of the datetime postback is from user's timezone.
                # Here assume that all users timezone are the same as the config timezone.
                # Thus we set the timezone of the parsed datetime as config timezone
                # and then transforms it to UTC time before writing into database.
                setting['notify_time'] = \
                    TIMEZONE.localize(datetime.strptime(setting['notify_time'], '%Y-%m-%d %H:%M')).astimezone(pytz.utc)
                # write setting into database
                notification = \
                    Notification(
                        userid=setting['userid'],
                        username=setting['username'],
                        notify_time=setting['notify_time'],
                        content=setting['content'],
                        establish_time=setting['establish_time'])
                db.session.add(notification)
                db.session.commit()
                # delete setting file
                os.remove(user_setting_path)
                # send successful message to user
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='已成功設定提醒!')
                )

    @classmethod
    def notification_confirm_ui(cls, content: str, notify_time):
        with open(flex_config['notify-confirm-ui'], 'r', encoding='utf-8') as flex_file:
            notify_confirm_ui = json.load(flex_file)
            notify_confirm_ui['body']['contents'][-1]['contents'][0]['contents'][1]['contents'][0]['text'] = notify_time
            notify_confirm_ui['body']['contents'][-1]['contents'][1]['contents'][1]['contents'][0]['text'] = content

        return notify_confirm_ui
