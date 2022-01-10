from __init__ import get_posts,get_group_info,get_page_info
import pymongo
import pickle
import time

from cookie import cookie
# client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
# pub = client['public']['Ru']
#
#
# with open('G:/Projects/Crawller/BasicCrawler/yangqi@mail.ru.pkl','rb') as f:
#     ck=pickle.load(f)

# names = ["MercedesBenz","mercedesbenzusa",'MercedesBenzUK',
#          "audi",'audiofficial','AudiUK','AudiCanada','BMW','BMWUSA','bmwuk','BMW.Canada',
#          "MazdaUK",'mazdacanada','toyotauk','toyota','TOYOTA.Global','porsche','FordCanada',
#          'Hyundai','hyundaiuk','kia','kiamotorsuk','kiacanada','skoda','Skoda.uk',
#          'subaruofamerica','OfficialSubaruUK','subaruofamerica','OfficialSubaruUK',
#          'suzukicarsuk','volvocars','VolvoCarUSA','volvocaruk','volvocarcanada',
#          'VW','renaultuk',"MercedesBenzRussia","AudiRussia","BMWRussia","MazdaRussia","toyotarussia",
#           'nissanrussia','porschemoscow','PorscheCenterRublevskiy','Chevrolet.Russia',
#           'citroenrussia','FordRussia','HyundaiRussia','InfinitiRussia','skodarussia']
# names2 = ["MercedesBenzRussia","AudiRussia","BMWRussia","MazdaRussia","toyotarussia",
#           'nissanrussia','porschemoscow','PorscheCenterRublevskiy','Chevrolet.Russia',
#           'citroenrussia','FordRussia','HyundaiRussia','InfinitiRussia','skodarussia']

# s = ['Citroen','Peugeot','infinitiglobal','GeelyAutoGlobal','ford',
#          'globalchevrolet']

s = ['nintendo']
result = []
for name in s:
    try:
        for post in get_posts(name,pages=99,extra_info=False,
                                       options={"comments": False, "reactors": False, "posts_per_page": 100,
                                                "progress": True,"cookie":cookie,"allow_extra_requests": False,
                                                },timeout=20):
        # for post in get_posts(name, pages=99, extra_info=False,
        #                           options={"comments": False, "reactors": False, "posts_per_page": 100,
        #                                    "progress": True,  "allow_extra_requests": False,
        #                                    }, timeout=20):
            result.append(post)
        # print(post)
        # pub.insert(post)
        # time.sleep(120)
    except Exception as e:
        print(e)

with open('g:/x.pkl','wb') as f:
    pickle.dump(result,f)

