import vk_api
import pymongo

def get_posts(data,name):
    lis = []
    for d in data['items']:
        temp = {}
        temp['Vendor'] = name
        temp['id'] = d['id']
        temp['text'] = d['text']
        temp['mark'] = d['marked_as_ads']
        imgs = []
        try:

            for i in d['attachments']:
                if i['type']=='photo':
                    imgs.append(i['photo']['sizes'][-1]['url'])
                if i['type']=="video":
                    pass
        except:
            pass
        temp['imgs']=imgs
        lis.append(temp)
    return lis

def get_group_list(path):
    user = []
    with open(path,'r',encoding="utf8") as f:
        for u in f.readlines():
            user.append(u.replace('\n',''))
    return user

def get_user_id(group_id):
    data = vk.groups.getById(group_id=group_id)[0]
    id = data['id']
    name = data["name"]
    return id,name

def generator(num,domain):
    while num<9999:

        data = vk.wall.get(count = 99, domain = domain,filter="owner", offset = num)
        if len(data['items'])==0:
            return
        num=num+99
        yield data

if __name__ == "__main__":
    vk_session = vk_api.VkApi('+79992060809', 'DIUIByang2008')
    vk_session.auth()
    vk = vk_session.get_api()
    tools = vk_api.VkTools(vk_session)
    db = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")['ads']['VK']
    users = get_group_list("list.txt")
    print(users)

    for user in users:
        user_id,user_name = get_user_id(user)
        content = []
        i=0
        post_gen = generator(0, user)
        while True:
            try:
                print(f"{i} pages")
                data = next(post_gen)
                print(data)
                post = get_posts(data,user_name)
                content.extend(post)
                i+=1
            except:
                break
        db.insert_many(content)





