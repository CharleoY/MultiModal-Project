import json
import re
from utils import time_parser
import langdetect

def tweet(x,user_id):
    query = []
    try:
        for i, item in enumerate(x.children):
            if "This content isn't available right now" in str(item.h3):
                continue
            text = ''
            ori_lang = ''
            retweet_lang = ''
            Image = {}
            retweetID = ''
            retweetUser = ''
            retweetText = ''
            retweetImage = {}
            reaction = {}
            attrs = json.loads(item['data-ft'])
            post_id = attrs.get('top_level_post_id')
            userID = user_id
            retweet = attrs.get('original_content_id')
            try:
                t = time_parser(item.abbr.text)
            except:
                continue
            if retweet == None:
                retweet = False

                try:
                    text = item.p.text
                    ori_lang = langdetect.detect(text)
                except:
                    pass

                try:
                    img = item.find('div', attrs={'data-ft': '{"tn":"H"}'}).findAll('a')
                    for im in img:
                        Image[re.findall(r"\/photo\.php\?fbid=\s*(.+)&id", im['href'])[0]] = im.img['alt']
                except Exception as e:
                    pass


            else:
                retweet = True
                retweetID = attrs.get('original_content_id')
                retweetUser = attrs.get('original_content_owner_id')
                try:
                    text = item.find('div', attrs={'data-ft': '{"tn":"*s"}'}).text
                    ori_lang = langdetect.detect(text)
                except:
                    pass
                try:
                    retweetText = item.find('div', attrs={'data-ft': '{"tn":"H"}'}).find('div', attrs={
                        'data-ft': '{"tn":"*s"}'}).text
                    retweet_lang = langdetect.detect(retweetText)
                except:
                    pass

                try:
                    img = item.find('div', attrs={'data-ft': '{"tn":"H"}'}).find('div',
                                                                                 attrs={'data-ft': '{"tn":"H"}'}).findAll(
                        'a')
                    for im in img:
                        try:
                            retweetImage[re.findall(r"\/photo\.php\?fbid=\s*(.+)&id", im['href'])[0]] = im.img['alt']
                        except:
                            retweetImage[re.findall(r"\/(\d+)\/\?type", im['href'])[0]] = im.img['alt']
                except Exception as e:
                    pass
            try:
                react = item.footer.find(id=f'like_{post_id}').a['aria-label'].replace('reactions, including ', '').replace(
                    'reaction, including ', '').replace(',', '').replace('and ', '')
                num = re.findall(r'(\d+)', react)[0]
                react = re.sub(r'(\d+) ', '', react)
                reaction[int(num)] = react
            except Exception as e:
                pass

            content = {'postID': str(post_id), 'userID': str(userID), 'text': text, 'image': json.dumps(Image), 'datetime': t,
                       'retweet': retweet, 'retweetID': str(retweetID), 'retweetUser': str(retweetUser), "retweetText": retweetText,
                       'retweetImage': json.dumps(retweetImage), 'reaction': json.dumps(reaction),'Language':ori_lang,"Retweet_lang":retweet_lang}
            if (content['text']=='' and content['image']=='{}' and content['retweet']==False) :
                continue
            if (content['retweetImage']=='{}' and content['retweetText']=='' and content['retweet']==True and content['text']==''):
                continue
            query.append(content)
        if len(query)>0:
            return query
        else:
            return 0
    except:
        return 0

def userInfo(soup,user_id,tree):
    temp = {'userID':user_id}
    for key in ['basic-info', "contact-info", "living", "relationship", "bio", 'education', 'bio2']:
        try:
            if key == 'education':
                try:
                    for item in soup.findAll('header'):
                        item.extract()

                    for item in soup.find(id=key).div.div.findChildren(recursive=False)[0]:
                        temp = {**temp, **{'Education': item.div.findChildren(recursive=False)[0].text}}
                        temp = {**temp, **{'Specialist': item.div.findChildren(recursive=False)[1].text}}
                    continue
                except:
                    continue
            if key == 'relationship' or key == 'bio':
                temp = {**temp, **{key.capitalize(): soup.find(id=key).div.div.text}}
                continue
            if key == 'bio2':
                temp = {**temp, **{
                    key.capitalize(): ' '.join(tree.xpath('//*[@id="root"]/div[1]/div[1]/div[2]/div[2]/text()'))}}

            for item in soup.find(id=key).div.div.findAll('tr'):
                if key == "living":

                    if item.findChildren(recursive=False)[0].text in ['Current City', 'Hometown']:

                        temp = {**temp, **{
                            item.findChildren(recursive=False)[0].text.replace('.',''): item.findChildren(recursive=False)[1].text}}
                    else:
                        pass

                else:
                    temp = {**temp,
                            **{item.findChildren(recursive=False)[0].text.replace('.',''): item.findChildren(recursive=False)[1].text}}
        except:
            pass
    return temp
