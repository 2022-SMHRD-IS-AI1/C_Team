import os
import re
from pprint import pprint

import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
import docx2txt
import kiwi_keybert as KK

# 폴더 내 문서 경로 설정
doc_folder_path = './new_folder'
doc_list = os.listdir(doc_folder_path)

# 텍스트 전처리 함수
def preprocess(text):
    # 소문자 변환
    text = text.lower()
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    # 숫자 제거
    text = re.sub(r'\d+', '', text)
    # 불용어 제거
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    return text

# 전처리된 문서를 저장할 리스트
processed_docs = []

# 폴더 내 모든 문서에 대해 전처리 수행
for doc in doc_list:
    # 문서 파일 열기
    # with open(os.path.join(doc_folder_path, doc), 'r', encoding='utf-8') as f:
    #     # 문서 파일 읽기
    #     text = f.read()
    #     # 전처리 수행
    #     processed_doc = preprocess(text)
    #     # 전처리된 문서 리스트에 추가
    #     processed_docs.append(processed_doc)

    # text = docx2txt.process('./new_folder/'+doc)
    # 전처리 수행
    # processed_doc = preprocess(text)
    processed_doc = KK.Kiwi_tokenize(doc)
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
                     alpha='auto')

# 각 문서별로 주제 분포 추정
doc_topic_dists = lda_model[corpus]

# 추정된 주제 별로 가장 높은 비중의 단어 10개씩 출력
pprint(lda_model.show_topics(num_topics=10, num_words=3, formatted=False))

for i, topic_list in enumerate(lda_model[corpus]):
    if i==100:
        break
    print(i,'번째 문서의 topic 비율은',topic_list)