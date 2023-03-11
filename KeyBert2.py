import os
import docx2txt
from kiwipiepy import Kiwi
from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings
from sentence_transformers import SentenceTransformer


# from collections import Counter

file_list = os.listdir('./new_folder')
doc = ""


kiwi = Kiwi(load_default_dict=True)
kiwi.load_user_dictionary('userDict.txt')
kiwi.prepare()
# kiwi_analyze = kiwi.analyze(doc)

kw_model = KeyBERT(model='distiluse-base-multilingual-cased-v1')

# roberta = TransformerDocumentEmbeddings('roberta-base')
# kw_model = KeyBERT(model=roberta)

# sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
# kw_model = KeyBERT(model=sentence_model)


result = []


for i in range(500):
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

    # print(token)

    keywords = kw_model.extract_keywords(token, highlight=True, keyphrase_ngram_range=(1, 2), stop_words=None)

    
    if keywords:
        result.append(keywords[0][0])
        # print(keywords[0][0])
    else:
        result.append("Null")
        # print("Null")
    
    # print(keywords[0][0])

print(result)