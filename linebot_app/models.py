from linebot_app.bot_config import TIMEZONE
from linebot_app.extensions import db


class Notification(db.Model):
    __tablename__ = 'Notifications'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50))
    username = db.Column(db.String(50))
    notify_time = db.Column(db.TIMESTAMP(timezone=True))
    content = db.Column(db.String(500))
    establish_time = db.Column(db.TIMESTAMP(timezone=True))

    def display_text(self):
        return f'ID: {self.id}\n' \
               f'建立時間: {self.establish_time.astimezone(TIMEZONE).replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")}\n' \
               f'提醒時間: {self.notify_time.astimezone(TIMEZONE).strftime("%Y-%m-%d %H:%M")}\n' \
               f'提醒內容: {self.content}'

    @classmethod
    def get_items_by_userid(cls, userid: str, page: int, per_page: int):
        return cls.query.filter_by(userid=userid).paginate(page, per_page)

    @classmethod
    def get_top(cls):
        return cls.query.order_by(cls.notify_time).first()
