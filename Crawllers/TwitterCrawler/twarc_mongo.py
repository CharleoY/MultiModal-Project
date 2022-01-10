from pymongo import MongoClient,errors
from twarc import Twarc
from utils import auth_list,drop_fields
import pandas as pd
from tqdm.auto import tqdm


class crawler:
    def __init__(self,user_list=None):
        self.db_tweet = MongoClient(f"mongodb://127.0.0.1:27017/")['new']['tweets']
        self.db_user = MongoClient(f"mongodb://127.0.0.1:27017/")['new']['user']
        self.user_list = user_list


    def crawl(self,username=None):

        if self.user_list == None and username != None:
            pass

        if self.user_list != None and username == None:

            for i,user in enumerate(tqdm(self.user_list)):
                # if self.db_user.find()

                seed = i%4
                consumer_key, consumer_secret, access_token, access_token_secret = auth_list[seed][2], auth_list[seed][
                    3], auth_list[seed][0], auth_list[seed][1]
                T = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)
                posts = T.timeline(screen_name=user,max_pages=3)
                post_list = []
                for j,post in enumerate(posts):
                    user_info,post_info = drop_fields(post)
                    post_list.append(post_info)
                    try:
                        self.db_tweet.insert_one(post_info)
                    except errors.DuplicateKeyError:
                        print('duplicated')
                        print(post)
                    except Exception as e:
                        print(e)
                        print(post)

                try:
                    self.db_user.insert_one(user_info)
                    print(f"Crawled {len(post_list)} posts for No.{i} user {user}, id: {user_info['id_str']}")
                except errors.DuplicateKeyError:
                    print('duplicated user')
                except Exception as e:
                    print(e)

        else:
            raise('Need username or userlist')


if __name__=="__main__":

    import pickle
    with open('./list.pkl','rb') as f:
        user_name = pickle.load(f)
    crawl = crawler(user_list=user_name)
    crawl.crawl()
