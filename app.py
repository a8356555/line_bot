# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# ��J�A�� message api ��T
line_bot_api = LineBotApi('TxaoPD1pU5bY0mgspcgaKPDGRFmWAf6PWZXBrnZMVNMG8AwpozGVPfI/2wT22KUoy5NX9vt6YlmkcqdJtgqhWuPXu8zo3p0NY9N7/+F3UyhrTcI9G4WqRO9yz+P4Wxl3vNxzgg/iLhMiR/01TPjFnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a08b90bfde9ee77cad4416f5eb49e040')

# �]�w�A�����T�������}�A�p https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])