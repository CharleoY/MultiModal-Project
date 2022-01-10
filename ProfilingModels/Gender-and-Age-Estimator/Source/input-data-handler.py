import csv
import re
import xml.etree.ElementTree as ET
import pickle
import pandas as pd


def extract_user_text (user):
    filename = 'Resources/data/' + user + '.xml'
    try:
        xml = ET.parse(filename)
    except:
        return ""
    root = xml.getroot()

    tweets = list()
    for documents in root:
        for document in documents:
            try:
                clean = re.sub('<[^>]*>', '', document.text)
                tweets.append(clean)
            except:
                continue

    return tweets


def build_target_data():
    target = open('Resources/data/truth.txt', 'r')
    target = target.readlines()

    with open ('Resources/data.csv', 'w') as data:
        datawriter = csv.writer(data)
        datawriter.writerow(['user', 'sex', 'age'])
        for users in target:
            user = users.split(':::')
            datawriter.writerow(user)


def main():
    build_target_data()

    data = pd.read_csv('Resources/data.csv')
    data = pd.DataFrame(data)

    users_texts_by_age = dict()
    users_texts_by_sex = dict()
    users_texts_by_id = dict()

    for index, row in data.iterrows():
        user = row['user']
        text_corpus = extract_user_text(user)
        for tweet in text_corpus:
            if not row['age'] in users_texts_by_age:
                users_texts_by_age[row['age']] = [tweet]
            else:
                users_texts_by_age[row['age']].append(tweet)

            if not row['sex'] in users_texts_by_sex:
                users_texts_by_sex[row['sex']] = [tweet]
            else:
                users_texts_by_sex[row['sex']].append(tweet)

            if not row['user'] in users_texts_by_id:
                users_texts_by_id[row['user']] = [tweet]
            else:
                users_texts_by_id[row['user']].append(tweet)

    #with open('Resources/' + 'users_texts_by_age' + '.pkl', 'wb') as f:
    #    pickle.dump(users_texts_by_age, f, pickle.HIGHEST_PROTOCOL)
    #with open('Resources/' + 'users_texts_by_sex' + '.pkl', 'wb') as f:
    #    pickle.dump(users_texts_by_sex, f, pickle.HIGHEST_PROTOCOL)
    #with open('Resources/' + 'users_texts_by_id' + '.pkl', 'wb') as f:
    #    pickle.dump(users_texts_by_id, f, pickle.HIGHEST_PROTOCOL)

    print("Success")

if __name__ == "__main__":
    main()