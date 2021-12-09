from linebot_app.app import create_app, db
from linebot_app.bot_config import database_url

app = create_app({
    'SQLALCHEMY_DATABASE_URI': database_url,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})

# force models loaded before creating all tables
import linebot_app.models
with app.app_context():
    db.create_all()
    db.session.commit()
