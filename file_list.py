import os
import docx2txt
from kiwipiepy import Kiwi
import numpy as np
from keybert import KeyBERT
kw_model = KeyBERT(model='Paraphrase-Multilingual-MiniLM-L12-v2')
file_list = os.listdir('./C_team/new_folder')

# print(file_list)
kiwi = Kiwi(load_default_dict=True)
kiwi.add_user_word("3D", "NNG")
kiwi.add_user_word("AR", "NNG")
#kiwi.load_user_dictionary('user_dictionary.txt')
kiwi.prepare()


topic_list = []

for i in range(200):
    text = docx2txt.process('./C_team/new_folder/'+file_list[i])
    # print(text)
    # 용언품사 = ['VV', 'VA']
    
    result = kiwi.analyze(text)
    # result = kiwi.tokenize(text, split_sents=True)

    cont = ''
    for token, pos, _, _ in result[0][0]:
        if pos.startswith('NN'):
            cont += token +' '

    # KeyBert 활용하여 keyword추출
    #stop_words=None 불용어 제거 하는 기준 None ex) stop_words=['3d']
   
    keywords = kw_model.extract_keywords(cont, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=10)
    #np_keywords = np.array(keywords)
    # print(keywords[0][0])
    #print(np_keywords[0])
    if keywords:
        topic_list.append(keywords[0][0])

print(file_list[:200])
print(topic_list)