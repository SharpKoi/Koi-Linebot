import os
from linebot_app.bot_config import config

flex_folder = config.get('DEFAULT', 'FLEX_UI_FOLDER_PATH')

flex_config = {
    'home-menu': os.path.join(flex_folder, 'home_menu.json'),
    'notify-settime-ui': os.path.join(flex_folder, 'notify_settime_ui.json'),
    'notify-confirm-ui': os.path.join(flex_folder, 'notify_confirm_ui.json')
}
