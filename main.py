import json
import os
import codecs
from flask import Flask
from flask import render_template
from citrus_drop import CitrusDrop


app = Flask(__name__)


ck = os.environ.get('TWITTER_CONSUMER_KEY')
cs = os.environ.get('TWITTER_CONSUMER_SECRET')
at = os.environ.get('TWITTER_ACCESS_TOKEN')
ats = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

with codecs.open('./idol_name_list.json', 'r', 'utf-8') as f:
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

# TODO: updateボタンを押したらCitrusDropの更新処理を実行する
@app.route('/update')
def update():
    cd.update_followers_dict()
    user_drop = cd.get_drop()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(user_drop, indent=4, ensure_ascii=False))
    title = "CitrusDrop"
    page = "index"
    return render_template('main.html', title=title, message=user_drop, page=page)


# TODO: Twitter認証処理を入れる

@app.route('/')
def index():
    title = "CitrusDrop"
    page = "index"
    return render_template('main.html', title=title, message=user_drop, page=page)


@app.route('/donut')
def donut():
    title = "CitrusDonut"
    page = "donut"
    return render_template('donut.html', title=title, message=user_drop, page=page)


@app.route('/save')
def save_drop():
    title = "save!"
    page = "save!"
    with open(path, 'w', encoding='utf-8') as f:
        d = cd.get_drop()
        f.write(json.dumps(d, indent=4, ensure_ascii=False))
    return render_template('main.html', title=title, message=user_drop, page=page)


if __name__ == '__main__':
    app.run()

