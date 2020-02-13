import json
import os
from urllib.parse import parse_qsl
import asyncio

from requests_oauthlib import OAuth1Session
from flask import Flask, jsonify, request, redirect, url_for
from flask import render_template
from citrus_drop import CitrusDrop


app = Flask(__name__)

user_drop = {
        'screen_name': '未取得',
        'last_update': '-',
        'profile_image_url': './static/not_found.png',
        'followers_count': '未取得',
        'friends_count': '未取得',
        'result': []
    }


@app.route('/update', methods=['GET'])
def update():
    global loop
    title = "CitrusDrop"
    page = "main"
    #loop = asyncio.get_event_loop()
    print("update呼ばれた")

    hoge = loop.run_until_complete(update_dict())
    print(hoge)
    return render_template('main.html', title=title, page=page, message=user_drop, disabled="true")


async def update_dict():
    title = "CitrusDrop"
    page = "main"
    print('kokomadekitayo')
    task = loop.create_task(asyncio.sleep(10))

    await task
    return render_template('main.html', title=title, page=page, message=user_drop, disabled="false")


@app.route('/')
def main():
    print("呼ばれた")
    disabled = "false"
    print(request.args.get('disabled'))
    if request.args.get('disabled'):
        disabled = "true"
    else:
        pass
    title = "CitrusDrop"
    page = "main"
    return render_template('main.html', title=title, page=page, message=user_drop, disabled=disabled)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())
    #app.run()
