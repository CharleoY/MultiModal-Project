from datetime import datetime

from copy import deepcopy

auth_list=[]

drop_user_field = ['id','protected','verified','profile_background_image_url_https','profile_image_url_https',
                   'following','follow_request_sent','notifications','translator_type',"withheld_in_countries",'utc_offset'
                   ,'time_zone','contributors_enabled']
drop_tweet_field = ["truncated","withheld_in_countries",'contributors',"quoted_status_id","	quoted_status_permalink",
                    "withheld_scope","withheld_copyright",'in_reply_to_status_id','in_reply_to_user_id',
                    'in_reply_to_screen_name','favorited','retweeted','possibly_sensitive','id','coordinates']

def time_format(t):
    return datetime.strftime(datetime.strptime(t, '%a %b %d %H:%M:%S +0000 %Y'),'%Y-%m-%d %H:%M:%S')

def drop_fields(c):
    t = deepcopy(c)
    for i in drop_user_field:
        try:
            t['user'].pop(i)
        except:
            pass
    for i in drop_tweet_field:
        try:
            t.pop(i)
        except:
            pass
    t['created_at'] = time_format(t['created_at'])
    t['user']['created_at'] = time_format(t['user']['created_at'])
    t['full_text'] = t['full_text'].encode('utf8').decode('utf8')
    t['user_id'] = t['user']['id_str']
    user = t['user']
    t.pop('user')

    return user,t