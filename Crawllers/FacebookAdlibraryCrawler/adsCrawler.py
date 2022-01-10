from selenium import webdriver
import time
import pymongo
from cookie import cookie
from bs4 import BeautifulSoup
import requests
import json
from list import Pages
def init_page(driver):
    driver.get('https://www.facebook.com/ads/library')
    for item in cookie:
        driver.add_cookie(item)

def get_content(driver,domain):
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    try:
        name = soup.find_all(class_='egkesoaz')[1].find(class_='dgpf1xc5').text
    except:
        name = ""
    items = soup.find_all(class_='_7jwy')

    all_ = []
    for item in items:
        i = {}
        j = []
        k = ''
        vc = ''
        id_ = ""
        try:
            text = item.find_all(class_='_4ik4')[1].text
            i['text'] = text
        except:
            i['text'] = ''
        try:
            imgs = item.find_all(class_='dweymo5e')
            if len(imgs) > 0:
                for img in imgs:
                    j.append(img.img['src'])
            else:
                video = item.find_all(class_='_8o0a')[0].video['src']
                video_cover = item.find_all(class_='_8o0a')[0].video['poster']
                k = video
                vc = video_cover
        except Exception as e:
            print(e)
        try:
            date = item.find_all(class_='_9cd3')[0].text
        except:
            date = ""
        try:
            id_ = item.find_all(class_='_9cd3')[1].text
        except:
            id_ = ""

        i['id_'] = id_
        i['imgs'] = j
        i['video'] = k
        i['Vendor'] = "a"
        i['domain'] = "a"
        i['video_cover'] = vc
        i['date'] = date
        all_.append(i)
    print("id_ : {},text : {}, images: {}, Vendor: {}, domain: {}, vc: {}, date: {}".format(i['id_'], i['text'],
                                                                                                i['imgs'], i['Vendor'],
                                                                                                i['domain'],
                                                                                                i['video_cover'],
                                                                                                i['date']))

def scroll_down(driver):
    while True:
        try:
            driver.find_element_by_class_name('_8n_3')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)
        except:
            break

def url_iter(urls):
#todo: read urls and return a iterator
    return iter(urls)

def get_ads_url(urlIter):
    urlDict = next(urlIter)
    url = urlDict['url'].replace("https://www.facebook.com/","https://mbasic.facebook.com/")
    domain = urlDict['domain']
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    id_ = json.loads(soup.find(id="recent").div.div.div['data-ft'])['page_id']
    url = "https://www.facebook.com/ads/library/?active_status=all" \
           "&ad_type=all&country=ALL&view_all_page_id={}" \
           "&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all".format(id_)
    return url,domain

def main():
    url,domain = get_ads_url(urlIter)
    driver.get(url)
    time.sleep(5)
    scroll_down(driver)
    content = get_content(driver,domain)
    if content != None and len(content)>0:
        db.insert_many(content)

def init_driver(headless):
    if not headless:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
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


if __name__=="__main__":
    driver = init_driver(False)
    init_page(driver)
    db = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")['ads']['Facebook4']
    urls = []
    for url in Pages:
        urls.append({"url":url,"domain":"Vehicle"})
    urlIter =url_iter(urls)
    while True:
        main()