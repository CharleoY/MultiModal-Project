import pickle
import pandas as pd
import numpy as np
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os


#GLOBAL VARIABLES SECTION
users_texts_by_age = dict()
users_texts_by_sex = dict()
users_texts_by_id = dict()
data = pd.DataFrame()

cachedStopWords = stopwords.words("english")
exclude = set(string.punctuation)
stemmer = PorterStemmer()
#GLOBAL VARIABLES SECTION END

def prepare_text(text):
    global cachedStopWords, exclude, stemmer
    text = re.sub(r'@[A-Za-z0-9_-]*', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'#[A-Za-z0-9_-]*', '', text)
    text = re.sub(r'pic\S+', '', text)

    text = nltk.word_tokenize(text)
    for i in range(0, text.__len__()):
        text[i] = text[i].lower()
        text[i] = stemmer.stem(text[i])

    return text


def get_mentions (text):
    try:
        mentions = re.findall('@[A-Za-z0-9_-]*', text)
        return mentions.__len__()
    except:
        return 0


def read_data():
    global users_texts_by_age, users_texts_by_sex, users_texts_by_id, data
    file = open('Resources/users_texts_by_age.pkl', 'rb')
    users_texts_by_age = pickle.load(file)
    file = open('Resources/users_texts_by_sex.pkl', 'rb')
    users_texts_by_sex = pickle.load(file)
    file = open('Resources/users_texts_by_id.pkl', 'rb')
    users_texts_by_id = pickle.load(file)
    data = pd.read_csv('Resources/data.csv')
    data = pd.DataFrame(data)


def define_features():
    # Define feature columns in dataset
    global data
    # v1
    data['user_common_1grams'] = 0
    data['user_common_2grams'] = 0
    data['user_common_3grams'] = 0
    data['user_age_18_24_ngrams'] = 0
    data['user_age_25_34_ngrams'] = 0
    data['user_age_35_49_ngrams'] = 0
    data['user_age_50_64_ngrams'] = 0
    data['user_age_65_xx_ngrams'] = 0
    data['user_gender_male_ngrams'] = 0
    data['user_gender_female_ngrams'] = 0
    data['avr_mentions'] = 0
    data['avr_punctuation'] = 0
    # v2
    data['avr_text_size'] = 0
    data['avr_starts_with_capital'] = 0
    data['avr_ends_with_punctuation'] = 0
    data['avr_capitals'] = 0
    data['avr_words_count'] = 0
    data['vocabulary_richness'] = 0


def define_pos_tag_features():
    # define empty columns for pos-tagging features
    global data
    data['CC'] = 0
    data['CD'] = 0
    data['DT'] = 0
    data['EX'] = 0
    data['FW'] = 0
    data['IN'] = 0
    data['JJ'] = 0
    data['JJR'] = 0
    data['JJS'] = 0
    data['LS'] = 0
    data['MD'] = 0
    data['NN'] = 0
    data['NNS'] = 0
    data['NNP'] = 0
    data['NNPS'] = 0
    data['PDT'] = 0
    data['POS'] = 0
    data['PRP'] = 0
    data['PRP$'] = 0
    data['RB'] = 0
    data['RBR'] = 0
    data['RBS'] = 0
    data['RP'] = 0
    data['SYM'] = 0
    data['TO'] = 0
    data['UH'] = 0
    data['VB'] = 0
    data['VBD'] = 0
    data['VBG'] = 0
    data['VBN'] = 0
    data['VBP'] = 0
    data['VBZ'] = 0
    data['WDT'] = 0
    data['WP'] = 0
    data['WP$'] = 0
    data['WRB'] = 0
    return


def calculate_mentions_feature():
    # Calculate average number of mentions per user/age group/sex group
    global data, users_texts_by_age, users_texts_by_id, users_texts_by_sex
    data['avr_user_mentions'] = 0
    data['avr_user_mentions'] = data['avr_user_mentions'].astype(np.float)
    for index, row in data.iterrows():
        user = row['user']
        mentions = 0
        tweets_size = 0
        try:
            tweets = users_texts_by_id[user]
        except:
            continue
        for tweet in tweets:
            mentions += get_mentions(tweet)
            tweets_size += 1
        avr_mentions = (float)(mentions / tweets_size)
        data.avr_user_mentions[data.user == user] = avr_mentions

    data['avr_age_group_mentions'] = 0
    data['avr_age_group_mentions'] = data['avr_age_group_mentions'].astype(np.float)
    for age in users_texts_by_age:
        age_summary_mentions = 0
        age_summary_tweets = 0
        for tweet in users_texts_by_age[age]:
            age_summary_tweets += 1
            age_summary_mentions += get_mentions(tweet)

        age_avr_mentions = (float)(age_summary_mentions / age_summary_tweets)
        data.avr_age_group_mentions[data.age == age] = age_avr_mentions

    data['avr_sex_group_mentions'] = 0
    data['avr_sex_group_mentions'] = data['avr_sex_group_mentions'].astype(np.float)
    for sex in users_texts_by_sex:
        sex_summary_mentions = 0
        sex_summary_tweets = 0
        for tweet in users_texts_by_sex[sex]:
            sex_summary_tweets += 1
            sex_summary_mentions += get_mentions(tweet)

        sex_avr_mentions = (float)(sex_summary_mentions / sex_summary_tweets)
        data.avr_sex_group_mentions[data.sex == sex] = sex_avr_mentions

        # MEANTIONS FEATURE SECTION END
    return


def get_ngrams(texts, n):
    # Calculates dictionary of ngrams for list of texts
    ngrams = dict()
    global cachedStopWords, exclude, stemmer
    for text in texts:
        text = prepare_text(text)
        text = ' '.join([word for word in text if word not in cachedStopWords])
        text = ''.join(ch for ch in text if ch not in exclude)

        text = nltk.word_tokenize(text)

        ngrams_list = nltk.ngrams(text, n)
        ngrams_list = [ ''.join(grams) for grams in ngrams_list]
        for ngram in ngrams_list:
            if not ngram in ngrams:
                ngrams[ngram] = 1
            else:
                ngrams[ngram] += 1
    return ngrams


def get_punctuation(text):
    # Calculate number of punctuations in given text
    punctuation_num = 0
    text = prepare_text(text)
    punctuation = ''.join(ch for ch in text if ch  in exclude)
    punctuation_num += punctuation.__len__()
    return punctuation_num


def calculate_ngrams_dicts():
    # Calculate the most popular ngrams for age/sex classes
    # TODO uncomment if neccessary!
    # nltk.download()


    # dictionary of dictionaries for 1000 most popular ngrams
    age_ngrams_dict = dict()

    # most common age ngrams
    for i in range(1, 4):
        # Building dictionaries of ngrams
        if i not in age_ngrams_dict:
            age_ngrams_dict[i] = dict()
        else:
            continue

        for age in users_texts_by_age:
            age_ngram = get_ngrams(users_texts_by_age[age], i)
            age_ngram = list(reversed(sorted(age_ngram, key=age_ngram.get)))
            if(age_ngram.__len__() >= 100):
                age_ngram = age_ngram[0:100]
            age_ngrams_dict[i][age] = [age_ngram]

    with open('Resources/' + 'age_ngrams_dict_100' + '.pkl', 'wb') as f:
        pickle.dump(age_ngrams_dict, f, pickle.HIGHEST_PROTOCOL)

    sex_ngrams_dict = dict()
    for i in range(1, 4):
        if i not in sex_ngrams_dict:
            sex_ngrams_dict[i] = dict()
        else:
            continue

        for sex in users_texts_by_sex:
            sex_ngrams = get_ngrams(users_texts_by_sex[sex], i)
            sex_ngrams = list(reversed(sorted(sex_ngrams, key=sex_ngrams.get)))
            if sex_ngrams.__len__() > 100:
                sex_ngrams = sex_ngrams[0:100]
            sex_ngrams_dict[i][sex] = [sex_ngrams]

    with open('Resources/' + 'sex_ngrams_dict_100' + '.pkl', 'wb') as f:
        pickle.dump(sex_ngrams_dict, f, pickle.HIGHEST_PROTOCOL)
    return


def calculate_common_ngrams_dict():
    global users_texts_by_id
    common_ngrams_dict = dict()
    count = 0
    for user in users_texts_by_id:
        count += 1
        texts = users_texts_by_id[user]
        for i in range(1, 4):
            if i not in common_ngrams_dict:
                common_ngrams_dict[i] = dict()
            user_ngrams = get_ngrams(texts, i)
            for ngram in user_ngrams:
                if ngram not in common_ngrams_dict[i]:
                    common_ngrams_dict[i][ngram] = 1
                else:
                    common_ngrams_dict[i][ngram] += 1
        print (str(count) + ' ' + str(user) + ' ngrams calculated')

    for i in range(1, 4):
        common_ngrams_dict[i] = list(reversed(sorted(common_ngrams_dict[i], key=common_ngrams_dict[i].get)))
        if common_ngrams_dict[i].__len__() > 100:
            common_ngrams_dict[i] = common_ngrams_dict[i][0:100]

    with open('Resources/' + 'common_ngrams_dict_100' + '.pkl', 'wb') as f:
        pickle.dump(common_ngrams_dict, f, pickle.HIGHEST_PROTOCOL)
    return


def calculate_pos_tag_features(texts):
    # calculate average number of each part of speech per message in user texts, using https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    pos_tag_dict = dict()
    global exclude
    for text in texts:
        # looks life prepare text function but without stemming
        text = re.sub(r'@[A-Za-z0-9_-]*', '', text)
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'#[A-Za-z0-9_-]*', '', text)
        text = re.sub(r'pic\S+', '', text)
        text = nltk.word_tokenize(text)

        text = nltk.pos_tag(text)
        for pos_tag in text:
            if pos_tag[1] in exclude:
                continue
            if pos_tag[1] not in pos_tag_dict:
                pos_tag_dict[pos_tag[1]] = 1
            else:
                pos_tag_dict[pos_tag[1]] += 1

    return pos_tag_dict


def calculate_features():
    # Calculates features for every user in dataset
    global data, users_texts_by_id, exclude
    file = open('Resources/common_ngrams_dict.pkl', 'rb')
    common_ngrams_dict = pickle.load(file)
    file = open('Resources/age_ngrams_dict.pkl', 'rb')
    age_ngrams_dict = pickle.load(file)
    file = open('Resources/sex_ngrams_dict.pkl', 'rb')
    gender_ngrams_dict = pickle.load(file)
    
    count = 0
    for index, row in data.iterrows():
        count += 1
        user = row['user']

        try:
            texts = users_texts_by_id[user]
        except:
            continue

        # ngrams feature section
        # num_common_ngrams = 0
        # num_age_18_24_ngrams = 0
        # num_age_25_34_ngrams = 0
        # num_age_35_49_ngrams = 0
        # num_age_50_64_ngrams = 0
        # num_age_65_xx_ngrams = 0
        # num_gender_male_ngrams = 0
        # num_gender_female_ngrams = 0
        #
        #
        #
        # for i in range(1, 4):
        #     user_ngrams = get_ngrams(texts, i)
        #     for ngram in user_ngrams:
        #         # common section
        #         if ngram in common_ngrams_dict[i]:
        #             num_common_ngrams += 1
        #
        #         if i == 1:
        #             # age section
        #             if ngram in age_ngrams_dict[1]['18-24\n'][0]:
        #                 num_age_18_24_ngrams += 1
        #             if ngram in age_ngrams_dict[1]['25-34\n'][0]:
        #                 num_age_25_34_ngrams += 1
        #             if ngram in age_ngrams_dict[1]['35-49\n'][0]:
        #                 num_age_35_49_ngrams += 1
        #             if ngram in age_ngrams_dict[1]['50-64\n'][0]:
        #                 num_age_50_64_ngrams += 1
        #             if ngram in age_ngrams_dict[1]['65-xx\n'][0]:
        #                 num_age_65_xx_ngrams += 1
        #
        #             # gender section
        #             if ngram in gender_ngrams_dict[1]['MALE'][0]:
        #                 num_gender_male_ngrams += 1
        #             if ngram in gender_ngrams_dict[1]['FEMALE'][0]:
        #                 num_gender_female_ngrams += 1
        #
        #
        #     avr_ngrams = float(num_common_ngrams / len(texts))
        #
        #     if i == 1:
        #         data.user_common_1grams[data.user == user] = avr_ngrams
        #         # age
        #         data.user_age_18_24_ngrams[data.user == user] = float(num_age_18_24_ngrams / len(texts))
        #         data.user_age_25_34_ngrams[data.user == user] = float(num_age_25_34_ngrams / len(texts))
        #         data.user_age_35_49_ngrams[data.user == user] = float(num_age_35_49_ngrams / len(texts))
        #         data.user_age_50_64_ngrams[data.user == user] = float(num_age_50_64_ngrams / len(texts))
        #         data.user_age_65_xx_ngrams[data.user == user] = float(num_age_65_xx_ngrams / len(texts))
        #         # gender
        #         data.user_gender_male_ngrams[data.user == user] = float(num_gender_male_ngrams / len(texts))
        #         data.user_gender_female_ngrams[data.user == user] = float(num_gender_female_ngrams / len(texts))
        #     elif i == 2:
        #         # common
        #         data.user_common_2grams[data.user == user] = avr_ngrams
        #     elif i == 3:
        #         data.user_common_3grams[data.user == user] = avr_ngrams
        #
        # data.to_csv('Resources/data_ngrams.csv', sep='\t')
        # ngram feature section end


        # punctuation/mentions/text size/starts with capital/words count/ends with punctuation features section
        num_punctuations = 0
        num_mentions = 0
        all_texts_size = 0
        words_count = 0
        starts_with_capital = 0
        ends_with_punctuation = 0
        # TODO calculate average capitals!
        for text in texts:
            num_punctuations += get_punctuation(text)
            num_mentions += get_mentions(text)
            all_texts_size += len(text)
            words_count = len(text.split(' '))
            try:
                if text[0].isupper():
                    starts_with_capital += 1
            except:
                print ('Error in text[0]: ' + text)
            try:
                if text[len(text) - 1] in exclude:
                    ends_with_punctuation += 1
            except:
                print ('Error in text[last]: ' + text)

        # v1
        avr_punctuation = float(num_punctuations / len(texts))
        avr_mentions = float(num_mentions / len(texts))
        # v2
        avr_text_size = float(all_texts_size / len(texts))
        avr_words_count = float(words_count / len(texts))
        avr_starts_with_capital = float(starts_with_capital / len(texts))
        avr_ends_with_punctiation = float(ends_with_punctuation / len(texts))

        data.avr_punctuation[data.user == user] = avr_punctuation
        data.avr_mentions[data.user == user] = avr_mentions
        data.avr_text_size[data.user == user] = avr_text_size
        data.avr_words_count[data.user == user] = avr_words_count
        data.avr_starts_with_capital[data.user == user] = avr_starts_with_capital
        data.avr_ends_with_punctuation[data.user == user] = avr_ends_with_punctiation
        # punctuation/mentions/text size/starts with capital/words count/ends with punctuation features section end

        # vocabulary richness feature
        vocabulary = get_ngrams(texts, 1)
        vocabulary_size = len(vocabulary)
        unique_words = sum( x == 1 for x in vocabulary.values() )
        vocabulary_richness = float(unique_words / vocabulary_size) * 100
        data.vocabulary_richness[data.user == user] = vocabulary_richness
        # vocabulary richness feature section ends

        # parts of speech features
        pos_tag_dict = calculate_pos_tag_features(texts)
        for pos_tag in pos_tag_dict:
            try:
                data.ix[data.user == user, pos_tag] = float(pos_tag_dict[pos_tag] / len(texts))
            except:
                print ('Undefined tag: ' + pos_tag)
        # parts of speech features section ends
        print(str(count) + ' ' + str(user) + ' user calculated')

    data.to_csv('Resources/data_text_postag.csv', sep = '\t')
    return


def main():
    os.chdir('../')
    read_data()
    #define_features()

    # FIXME uncomment to get dictionary files!
    calculate_common_ngrams_dict()
    calculate_ngrams_dicts()
    #define_pos_tag_features()
    #calculate_features()
    return

if __name__ == "__main__":
    main()