import sys, errno
import os
import json

from flask import Blueprint
from flask import request, abort
from linebot.exceptions import InvalidSignatureError

from linebot_app.bot_config import handler, CACHE_FOLDER_PATH
from linebot_app import thread_manager

blueprint = Blueprint(name='linebot', import_name=__name__)


@blueprint.route('/shutdown', methods=['POST'])
def shutdown():
    # clear cache files
    with os.scandir(CACHE_FOLDER_PATH) as iter_files:
        for f in iter_files:
            if f.is_file():
                os.remove(f.path)

    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    print('Server shutdown.')
    if shutdown_func:
        # raise RuntimeError('Not running with the Werkzeug Server')
        thread_manager.stop_all()
        shutdown_func()
    else:
        sys.exit(errno.EINTR)

    return 'Server shutting down...'


# 接收 LINE 的資訊
@blueprint.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    if signature is None:
        return 'This route is for line message api.'

    body = request.get_data(as_text=True)

    try:
        body_json = json.loads(body)
        if body_json['events']:
            event_info = body_json['events'][0]
            user_id = event_info['source']['userId']
            print('[使用者] ' + user_id)
            if event_info['type'] == 'message':
                if event_info['message']['type'] == 'text':
                    print('[文字訊息] ' + event_info['message']['text'])
            elif event_info['type'] == 'postback':
                print('[POSTBACK] ' + event_info['postback']['data'])
        else:
            print('received ping.')

        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
