import os
import codecs
import json
from citrus_drop import CitrusDrop

ck = os.environ.get('TWITTER_CONSUMER_KEY')
cs = os.environ.get('TWITTER_CONSUMER_SECRET')
at = os.environ.get('TWITTER_ACCESS_TOKEN')
ats = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

with codecs.open('./idol_name_list.json', 'r', 'utf-8') as f:
    idol_name_list = json.load(f)

twitter_user_id = '101991197'

cd = CitrusDrop(consumer_key=ck, consumer_secret=cs, access_token=at,
                access_token_secret=ats, idol_name_list=idol_name_list, user_id=twitter_user_id)

with codecs.open('follower_dict.json', 'r', 'utf-8') as f:
    d = json.load(f)
    cd.set_followers_dict(d)

print(cd.get_drop())
