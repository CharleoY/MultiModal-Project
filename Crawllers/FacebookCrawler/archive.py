
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import time


ROOT_URL = "https://mbasic.facebook.com/"
nextMemberPage='m_more_item'
memberPage = 'https://mbasic.facebook.com/browse/group/members/?id={}&start=0&listType=list_nonfriend_nonadmin&refid=18'


def getNextPage(source):
    try:
        nextPage = ROOT_URL+source.find(id=nextMemberPage).a['href']
        return nextPage
    except:
        return 0

def getUserIDandName(source):

    user_list=[]
    for item in source.findAll('table')[2:]:
        try:
            user_list.append((item.a.text, item['id'][7:]))
        except:
            print('Error')
    return user_list
for j in tqdm(range(df.shape[0])):
    i = 1
    item = df.iloc[j]
    groupname = item['name']
    groupurl = item['url']
    groupid = item['id']
    amount = item['member']
    grouptype = item['type']
    print(f'Scrap group:{groupname}, {amount} users')
    nextPage = session.get(memberPage.format(str(groupid)))
    if nextPage.status_code == 200:
        while i==1:
            source = BeautifulSoup(nextPage.content,'html.parser')
            userList = getUserIDandName(source)
            queryList = []
            for u in userList:
                username = u[0]
                userid = u[1]
                page = nextPage.url
                type_= grouptype
                user = {"ID":userid, "Name":username,"Type":grouptype,"Page":page}
                print(f"Insert {user} into MongoDB")
                queryList.append(user)
            USER.insert_many(queryList)

            nextPage = getNextPage(source)
            if nextPage != 0:
                nextPage = session.get(nextPage)
                print(f'Successful get next page : {nextPage.url}')
                time.sleep(10)
            else:
                i=nextPage
    else:
        time.sleep(300)
