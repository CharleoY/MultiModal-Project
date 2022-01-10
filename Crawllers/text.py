import time as tm
import os
import re
import json
import sqlite3 as sql
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from random import choice
from random import randint


# import utils
#
# logger = utils.configure_root_logger()

class Facebook:

    def __init__(self, _email=None, _password=None, _browser_type="Chrome", _is_headless=True, _database=None):

        # the variables which are fixed
        self.root_url = "https://www.facebook.com/"  # facebook root url
        self.email = _email  # email
        self.password = _password  # password

        # some identifier
        self.browser_state = None  # browser_state
        self.login_state = None  # login_state

        # some parameters of webdriver
        self.cookies_path = "./cookies/cookies(" + _email + ").json"  # path to save cookie

        # indicators of item
        self.timeline_text_class = '_5pbx userContent _3576'
        self.timeline_loading_gif = 'uiSimpleScrollingLoadingIndicator'
        self.images_box = 'fbPhotoStarGridElement fbPhotoStarGridNonStarred focus_target _53s fbPhotoCurationControlWrapper'

        self.images_box1 = 'fbStarGrid _69n fbPhotosRedesignBorderOverlay fbStarGridAppendedTo'
        self.images_box2 = 'fbStarGrid _69n fbPhotosRedesignBorderOverlay'
        self.basic_info = 'uiList fbProfileEditExperiences _4kg _4ks'
        self.background = 'coverPhotoImg photo img'
        self.avatar = '_1nv3 _11kg _1nv5 profilePicThumb'
        self.intro = '_3c-4 _2x70 __2p _2ph- _52jv'
        # the variables which may be variant regularly

        self._url_type = None

        # user list file
        self.file_loc = './profiles.csv'  # file path
        self.database = _database  # database path

        # the selection of browser
        if _browser_type == "Chrome":
            try:
                options = webdriver.ChromeOptions()
                if _is_headless is True:
                    # options.add_argument('--allow-running-insecure-content')
                    prefs = {"profile.managed_default_content_settings.images": 2}
                    options.add_experimental_option("prefs", prefs)
                    options.add_argument("--headless")
                    options.add_argument("--disable - gpu")
                    options.add_argument('--window-size=1080x3000')

                    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
                    self.driver = webdriver.Chrome(options=options)
                else:
                    # options.add_argument('--allow-running-insecure-content')
                    prefs = {"profile.managed_default_content_settings.images": 2}
                    options.add_experimental_option("prefs", prefs)
                    options.add_argument('--window-size=1080x1920')
                    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
                    self.driver = webdriver.Chrome(options=options)
                    self.browser_state = 1
            except AttributeError:
                self.browser_state = 0

        if _browser_type == "Firefox":
            try:
                options = webdriver.FirefoxOptions()
                if _is_headless is True:
                    options.set_headless()
                    options.add_argument("--disable - gpu")
                else:
                    self.driver = webdriver.Firefox(options=options)
                    self.browser_state = 1
            except AttributeError:
                self.browser_state = 0
        self.driver.delete_all_cookies()

        # connect to database and open the root page of facebook
        self.get(self.root_url)
        if self.database != None:
            self.conn = sql.connect(self.database)
            self.cur = self.conn.cursor()
            print('connected')

    def click(self, tag):
        action = ActionChains(self.driver)
        action.click(self.driver.find_element_by_link_text(tag)).perform()

    def page_down(self):
        body = self.driver.find_element_by_css_selector('body')
        body.send_keys(Keys.END)

    def check_existance(self, table_name, user_id):
        self.cur.execute("SELECT * FROM {} WHERE user_id='{}';".format(table_name, user_id))
        row = self.cur.fetchall()
        if len(row) != 0:
            return True
        else:
            return False

    def skip_non_exist(self):
        try:
            self.driver.find_element_by_class_name('_4-dp')
            return False
        except:
            try:
                self.driver.find_element_by_class_name('mtm fsm fwn fcg')
                return False
            except:
                try:
                    self.driver.find_element_by_link_text('Go to News Feed')
                    return False
                except:
                    return True

    def confusion(self):

            c = 300
            tags = [ 'About', 'Friends', 'Albums']
            try:
                tag = choice(tags)
                self.click(tag)
                a = randint(1, 3)
                tm.sleep(a)
                self.page_down()
                b = randint(1, 3)
                tm.sleep(b)
                self.page_down()
                c = c - a - b
            except:
                pass

            return c


    def get_name_list(self):
        """
        get user_info from file
        :return: name_list
        """
        df = pd.read_csv(self.file_loc, index_col=0, header=0)
        name_list = df['url'].tolist()
        return name_list

    def get(self, url):
        """
        Open url after checking for not same page
        :param url: 待跳转的url
        :return: NULL
        """
        current_url = self.driver.current_url
        if url == current_url:
            pass
        else:
            self.driver.get(url)

    def login_with_account(self):
        """
        facebook login with username and password
        """
        self.get(self.root_url)
        try:
            # username
            email_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, "email")))
            email_element.clear()
            email_element.send_keys(self.email)
            self.driver.implicitly_wait(1)

            # password
            password_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, "pass")))
            password_element.clear()
            password_element.send_keys(self.password)
            self.driver.implicitly_wait(1)

            # click
            login_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, "u_0_b")))
            login_element.click()

            try:
                one_tap = WebDriverWait(self.driver, timeout=10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/form/div/button')))

                one_tap.click()
            except:
                pass
        except:
            pass

    def login_with_cookies(self):
        """
        facebook login with cookies
        """
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, 'r', encoding='utf-8') as file:
                list_cookies = json.loads(file.read())
            if len(list_cookies) != 0:
                self.driver.get(self.root_url)
                for cookie in list_cookies:
                    try:
                        self.driver.add_cookie({
                            "domain": cookie["domain"],
                            "name": cookie["name"],
                            "value": cookie["value"],
                            "path": cookie["path"],
                            # "expiry": cookie["expiry"]
                        })
                    except KeyError:
                        pass

                self.driver.get(self.root_url)

    def is_login_success(self):
        """
        Determine whether login is successful

        :return:
            login_status: False - Fail, True - Success
        """
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "uiFutureSideNav")))
            login_status = True
            print('login success')
        except:
            login_status = False

        return login_status

    def sign_in(self):
        """
        facebook login via webdriver, cookies login first, if no cookies, login with account and save the cookies
        :return: a status code —— True: Success, False: False

        """
        if os.path.exists(self.cookies_path):
            self.login_with_cookies()
        else:
            self.login_with_account()

        # status judgement
        if self.is_login_success():
            self.save_cookie()

    def save_cookie(self):

        if not os.path.exists("cookies"):
            os.mkdir("cookies")
        dict_cookies = self.driver.get_cookies()
        json_cookies = json.dumps(dict_cookies)
        if os.path.exists(os.path.join("./cookies", self.cookies_path)):
            pass
        else:
            with open(self.cookies_path, "w") as file:
                file.write(json_cookies)

    def url_type_judge(self, _url):
        """
        There are two types of user's homepage in facebook：
            1. https://www.facebook.com/erlyn.jumawan.7
            2. https://www.facebook.com/profile.php?id=100025029671192
        need to determine firstly the type of the url
        :param _url: url
        :return:
            _url_type: 1 or 2
        """
        url_root = self.root_url
        url_new = _url.replace(url_root, "")
        url_cut = url_new.split("?")
        if url_cut[0] == "profile.php":
            self._url_type = 2
        else:
            self._url_type = 1

        return self._url_type

    def get_user_id(self, url):
        """
        Get user's user_id or user name
        :param user_homepage_url
        :return: user id
        """
        if self.url_type_judge(url) == 1:
            self.user_id = url.split('/')[-1]
        else:
            self.user_id = url.split('=')[-1]

        return self.user_id

    def get_time(self, unix_time):
        """
        unix time stamp -> "%Y-%m-%d %H:%M:%S" time format
        e.g. 1522048036 -> 2018-03-26 15:07:16
        :param _unix_time_stamp
        :return:
            "%Y-%m-%d %H:%M:%S"
        """
        _format = "%Y-%m-%d"
        value = tm.localtime(unix_time)
        _time_string = tm.strftime(_format, value)

        return _time_string

    def storage(self, query, item):
        self.cur.execute(query, item)
        self.conn.commit()

    def get_posts(self, url):

        # identify url type
        self.user_id = self.get_user_id(url)
        page_type = self.url_type_judge(url)
        if page_type == 1:
            url_ = self.root_url + self.user_id
        else:
            url_ = self.root_url + 'profile.php?id=' + str(self.user_id)
        self.driver.get(url_)

        # Scroll down
        i = 0

        while i < 100:

            try:
                self.driver.find_element_by_class_name(self.timeline_loading_gif)
                self.page_down()
                tm.sleep(randint(1, 10) / 10)
                self.page_down()
                tm.sleep(randint(1, 10) / 10)
                self.page_down()
                tm.sleep(randint(1, 10) / 10)
                self.page_down()
                tm.sleep(randint(1, 10) / 10)
                i += 1
            except:
                print('No target')
                break

        # extract text
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        text_box = soup.find_all(class_=self.timeline_text_class)

        try:

            for text in text_box:
                try:
                    post = text.text
                    print(post)
                    insert = [self.user_id, post]
                    self.cur.execute(f"INSERT INTO text VALUES (?,?)", insert)
                except:
                    pass
            self.conn.commit()
            print('Txt completed')
        except:
            try:
                self.conn.commit()
            except:
                print('Cannot reach database')
                pass
            print('no text')
            pass

        intro = soup.find(class_=self.intro)
        try:
            bio = soup.find(class_='uiList _3-8x _2pic _4kg').find_all(class_='_1zw6 _md0 _5h-n _5vb9')
            bio_list = []
            for b in bio:
                try:
                    bio_list.append(b.text)
                except:
                    pass
            bio_list_json = json.dumps(bio_list)
        except:
            bio_list_json = ''

        try:
            len(intro)
            store_intro = [self.user_id, intro.text, bio_list_json]
            self.cur.execute(f"INSERT INTO intro VALUES (?,?,?)", store_intro)
            self.conn.commit()
        except:
            intro = ''
            store_intro = [self.user_id, intro, bio_list_json]
            self.cur.execute(f"INSERT INTO intro VALUES (?,?,?)", store_intro)
            self.conn.commit()

    def get_images(self, url):
        # identify url type
        self.user_id = self.get_user_id(url)
        page_type = self.url_type_judge(url)
        if page_type == 1:
            url_ = self.root_url + self.user_id + '/photos'
        else:
            url_ = self.root_url + 'profile.php?id=' + str(self.user_id) + '&sk=photos'
        self.get(url_)

        tm.sleep(randint(2, 5))
        if self.skip_non_exist() == False:
            return False

        if self.get_limitation():
            return 'limitied'

        # extract text
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        image_box = soup.find_all('li', class_=self.images_box)

        image_list = []
        try:
            for image in image_box:
                image = image.get('data-fbid')
                image_list.append(image)
            il_json = json.dumps(image_list)
        except:
            il_json = ''
        try:
            background = soup.find('img', class_=self.background).get('src')
        except:
            background = ''
        try:
            avatar = soup.find('a', class_=self.avatar).get('href')
            avatar_id = re.findall(r'(?<=\=).*?(?=\&)', avatar)[0]
        except:
            avatar_id = ''

        if il_json == background == avatar_id == '':
            return False

        store = [self.user_id, il_json, avatar_id, background]
        self.cur.execute(f"INSERT INTO images VALUES (?,?,?,?)", store)
        self.conn.commit()
        print('image submited')

    def get_info(self, url):
        self.user_id = self.get_user_id(url)
        page_type = self.url_type_judge(url)
        if page_type == 1:
            url_ = self.root_url + self.user_id + '/about?section=contact-info'
        else:
            url_ = self.root_url + 'profile.php?id=' + str(self.user_id) + 'sk=about&section=contact-info'
        self.get(url_)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        lang = ''
        gender = ''
        birth = ''
        p_view = ''
        try:
            lang = soup.find('li', class_='_3pw9 _2pi4 _2ge8', id='row_languages').find(class_='_4bl7 _pt5').text
        except:
            lang = ''
        try:
            birth = soup.find('li', class_='_3pw9 _2pi4 _2ge8 _4vs2').find(class_='_4bl7 _pt5').text
        except:
            birth = ''
        try:
            gender = soup.find('li', class_='_3pw9 _2pi4 _2ge8 _3ms8').find(class_='_4bl7 _pt5').text
        except:
            gender = ''
        try:
            p_view = soup.find('ul', class_='uiList _4kg _6-h _704 _6-i').text
        except:
            p_view = ''

        store = [self.user_id, lang, gender, birth, p_view]
        self.cur.execute(f"INSERT INTO info VALUES (?,?,?,?,?)", store)
        self.conn.commit()
        print('info submited')

    def get_limitation(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/a')
            return True
        except:
            return False


if __name__ == "__main__":
    # driver.quit()
    pass
