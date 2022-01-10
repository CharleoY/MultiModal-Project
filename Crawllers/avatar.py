import time as tm
import os
import re
import ast
import json
import sqlite3 as sql
import pandas as pd
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from random import choice
from random import randint


# import utils1
#
# logger = utils1.configure_root_logger()

class Facebook:


    def __init__(self, _email=None, _password=None, _browser_type="Chrome", _is_headless=False, _database=None):

        # the variables which are fixed
        self.url = "https://www.facebook.com/"  # facebook root url
        self.email = _email  # email
        self.password = _password  # password

        # some identifier
        self.browser_state = None  # browser_state
        self.login_state = None  # login_state

        # some parameters of webdriver
        self.cookies_path = "./cookies/new/cookies(" + _email + ").json"  # path to save cookie

        self.gender = None

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

                    options.add_argument('--allow-running-insecure-content')
                    prefs = {"profile.managed_default_content_settings.images": 2}
                    options.add_experimental_option("prefs", prefs)
                    options.add_argument("--disable -gpu")
                    options.add_argument("--headless")

                    self.driver = webdriver.Chrome(options=options)
                else:
                    # options.add_argument('--allow-running-insecure-content')
                    # prefs = {"profile.managed_default_content_settings.images": 2}
                    # options.add_experimental_option("prefs", prefs)
                    # self.driver = webdriver.Chrome(options=options)

                    options.add_argument(
                        r"user-data-dir=C:/Users/yang/AppData/Local/Google/Chrome/User Data/")  # 把数据传入程序
                    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止网站发现我们使用模拟器
                    self.driver = webdriver.Chrome()
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
        self.get(self.url)
        if self.database != None:
            self.conn = sql.connect(self.database)
            self.cur = self.conn.cursor()
            print('connected')

    def click(self,tag):
        action = ActionChains(self.driver)
        action.click(self.driver.find_element_by_link_text(tag)).perform()

    def page_down(self):
        body = self.driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)

    def check_existance(self,user_id):
        self.cur.execute("SELECT * FROM 'avatar' WHERE user_id='{}';".format(user_id))
        row=self.cur.fetchall()
        if len(row) != 0:
            return True
        else:
            return False

    def skip_non_exist(self):
        try:
            self.driver.find_element_by_class_name('_4-dp')
            return False
        except:
            return True


    def confusion(self,f=True):
        if f!=False:
            c=60
            tags=['Timeline','About','Friends','Albums']
            try:
                tag=choice(tags)
                self.click(tag)
                a=randint(1,3)
                tm.sleep(a)
                self.page_down()
                b=randint(1, 3)
                tm.sleep(b)
                self.page_down()
                c=c-a-b
            except:
                pass

            return c
        else:
            return 0

    def get_name_list(self,user=False):
        """
        get user_info from file
        :return: name_list
        """
        df = pd.read_csv(self.file_loc, index_col=0, header=0)
        if user==False:
            name_list = df['url'].tolist()
        else:
            name_list = df['user_id'].tolist()
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
        self.get(self.url)
        try:
            # username
            email_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.NAME, "email")))
            email_element.clear()
            email_element.send_keys(self.email)
            self.driver.implicitly_wait(1)

            # password
            password_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.NAME, "pass")))
            password_element.clear()
            password_element.send_keys(self.password)
            self.driver.implicitly_wait(1)

            # click
            login_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.NAME, "login")))
            login_element.click()

            # click ok to continue
            self.driver.implicitly_wait(1)
            login_element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bj")))
            login_element.click()


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
                self.driver.get(self.url)
                for cookie in list_cookies:
                    try:
                        self.driver.add_cookie({
                            "domain": cookie["domain"],
                            "name": cookie["name"],
                            "value": cookie["value"],
                            "path": cookie["path"],

                        })
                    except KeyError:
                        pass

                self.driver.get(self.url)

    def is_login_success(self):
        """
        Determine whether login is successful

        :return:
            login_status: False - Fail, True - Success
        """
        try:
            WebDriverWait(self.driver, timeout=20).until(EC.presence_of_element_located((By.ID, "u_0_d")))
            login_status = True
            print('login success')
        except:
            login_status = False
            print('login failed')

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

    def page_refresh_to_bottom(self, item, timeout=1, poll_frequency=0.1):
        """
        Scroll down the page
        :param item
        :param timeout
        :param poll_frequency
        :return: NULL
        """

        if item == 'timeline':
            length = 0
            while length <= 130:  # how many scroll down need to perform
                page = self.driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                a = soup.find(id='structured_composer_async_container')
                try:
                    b = a.find_all('article')
                    length = len(b)
                except:
                    pass

                try:
                    self.driver.find_element_by_css_selector("[class='_52jj _2ph_']")
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')


                except:
                    break

        ###future fuction, to crawl the user info and album

        # elif item == "users":
        #     while True:
        #         try:
        #             WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency).until(
        #                 EC.presence_of_element_located((By.XPATH, self.bottom_id_search)))
        #             break
        #         except:
        #             self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #             self.driver.implicitly_wait(randint(1, 5))
        #
        else:
            length = 0
            while length <= 100:  # how many scroll down need to perform
                page = self.driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                thumbnail_area = soup.find(id="thumbnail_area")
                try:
                    length = len(thumbnail_area)
                except:
                    break

                try:
                    self.driver.find_element_by_css_selector("[class='centeredIndicator']")
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')


                except:
                    break

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
        url_root = "https://www.facebook.com/"
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

    def get_sex(self, url):
        """
        Get gender of current usr
        :param url
        :return:
            gender or None
        """
        url_type = self.url_type_judge(url)
        self.get_user_id(url)

        if url_type == 1:
            page = 'https://mobile.facebook.com/' + str(self.user_id) + '/about'
            self.get(page)
        else:
            page = 'https://mobile.facebook.com/profile.php?v=info&id=' + str(self.user_id)
            self.get(page)

        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        try:
            a = soup.find(title='Gender')
            self.gender = a.find(class_="_5cdv r").text
            print(self.gender)
            return self.gender
        except:
            return None
            pass

    def get_timeline(self, url):
        """
        Get user's timeline data
        :param url
        :return:
            Timeline data [user_id, time, text,gender]
        """
        time = None
        text = None
        self.get_user_id(url)
        self.get_sex(url)
        tm.sleep(1)
        self.get(url)
        try:
            self.driver.find_element_by_css_selector('[class="_mBrokenLinkPage__backToFeed"]')
            return 0
        except:
            pass
        self.page_refresh_to_bottom('timeline')
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        container = soup.find(id='structured_composer_async_container')
        try:
            text_container = container.find_all('article')
        except:
            return 0

        for item in text_container:
            try:
                text = item.p.text
            except:
                text = None
                pass
            try:
                time_ = item.find(class_='_52jc _5qc4 _78cz _24u0 _36xo')
                time = time_.abbr.text
            except:
                time = None
                pass

            timeline = [self.user_id, time, text, self.gender]
            if text != None:
                try:

                    self.cur.execute(f"INSERT INTO users VALUES (?,?,?,?)", timeline)

                except sql.IntegrityError:
                    print(Exception)
        self.conn.commit()
        # photo

    def get_photo(self, url):
        self.get_user_id(url)
        if self.url_type_judge(url) == 1:
            self.get('https://mobile.facebook.com/' + str(self.user_id) + '/photos')
        else:
            url_ = 'https://mobile.facebook.com/profile.php?v=photos&id=' + str(self.user_id)

            self.get(url_)
        try:
            album_element = WebDriverWait(self.driver, timeout=1).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='m_more_albums']")))
            album_element.click()
        except:
            pass

        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        Catagory = soup.find_all(class_="item _50lb tall acw abb")

        album_list = []
        for item in Catagory:
            herf = item.a.attrs['href']
            album_url = self.url + herf
            album_list.append(album_url)
        for url in album_list:
            self.get(url)
            try:
                button_element = WebDriverWait(self.driver, timeout=1).until(
                    EC.presence_of_element_located((By.TAG_NAME, "button")))
                button_element.click()
            except:
                pass
            try:
                self.page_refresh_to_bottom('photo')
            except:
                pass
            page = self.driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            thumbnail_area = soup.find(id="thumbnail_area")
            if thumbnail_area != None:
                for i, item in enumerate(thumbnail_area):
                    url_dic = item.i.attrs['data-store']
                    photo = ast.literal_eval(url_dic)['imgsrc']
                    photo = photo.replace('\\', '')
                    photolist = [self.user_id, photo, self.gender]
                    if photo != None:
                        try:

                            self.cur.execute(f"INSERT INTO image VALUES (?,?,?)", photolist)

                        except sql.IntegrityError:
                            print(Exception)
                self.conn.commit()

    def get_avatar(self, url):
        self.url_type_judge(url)
        self.get_user_id(url)
        print(self.user_id)
        pattern = "https://mbasic.facebook.com/photo/view_full_size/?fbid={}&ref_component=mbasic_photo_permalink&ref_page=%2Fwap%2Fphoto.php&refid=13&ref=104&__tn__=%2Cg&ref_component=mbasic_photo_permalink&ref_page=%2Fwap%2Fphoto.php&refid=13&ref=104&__tn__=%2Cg"
        self.get(url)
        self.driver.implicitly_wait(2)
        try:
            cc = WebDriverWait(self.driver, timeout=5).until(EC.presence_of_element_located((By.ID, "cover-name-root")))
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            image_href = soup.find_all(class_='_39pi _1mh-')
            if len(image_href) != 0:
                BG_id = re.findall(r'(?<=\=).*?(?=\&)', image_href[0].get('href'))[0]
                PF_id = re.findall(r'(?<=\=).*?(?=\&)', image_href[1].get('href'))[0]
                BG_url = pattern.format(BG_id)
                PF_url = pattern.format(PF_id)
                self.driver.get(PF_url)
                img = self.driver.current_url
                self.driver.get(BG_url)
                BG = self.driver.current_url
                print(img, '\n', BG)
                img_list = [self.user_id, img, BG]
                if 'fbcdn' not in BG:
                    raise ValueError("URL is not correct.")
                if PF_url != None:
                    try:
                        self.cur.execute(f"INSERT INTO avatar VALUES (?,?,?)", img_list)
                    except sql.IntegrityError:
                        print(Exception)
                    self.conn.commit()
            else:
                img = 'None'
                BG = 'None'
                img_list = [self.user_id, img, BG]
                try:
                    self.cur.execute(f"INSERT INTO avatar VALUES (?,?,?)", img_list)
                except sql.IntegrityError:
                    print(Exception)
                self.conn.commit()

        except Exception as e:
            print(e)

    def get_file(self, url):
        pass


    def get_avatar_first_20_images(self, url):
        self.url_type_judge(url)
        self.get_user_id(url)
        print(self.user_id)

        if not self.check_existance(self.user_id):

            if self.url_type_judge(url) == 1:
                self.get('https://www.facebook.com/' + str(self.user_id) + '/photos')
            else:
                url_ = 'https://www.facebook.com/profile.php?id=' + str(self.user_id) + '&sk=photos'
                self.get(url_)
            try:
                cc = WebDriverWait(self.driver, timeout=5).until(
                    EC.presence_of_element_located((By.ID, "pagelet_timeline_medley_photos")))
                page = self.driver.page_source
                soup = BeautifulSoup(page, 'html.parser')

                # cover url
                cover = ''
                try:
                    finds = soup.find_all(class_='cover')
                    cover = finds[0].a.get('ajaxify')
                except:
                    print('error_covers')
                    pass
                print('cover: \n', cover)

                # first 20 images
                urls = soup.find(class_='fbStarGrid _69n fbPhotosRedesignBorderOverlay')
                if urls == None:
                    urls = soup.find(class_='fbStarGrid _69n fbPhotosRedesignBorderOverlay fbStarGridAppendedTo')
                images = []
                try:
                    for item in urls.children:
                        images.append(item.a.get('href'))

                    print('images:\n', images)
                except:
                    print('error_images')
                    pass
                images = json.dumps(images)

                # avatar url
                avatar = ''
                try:
                    link = soup.find(class_='_1nv3 _11kg _1nv5 profilePicThumb')
                    avatar = link.get('href')

                    if 'https' not in avatar:
                        avatar=self.get_avatar_irregular()
                    print('avatar: \n', avatar)
                except:
                    print('error: avatar1')

                img_list = [self.user_id, cover, images, avatar]
                if self.database != None:
                    try:
                        self.cur.execute(f"INSERT INTO avatar VALUES (?,?,?,?)", img_list)
                    except sql.IntegrityError:
                        print('error sql:')
                        print(Exception)
                    self.conn.commit()
                else:
                    print(img_list)

            except Exception as e:
                print('error tag:',e)
                return False
        else:
            print('Already exist, skip to next.')
            return False


    def get_avatar_irregular(self):
        avatar_link = ''
        try:

            tm.sleep(1)
            element = self.driver.find_element_by_class_name('_11kf')
            element.click()
            tm.sleep(2)
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            parser=soup.find(class_='_4-od')
            avatar_link=parser.div.img.get('src')


        except:
            print('error: avatar2')

        return avatar_link











if __name__ == "__main__":
    # driver.quit()
    pass
