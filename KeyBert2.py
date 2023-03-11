import os
import docx2txt
from kiwipiepy import Kiwi
from keybert import KeyBERT

file_list = os.listdir('./new_folder')
doc = ""


kiwi = Kiwi(load_default_dict=True)
kiwi.load_user_dictionary('userDict.txt')
kiwi.prepare()
# kiwi_analyze = kiwi.analyze(doc)

kw_model = KeyBERT(model='paraphrase-MiniLM-L3-v2')


for i in range(200):
    doc = docx2txt.process('./new_folder/'+file_list[i])
    kiwi_tokenize = kiwi.tokenize(doc)

    # print("analyze : ",len(kiwi_analyze))
    token = ''
    형용사 = ('VA')
    용언품사 = ('VV', 'VA')
    명사 = ('N')
    for i in kiwi_tokenize:
        if i[1].startswith(명사):
            token += (i[0] + '\t')

    print(token)
        

    # keywords = kw_model.extract_keywords(token, keyphrase_ngram_range=(1, 3), stop_words=None, use_mmr=True, diversity=0.7)

    # print(keywords)


# from bertopic import BERTopic
# from sklearn.datasets import fetch_20newsgroups
 
# #docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']

# topic_model = BERTopic()
# topics, probs = topic_model.fit_transform(doc)

# topic_model.get_topic(0)