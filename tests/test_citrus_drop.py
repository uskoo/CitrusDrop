#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import json

from citrus_drop import CitrusDrop


def test_search_fullname():
    TESTS = [
        ['高垣楓担当のプロデューサーです。佐藤心と中野有香もプロデュースしています。副業で自然言語処理のエンジニアもしています。', ['高垣楓', '佐藤心', '中野有香']],
        ['デレ：橘ありす・速水奏・miroir◆ミリ：桜守歌織・箱崎星梨花◆リステ：かえ・陽花・天葉◆絵を描いたりUnityとかPythonでなにか作ったりします◆', ['橘ありす', '速水奏', '桜守歌織', '箱崎星梨花']],
    ]

    with open('idol_name_list.json', 'r') as f:
        idol_name_list = json.load(f)
    
    cd = CitrusDrop(os.environ['TWITTER_CONSUMER_KEY'],
                    os.environ['TWITTER_CONSUMER_SECRET'],
                    os.environ['TWITTER_ACCESS_TOKEN'],
                    os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
                    idol_name_list
                    )

    for t in TESTS:
        assert all([c in t[1] for c in cd._search_fullname(t[0])])


def test_search_partname():
    TESTS = [
        ['ただの通りすがりの星梨花Pです。\nラウンジ【中二病奥義・三曲の極み】のラウマス。星梨花さんと日本酒の普及に努めるアラサー。ありがとうミリオンライブ!\n\nミリシタID:2833KPT2\n\n\n質問箱→https://t.co/6y2UByvDsj', ['箱崎星梨花']],
    ]

    with open('idol_name_list.json', 'r') as f:
        idol_name_list = json.load(f)

    cd = CitrusDrop(os.environ['TWITTER_CONSUMER_KEY'],
                    os.environ['TWITTER_CONSUMER_SECRET'],
                    os.environ['TWITTER_ACCESS_TOKEN'],
                    os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
                    idol_name_list
                    )

    for t in TESTS:
        data = cd._search_partname(t[0])
