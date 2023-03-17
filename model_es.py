import os
import re
from pprint import pprint

import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
import docx2txt
import kiwi_jh as KK
import numpy as np

# 폴더 내 문서 경로 설정
doc_folder_path = './new_folder'
doc_list = os.listdir(doc_folder_path)

# stopwords = ({'개발', '연구', '향상', '전략', '과정', '문제', '정의', '배포', '지원', '결과',
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
#                                  '추가', '데이터', '모델', '분석', '수', '시스템', '기획'})
# 텍스트 전처리 함수
def preprocess(text):
    # 소문자 변환
    text = text.lower()
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    # 숫자 제거
    # text = re.sub(r'\d+', '', text)
    # 불용어 제거
    text = ' '.join([word for word in text.split()])

    return text

# 전처리된 문서를 저장할 리스트
processed_docs = []

# 폴더 내 모든 문서에 대해 전처리 수행
for doc in doc_list:
    # 토큰 가져오기
    token = KK.Kiwi_tokenize(doc)
    processed_doc = preprocess(token)
    # 전처리된 문서 리스트에 추가
    processed_docs.append(processed_doc)

# 문서를 단어별로 분리하여 단어장 생성
dictionary = corpora.Dictionary([doc.split() for doc in processed_docs])

# 문서-단어 행렬 생성
corpus = [dictionary.doc2bow(doc.split()) for doc in processed_docs]

# LDA 모델 생성
lda_model = LdaModel(corpus=corpus,
                     id2word=dictionary,
                     num_topics=10, # 주제 개수 설정
                     passes=20, # 알고리즘 반복 횟수 설정
                     alpha='auto',
                     eta="auto",
                     iterations=400,
                     eval_every=None)

# LDA 모델 생성
# lda_model = LdaModel(corpus=corpus,
#                      id2word=dictionary,
#                      num_topics=10, # 주제 개수 설정
#                      passes=20, # 알고리즘 반복 횟수 설정
#                      alpha='symmetric')

# 각 문서별로 주제 분포 추정
doc_topic_dists = lda_model[corpus]

# doc_topic_dists = [doc for doc in lda_model[corpus]]


# pprint(lda_model.show_topics(num_topics=10, num_words=1, formatted=False))
top10 = lda_model.show_topics(num_topics=10, num_words=1, formatted=False)
print(top10)
name_list = []
name_list2 = []
for i in range(10):
    name_list.append(top10[i])
    name_list.append(top10[i][1][0][0])
    
    
print(name_list)

for i, topic_list in enumerate(lda_model[corpus]):
    if i==50:
        break
    
    topic_per = [topic[1] for topic in topic_list]
    topic_name = [topic[0] for topic in topic_list]
    
    for i in topic_name:
        name_list2.append(name_list[i])
    
    print('문서의 topic 비율은', name_list2, topic_per)
    print(doc_list[i], '문서의 topic 비율은', max(topic_per))
    name_list2 = []
# topic = []

# for i, topic_list in enumerate(lda_model[corpus]):
#     if i==100:
#         break
#     print(doc_list[i],'문서의 topic 비율은',topic_list)
#     for i in topic_list:
#         topic.append(i[1])
#     print(max(topic))
#     topic = []

    



# 추정된 주제 별로 가장 높은 비중의 단어 10개씩 출력
# pprint(lda_model.show_topics(num_topics=10, num_words=1, formatted=False))
# topic = lda_model.show_topics(num_topics=10, num_words=1, formatted=False)
# ouput = topic[]
# topic = lda_model.show_topics(num_topics=10, num_words=1, formatted=False)

# doc_topic_dists = [sorted(lda_model[doc], key=lambda x: -x[1])[0][0][] for doc in corpus]
# topic_names = [lda_model.show_topic(topic_id)[0][0] for topic_id in doc_topic_dists]
# for i, topic in enumerate(lda_model[corpus]):
#     print(doc_list[i],'문서의 topic 비율은',topic)





import pyLDAvis.gensim as gensimvis
import pyLDAvis

lda_visualization = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)
pyLDAvis.save_html(lda_visualization, 'file_name.html')

# topic = lda_model.show_topics(num_topics=10, num_words=1, formatted=False)

# for i in range(10):
#     name = topic[i][1][0][0]
#     output=topic[i][1][0][1]
#     print(name, output)
