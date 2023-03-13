import os
import docx2txt
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from keybert import KeyBERT
import numpy as np
#from flair.embeddings import TransformerDocumentEmbeddings
#from sentence_transformers import SentenceTransformer

kiwi = Kiwi(load_default_dict=True)
kiwi.load_user_dictionary('userDict.txt')
# stopwords = ['개발', '연구', '향상', '전략', '과정', '문제', '정의', '배포', '지원', '결과',
#                '솔루션', '테스트', '시장', '진출', '높이기', '반영', '감시', '목적', '대상', '기능', '기술', '단계',
#                  '방법', '활용', '환경', '사용', '라이브러리', '사용자', '이해', '적용', '성과', '개선', '개월', '계획',
#                    '고려', '가치', '수립', '목표', '포함', '결정', '참가자', '여부', '내용', '시간', '배경', '제공',
#                      '이용', '준지', '진행', '도모', '발전', '상품', '정보', '기반', '사업', '처리', '입니다', '합니다',
#                        '같습니다', '것입니다', '있습니다', '돕는다', '됩니다', '시킵니다', '다음과', '다음은', '이상', '본', '모든', '빠른',
#                         '빠르고', '정확한', '위함', '은', '는', '이', '가', '을', '를', '하여', '하기', '및', '에서', '과', '와', '의',
#                          '위한', '으로', '이고', '시키기', '시키고', '것', '위해', '있는', '등', '통해', '통하여', '통해서',
#                           '하는', '한', '있도록', '더', '에서', '보다', '이를', '같은', '다른', '느끼는', '할 수', '쉽게',
#                            '원하는', '새로운', '하고', '시키는', '각각의', '하며', '또한', '거쳐', '등의', '된', '하거나', '가장',
#                             '최적의', '기반으로', '테스트', '다양한', '이런', '이러한', '에서', '나는', '해서', '따라', '따라서', '에',
#                              '하게', '보다', '이용한', '만들고', '사용한', '활용한', '1.', '2.', '3.', '4.', '5.', '6.',
#                               '7.', '8.', '9.', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)', ' (7)', '(8)', '(9)', '주요',
#                                '중요한', '매우', '것이', '있고', '하도록', '이루기', '로', '여러', '되며', '-', '.', ',',
#                                 '따른', '두고', '담고', '있도록', '모으고', '모아', '담아', '두고', '의도한', '해당', '형식', '경우',
#                                  '추가']
# stopwords = Stopwords(filename='stopwords.txt')
# for i in stop_words:
#     stopwords.add(i)
# stopwords.save('stopwords.txt')
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
            
    unique, counts = np.unique(token, return_counts=True)
    uniq_cnt_dict = dict(zip(unique, counts))
    token = sorted(uniq_cnt_dict.items(), 
       reverse = True, 
       key = lambda x: x[1])
    # print(token)
    return token

def KeyBERT_model(token):
    result = []

    keywords = keyBERT_model.extract_keywords(token, keyphrase_ngram_range=(1, 1))

    # keywords = np.argmax(keywords)
    print(keywords)
    if keywords:
        result.append(keywords)
        # print(keywords[0][0])
    else:
        result.append("Null")
        # print("Null")

    # print(keywords[0][0])

    # print(result)
    return result
