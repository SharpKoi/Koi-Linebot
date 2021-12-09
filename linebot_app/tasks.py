from datetime import datetime

import pytz
import schedule
from linebot.models import TextSendMessage

from linebot_app.app import db
from linebot_app.bot_config import line_bot_api, TIMEZONE, NOTIFICATION_HEADER
from linebot_app.models import Notification


@schedule.repeat(schedule.every(15).seconds)
def notify():
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    # query the first notification
    notification = Notification.get_top()
    if notification:
        # print(f'[{now.astimezone(TIMEZONE)}] 報時')
        # check time to notify
        if notification.notify_time == now.replace(second=0, microsecond=0):
            print(f'[{now.astimezone(TIMEZONE).strftime("%Y-%m-%d %H:%M")}] execute notify task')
            line_bot_api.push_message(
                to=notification.userid,
                messages=[
                    TextSendMessage(text=f'{NOTIFICATION_HEADER}\n{notification.content}')
                ])
            # delete current notification
            db.session.delete(notification)
            db.session.commit()
