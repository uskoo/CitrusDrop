#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
from citrus_drop import CitrusDrop


def test_get_followers():
    cd = CitrusDrop(os.environ['CONSUMER_KEY'],
                    os.environ['CONSUMER_SECRET'],
                    os.environ['ACCESS_TOKEN'],
                    os.environ['ACCESS_TOKEN_SECRET']
                    )

    cd.get_followers()
