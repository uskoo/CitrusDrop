import os
import codecs
import json
from citrus_drop import CitrusDrop

ck = os.environ.get('TWITTER_CONSUMER_KEY')
cs = os.environ.get('TWITTER_CONSUMER_SECRET')
at = os.environ.get('TWITTER_ACCESS_TOKEN')
ats = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

with open('./idol_name_list.json', 'r', encoding='utf-8') as f:
    idol_name_list = json.load(f)

twitter_user_id = '101991197'

# CitrusDrop生成
cd = CitrusDrop(consumer_key=ck, consumer_secret=cs, access_token=at,
                access_token_secret=ats, idol_name_list=idol_name_list, user_id=twitter_user_id)

# ファイルをdictに読広
# set_followers_dict test
try:
    with open('follower_dict.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
        cd.set_followers_dict(d)
except FileNotFoundError:
    pass

cd.set_user_profile()

# get_followers()
# get_followers_count()
# get_rest_api_followers_list()
# update_followers_dict_light()

# update_followers_dict() テスト
# twitterからプロフィールを取得
# cd.update_followers_dict()

# drop（解析結果のdict）を出力
print(cd.get_drop())
