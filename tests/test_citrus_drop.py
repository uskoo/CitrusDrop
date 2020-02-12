#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
import json

from citrus_drop import CitrusDrop


def test_get_followers():
    with open('idol_name_list.json', 'r') as f:
        idol_name_list = json.load(f)
    
    cd = CitrusDrop(os.environ['CONSUMER_KEY'],
                    os.environ['CONSUMER_SECRET'],
                    os.environ['ACCESS_TOKEN'],
                    os.environ['ACCESS_TOKEN_SECRET'],
                    idol_name_list
                    )

    cd.get_followers()
    cd.find_idol()
