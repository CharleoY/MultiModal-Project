from avatar import *

import sqlite3 as sql
import time

def init(db='./db/data.db'):
    try:
        conn = sql.connect(db)
        cur = conn.cursor()

        table_users = """
                    CREATE TABLE IF NOT EXISTS
                        avatar(
                            user_id text PRIMARY KEY,

                            cover text,
                            
                            image text,
                            avatar text
                        );
                    """
        cur.execute(table_users)

    except:
        pass
init()

user_name_for_upload = ""
password_for_upload = ""
database='./db/data.db'
fb=Facebook(user_name_for_upload,password_for_upload,_database=database)

fb.sign_in()

user_list=fb.get_name_list()
for i,user in enumerate(user_list):


    print('No.',i,'User:',user)
    start=time.time()

    f=fb.get_avatar_first_20_images(user)
    time.sleep(fb.confusion(f))

    end=time.time()

    print('process time:',end-start)
