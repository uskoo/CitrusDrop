#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import json
import time
import datetime
# import codecs
from requests_oauthlib import OAuth1Session


class CitrusDrop:
    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str, idol_name_list: list):
        """
        
        Args:
            consumer_key (str): for twitter api
            consumer_secret (str): for twitter api
            access_token (str): for twitter api
            access_token_secret (str): for twitter api
        """
        self.twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
        self.followers_dict = []    # twitterから取得したProfileそのもの
        self.followers_dict_light = []  # profileを必要なものに絞ったやつ
        self.followers_count = -1   # /followers/ids から取得したfollowerの数 = twitterのfollower数 -1:未取得
        self.dict_count = 0         # /followers/list から取得済みのdictの数
        self.cursor = -1            # /followers/list 読み込み用のcursor値 -1:未取得, 0:取得完了, その他の値:カーソル位置
        self.rate_limit_status = {}
        self.idol_name_list = idol_name_list
        self.drop = {}              # 解析結果
        self.ng_name_list = ['愛', '関', '礼', '優', '心', '海', '星']

    # followers APIをTwitterに送信する
    def get_followers(self):
        url = "https://api.twitter.com/1.1/followers/list.json"
        if self.cursor == -1:
            params = {}
        else:
            params = {'cursor': self.cursor}
        res = self.twitter.get(url, params=params)

        if res.status_code == 200:
            json_dict = json.loads(res.text)
            print(json.dumps(res.text, indent=4, ensure_ascii=False))
            for u in json_dict['users']:
                self.followers_dict.append(u)
                print(u)

            self.cursor = json_dict['next_cursor']
        else:
            print("status code", res.status_code)  # status code 429: Too much requests

    # followerの数をカウントし、followers_countに入れる
    def get_followers_count(self):
        url = "https://api.twitter.com/1.1/followers/ids.json"
        params = {}
        res = self.twitter.get(url, params=params)

        if res.status_code == 200:
            json_dict = json.loads(res.text)
            self.followers_count = len(json_dict['ids'])

    # API残量のリストを取得し、rate_limit_statusに入れる
    def get_rate_limit_status(self):
        url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
        params = {}
        res = self.twitter.get(url, params=params)

        if res.status_code == 200:
            self.rate_limit_status = json.loads(res.text)

    def get_rest_api_followers_list(self):
        url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
        params = {}
        res = self.twitter.get(url, params=params)

        if res.status_code == 200:
            fl = json.loads(res.text)
            return fl['resources']['followers']['/followers/list']['remaining']
        else:
            return 0

    # APIの残量とリセット時間をカウントし、送信制御する
    # TODO:threadingで回すようにする
    def update_followers_dict(self):
        # フォロワー数を取得
        if self.followers_count == -1:
            self.get_followers_count()

        while self.cursor != 0:
            # API残量チェック
            # 待機しなくてもよい場合はfollowerを取得する
            if self.get_rest_api_followers_list() != 0:
                self.get_followers()
            else:
                # APIリセット時刻を取得(UNIX時刻)
                self.get_rate_limit_status()
                ut_reset = self.rate_limit_status['resources']['followers']['/followers/list']['reset']
                dt_reset = datetime.datetime.fromtimestamp(ut_reset)
                # 現在時億を取得
                dt_now = datetime.datetime.now()
                ut_now = int(time.mktime(dt_now.timetuple()))
                # リセット時刻まで待機
                wait = ut_reset - ut_now
                print("Waiting until", dt_reset, "from", dt_now, "wait time", wait, "sec")
                time.sleep(wait)

        self.update_followers_dict_light()

    # 解析用に要素を絞ったdictを更新
    def update_followers_dict_light(self):
        for u in self.followers_dict:
            ud = {
                'screen_name': u["screen_name"],
                'description': u['description']
            }
            self.followers_dict_light.append(ud)

    # ユーザ毎の属性を取得する
    def find_idol(self):
        for user_dict in self.followers_dict:
            description = user_dict['description']
            d = {'screen_name': user_dict['screen_name'], 'description': user_dict['description'], 'idol_count': []}
            for idol_name in self.idol_name_list:
                count = 0
                for c in idol_name.values():
                    count += description.count(c)
                if count > 1:
                    idol_count = {'idol_name': idol_name["name"], 'count': count}
                    d['idol_count'].append(idol_count)
            print(d)
            # {'screen_name': 'xxxxxx',  {'idol_name': 'xxxxx', 'count': xxx}, ...}

    # 全体の属性を取得する
    def get_drop(self):
        # with codecs.open('../idol_name_list.json', 'r', 'utf-8') as f:
        #     idol_name_list = json.load(f)

        # {'idol_name': 'xxxxx', 'count': xxx}, ...
        d = []
        for idol_name in self.idol_name_list:
            count = 0
            for called_name in idol_name.values():
                for u in self.followers_dict_light:
                    count += u['description'].count(called_name)
            if count > 1:
                idol_count = {'idol_name': idol_name["name"], 'count': count}
                d.append(idol_count)
        return sorted(d, key=lambda x: x['count'], reverse=True)

    def _search_fullname(self, text: str):
        return [profile for profile in self.idol_name_list if text.find(profile['name']) >= 0]

    def _search_partname(self, text: str):
        idol_name_list = self.idol_name_list

        output_list = []

        for key in ['given_name', 'family_name']:
            idol_name_list = filter(lambda x: x[key] not in self.ng_name_list, idol_name_list)
            output_list += filter(lambda x: text.find(x[key]) >= 0, idol_name_list)

        return output_list
