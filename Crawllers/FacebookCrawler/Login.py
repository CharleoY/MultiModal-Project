import requests
from bs4 import BeautifulSoup
import os
import pickle



def cookie():
    cookies={}

    cookies2 = {}
    x = [cookies,cookies2]

    return x

def saveCookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def loadCookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def Login(email, password):
    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0',
        "referer": "https://mbasic.facebook.com/login/save-device/?login_source=login&refsrc=https%3A%2F%2Fmbasic.facebook.com%2F&_rdr",
        "accept-language": "en-US,en;q=0.9"})
    if os.path.exists("{}.pkl".format(email)):
        print('Loading Cookies')
        cookies = loadCookies("{}.pkl".format(email))
        session.cookies.update(cookies)

    else:
        print("Use Password Login")
        response = session.get('https://mbasic.facebook.com')
        response = session.post('https://mbasic.facebook.com/login.php', data={
            'email': email,
            'pass': password
        }, allow_redirects=False)

    response = session.get('https://mbasic.facebook.com')
    print(response.status_code)
    content = BeautifulSoup(response.content,"html.parser")

    if content.find(placeholder="What's on your mind?") != None:
        saveCookies(session.cookies, "{}.pkl".format(email))
        print('Login Success')
        return session
    else:
        raise ValueError("Login Failed")




