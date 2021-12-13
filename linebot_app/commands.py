import os
import json
from typing import Any, List, Dict, Callable, Optional

from flask_sqlalchemy import Pagination
from linebot.models import (Source, SourceRoom, SourceGroup,
                            TextSendMessage, FlexSendMessage)

from linebot_app import db
from linebot_app.bot_config import line_bot_api, config, SETTING_FOLDER_PATH, FLEX_ALTER, QUIT_MESSAGE
from linebot_app.flex import flex_config
from linebot_app.models import Notification

registered_commands: Dict[str, Callable] = dict()
command_shortcuts: Dict[str, str] = dict()


def bot_command(label: str, shortcuts: Optional[Dict[str, str]] = None):
    def decorator(func):
        registered_commands[label] = func
        if shortcuts is not None:
            _shortcuts = dict(map(lambda kv: (kv[0], label + ' ' + kv[1]), shortcuts.items()))
            command_shortcuts.update(_shortcuts)
        return func

    return decorator


@bot_command('menu', shortcuts={'選單': ''})
def menu_command(source: Source, reply_token: str, args: List) -> bool:
    with open(flex_config['home-menu'], 'r', encoding='utf-8') as f:
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(alt_text=FLEX_ALTER,
                            contents=json.load(f))
        )

    return True


@bot_command('quit', shortcuts={'踢出': ''})
def quit_command(source: Source, reply_token: str, args: List) -> bool:
    if isinstance(source, SourceGroup):
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=QUIT_MESSAGE))
        line_bot_api.leave_group(source.group_id)
        return True
    elif isinstance(source, SourceRoom):
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=QUIT_MESSAGE))
        line_bot_api.leave_room(source.room_id)
        return True

    return False


@bot_command('notification', shortcuts={'添加提醒': 'add', '刪除提醒': 'rm', '提醒列表': 'list'})
def notification_command(source: Source, reply_token: str, args: List) -> bool:
    if args[0] == 'list':
        page = 1 if (len(args) == 1) else int(args[1])
        pagination: Pagination = Notification.get_items_by_userid(source.user_id, page, 5)

        list_str = f'你的提醒列表({page}/{pagination.pages}): \n' + \
                   '\n\n'.join([notification.display_text() for notification in pagination.items])

        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=list_str))

        return True
    elif args[0] == 'add':
        user_setting_path = os.path.join(SETTING_FOLDER_PATH, f'{source.user_id}.json')

        if os.path.exists(user_setting_path):
            line_bot_api.reply_message(
                reply_token,
                [
                    TextSendMessage(text='遺棄先前的設定，幫您準備新的提醒設定'),
                    TextSendMessage(text='請輸入文字提醒內容')
                ]
            )
            os.remove(user_setting_path)
        else:
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text='請輸入文字提醒內容')
            )

        # step 1
        # create setting data
        setting = dict()
        setting['step'] = 1
        setting['userid'] = source.user_id
        setting['username'] = line_bot_api.get_profile(source.user_id).display_name
        # update setting file
        with open(user_setting_path, mode='w', encoding='utf-8') as f:
            json.dump(setting, f, indent=4, ensure_ascii=False)

        return True
    elif args[0] == 'rm':
        _id = int(args[1])
        Notification.query.filter_by(id=_id, userid=source.user_id).delete()
        db.session.commit()

        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=f'已成功刪除id={_id}的提醒')
        )

        return True
    elif args[0] == 'set':
        pass
    else:
        pass

    return False


@bot_command('yt')
def yt_command(source: Source, reply_token: str, args: List) -> bool:
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=config.get('message.user', 'DOWNLOADING_MESSAGE'))
    )

    return True
