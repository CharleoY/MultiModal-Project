from Login import Login, cookie
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import time
from items import tweet, userInfo
import pandas as pd
from db import initDatabase
from lxml import html
from random import choice
import sys


ROOT_URL = "https://mbasic.facebook.com/"
TIMELINE_URL = "https://mbasic.facebook.com/profile.php?id={}&v=timeline&refid=17"
TWEET_URL = "https://mbasic.facebook.com/story.php?story_fbid={}&id={}&refid=17"
IMAGE_URL = "https://mbasic.facebook.com/photo.php?fbid={}&id={}&refid=17"
USER_URL = "https://www.facebook.com/profile.php?id={}&refid=17"
PHOTO_URL = "https://mbasic.facebook.com/profile.php?id={}&v=photos&refid=17"
LIKES = "https://mbasic.facebook.com/profile.php?id={}&v=likes&refid=17"
AVATAR = 'https://mbasic.facebook.com/profile/picture/view/?profile_id={}'
NEXT_PAGE = "m_more_item"

# More = soup.find('span',string='See More Stories')
db = initDatabase().initMongoDB()
FACEBOOK = db['facebook']
USER = FACEBOOK['user_detail']
TWEET = FACEBOOK['tweet']
email = ""
passwd = ""
session = Login(email, passwd)
homepage_resp = session.get(ROOT_URL)
df = pd.read_pickle('./fb.pkl')
count = 0

cookies = cookie()

for i, id_ in enumerate(tqdm(range(df.shape[0]))):

    about_url = ''
    collection = []
    USER_ID = df['ID'][i]
    TYPE = df['Type'][i]
    if USER.find_one({'userID': USER_ID}) != None:
        print('Exist User, skipping....')
        continue
    print(f'Collecting {USER_ID}')
    co = cookies[i % (len(cookies))]
    print("Cookie : ", co["c_user"])
    session.cookies.update(co)
    userTimeline = session.get(TIMELINE_URL.format(str(USER_ID)))
    soup = BeautifulSoup(userTimeline.content, 'html.parser')
    if soup.find('span', string='The page you requested cannot be displayed '
                                'right now. It may be temporarily unavailable, the link you clicked on may be'
                                ' broken or expired, or you may not have permission to view this page.') is not None:
        continue
    if soup.title.text == "You’re Temporarily Blocked":
        print('Blocked by Facebook, exit')
        sys.exit()
    j = 0
    while True:
        if j == 0:
            try:
                about_url = ROOT_URL + soup.find('a', string='About')['href'][1:]
            except:
                pass
        else:
            userTimeline = session.get(NextPage)
            soup = BeautifulSoup(userTimeline.content, 'html.parser')
            if soup.title.text == "You’re Temporarily Blocked":
                print('Blocked by Facebook, exit')
                sys.exit()
        temp = soup.section
        for item in soup.findAll('header'):
            item.extract()
        tweets = tweet(temp, USER_ID)

        if tweets != 0:
            collection.extend(tweets)

        if soup.find('span', string='See More Stories') is None:
            print('No more timeline, go for next user.')
            break
        else:
            NextPage = ROOT_URL + soup.find('span', string='See More Stories').parent['href']
            print(f"Find Next Page {NextPage}, continue.")
        j += 1
        count += 1
        if count % 100 == 0:
            print('Sleep for 200s now to prevent ban.')
            time.sleep(200)
    if about_url != '' and about_url != None:
        try:
            info = session.get(about_url)
            soup = BeautifulSoup(info.content, 'html.parser')
            if soup.find('span', string='The page you requested cannot be displayed '
                                        'right now. It may be temporarily unavailable, the link you clicked on may be'
                                        ' broken or expired, or you may not have permission to view this page.') is not None:
                continue
            if soup.title.text == "You’re Temporarily Blocked":
                print('Blocked by Facebook, exit')
                sys.exit()
            tree = html.fromstring(info.content)
            for item in soup.findAll('header'):
                item.extract()
            user_info = userInfo(soup, USER_ID, tree)
            try:
                avatar = session.get(AVATAR.format(USER_ID))
                soup = BeautifulSoup(avatar.content, 'html.parser')
                avt = soup.find(id="objects_container").img['src']
                user_info = {**user_info, **{'Avatar': avt}}
                count += 1
            except Exception as e:
                print('Avatar Error: ', e)
            if len(user_info) > 1:
                print('Inserting user info into database')
                USER.insert_one(user_info)
        except Exception as e:
            print('Userinfo Error: ', e)
    else:
        try:
            info = session.get(USER_URL.format(str(USER_ID)))
            soup = BeautifulSoup(info.content, 'html.parser')
            if soup.find('span', string='The page you requested cannot be displayed '
                                        'right now. It may be temporarily unavailable, the link you clicked on may be'
                                        ' broken or expired, or you may not have permission to view this page.') != None:
                continue
            if soup.title.text == "You’re Temporarily Blocked":
                print('Blocked by Facebook, exit')
                sys.exit()
            tree = html.fromstring(info.content)
            for item in soup.findAll('header'):
                item.extract()
            user_info = userInfo(soup, USER_ID, tree)
            try:
                avatar = session.get(AVATAR.format(USER_ID))
                soup = BeautifulSoup(avatar.content, 'html.parser')
                avt = soup.find(id="objects_container").img['src']
                user_info = {**user_info, **{'Avatar': avt}}
                count += 1
            except Exception as e:
                print('Avatar Error: ', e)
            if len(user_info) > 1:
                print('Inserting user info into database')
                USER.insert_one(user_info)
        except Exception as e:
            print('Userinfo Error: ', e)
    count += 1
    if collection != 0 and collection != []:
        TWEET.insert_many(collection)
        print(f'Insterting {len(collection)} tweets into database')
    time.sleep(5)
