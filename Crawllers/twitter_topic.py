from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
import pymongo
from tqdm.auto import tqdm
import time
from collections import Counter

SEED = 0
TOPIC_URL = "https://www.twitter.com/{}/topics"
TOPIC_CLASS = 'css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-1hvjb8t'
TOPIC_NAME_CLASS = 'css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-qvutc0'
TOPIC_CATE_CLASS = 'css-901oao css-cens5h r-14j79pv r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0'

db = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")['twarc']['topics']

def init_driver(headless):
    if not headless:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable - gpu")
        driver = webdriver.Chrome(options=options)
    else:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument('--allow-running-insecure-content')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable - gpu")
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    return driver

driver = init_driver(False)

def switch_cookie(x):
    driver.delete_all_cookies()
    with open(f'g:/dataset/twitter_data/cookie{x}.pkl', 'rb') as f:
        cookie = pickle.load(f)
        print(cookie)

    for c in cookie:
        try:
            driver.add_cookie({
                "domain": c["domain"],
                "name": c["name"],
                "value": c["value"],
                "path": c["path"],

            })
        except:
            pass
    driver.refresh()
    time.sleep(2)


with open('./user.pkl','rb') as f:
    dd = pickle.load(f)
userlist = dd['screen_name'].tolist()


for i,user in enumerate(tqdm(userlist)):
    driver.get('http://www.twitter.com')
    if i%20 == 0:
        switch_cookie((SEED%3))
        SEED+=1


    driver.get(TOPIC_URL.format(user))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    x = []

    try:
        for item in soup.find_all(class_=TOPIC_CLASS):
            x.append(item.find(class_=TOPIC_CATE_CLASS).text)
    except:
        pass

    r = dict(Counter(x))
    r['user'] = user

    print(r)
    db.insert_one(r)





