# authenticateのないテスト用コード
import json
import os
from urllib.parse import parse_qsl
import urllib.request
import asyncio
import time

import codecs
from flask import Flask, jsonify, request, redirect, url_for, g
from flask import render_template
from flask_executor import Executor
from citrus_drop import CitrusDrop


app = Flask(__name__)

executor = Executor(app)

ck = os.environ.get('TWITTER_CONSUMER_KEY')
cs = os.environ.get('TWITTER_CONSUMER_SECRET')
at = os.environ.get('TWITTER_ACCESS_TOKEN')
ats = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')


with open('./idol_name_list.json', 'r', encoding='utf-8') as f:
    idol_name_list = json.load(f)

# TODO: Twitter認証処理後に、access_tokenと同時にid_strを取得して、CitrusDropを初期化する
# 以下は仮のID
twitter_user_id = '101991197'

# CitrusDrop初期化
cd = CitrusDrop(consumer_key=ck, consumer_secret=cs, access_token=at,
                access_token_secret=ats, idol_name_list=idol_name_list, user_id=twitter_user_id)

# キャッシュがあったらとりあえず表示だけするためuser_infoをロードする処理
path = './static/' + twitter_user_id + '.json'

try:
    with open(path, 'r', encoding='utf-8') as f:
        user_drop = json.load(f)
        print(user_drop)
except FileNotFoundError:
    user_drop = {
        'screen_name': '未取得',
        'last_update': '-',
        'profile_image_url': './static/not_found.png',
        'followers_count': '未取得',
        'friends_count': '未取得',
        'result': []
    }

# TODO: updateを非同期にする
@app.route('/update', methods=['GET'])
def update():
    g.update_disabled = 'true'
    executor.submit(update_dict)

    title = "CitrusDrop"
    page = "index"
    global user_drop

    return render_template('main.html', title=title, message=user_drop, page=page, disabled='true')


def update_dict():
    # 消しちゃだめ Twitter API処理に時間がかかって困るときにコメントアウト
    global cd
    # cd.update_followers_dict()
    time.sleep(10)

    global user_drop
    user_drop = cd.get_drop()

    global path
    path = './static/' + user_drop['user_id'] + 'test.json'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(user_drop, indent=4, ensure_ascii=False))
        print('saved')

    return True


def some_callback(future):
    # update_dict後にsome_callbackが呼び出されることは確認
    # some_callback自身がNoneType Objectなのでflaskのメソッドを呼び出せない
    url = 'http://127.0.0.1:5000/reload'
    req = urllib.request.Request(url)
    urllib.request.urlopen(req)


executor.add_default_done_callback(some_callback)


@app.route('/reload', methods=['GET'])
def reload():
    print("reloadされた")
    return redirect(url_for('main', reload='true'))


@app.route('/', methods=['GET'])
def index():
    title = "CitrusDrop"
    page = "index"
    global user_drop
    return render_template('index.html', title=title, message=user_drop, page=page)


@app.route('/main')
def main():
    print(request.args.get('reload'))
    print('mainだよ')
    title = "CitrusDrop"
    page = "main"
    global user_drop
    if reload == 'true':
        return render_template('main.html', title=title, message=user_drop, page=page, disabled='false', reload='true')
    else:
        return render_template('main.html', title=title, message=user_drop, page=page, disabled='false')


@app.route('/donut')
def donut():
    title = "CitrusDonut"
    page = "donut"
    global user_drop
    return render_template('donut.html', title=title, message=user_drop, page=page)


@app.route('/save')
def save_drop():
    title = "save!"
    page = "save!"
    global path
    with open(path, 'w', encoding='utf-8') as f:
        d = g.cd.get_drop()
        f.write(json.dumps(d, indent=4, ensure_ascii=False))
    return render_template('main.html', title=title, message=user_drop, page=page)


if __name__ == '__main__':
    app.run()
