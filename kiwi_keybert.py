import os
import docx2txt
from kiwipiepy import Kiwi
from keybert import KeyBERT
import numpy as np
#from flair.embeddings import TransformerDocumentEmbeddings
#from sentence_transformers import SentenceTransformer

kiwi = Kiwi(load_default_dict=True)
kiwi.load_user_dictionary('userDict.txt')
kiwi.prepare()

keyBERT_model = KeyBERT(model='distiluse-base-multilingual-cased-v1')
# roberta = TransformerDocumentEmbeddings('roberta-base')
# kw_model = KeyBERT(model=roberta)

# sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
# kw_model = KeyBERT(model=sentence_model)

file_list = os.listdir('./new_folder')

def Kiwi_tokenize(file_name):
    doc = ''
    token = []

    #형용사 = ('VA')
    #용언품사 = ('VV', 'VA')
    명사 = ('N')

    doc = docx2txt.process('./new_folder/'+file_name)
    kiwi_tokenize = kiwi.tokenize(doc)

    for i in kiwi_tokenize:
        if i[1].startswith(명사):
            token.append(i[0])
            
    return token

def KeyBERT_model(token):
    result = []

    keywords = keyBERT_model.extract_keywords(token, highlight=True, keyphrase_ngram_range=(1, 3), stop_words=None)

    if keywords:
        result.append(keywords[0][0])
        # print(keywords[0][0])
    else:
        result.append("Null")
        # print("Null")

    # print(keywords[0][0])

    print(result)
    return result
