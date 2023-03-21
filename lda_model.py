import os
import re
from pprint import pprint
from tqdm import tqdm

from gensim import corpora
from gensim.models import LdaModel
import kiwi

import pyLDAvis.gensim as gensimvis
import pyLDAvis
import numpy as np


# 텍스트 전처리 함수
def preprocess(text):
    # 소문자 변환
    text = text.lower()
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    # 불용어 제거
    text = ' '.join([word for word in text.split()])

    return text


def classification(file_path):
    # 폴더 내 문서 경로 설정
    doc_folder_path = file_path
    doc_list = os.listdir(doc_folder_path)

    # 전처리된 문서를 저장할 리스트
    processed_docs = []

    # 폴더 내 모든 문서에 대해 전처리 수행
    for doc in tqdm(doc_list):
        # Kiwi에서 문서별 토큰 가져오기
        token = kiwi.tokenize(doc, file_path)
        # 전처리 수행
        processed_doc = preprocess(token)
        # 전처리된 문서 리스트에 추가
        processed_docs.append(processed_doc)

    # 문서를 단어별로 분리하여 단어장 생성
    dictionary = corpora.Dictionary([doc.split() for doc in tqdm(processed_docs)])

    # 문서-단어 행렬 생성
    corpus = [dictionary.doc2bow(doc.split()) for doc in tqdm(processed_docs)]

    num_topics = 10
    # LDA 모델 생성
    lda_model = LdaModel(corpus=corpus,
                        id2word=dictionary,
                        random_state=2,
                        num_topics=num_topics, # 주제 개수 설정
                        passes=20, # 알고리즘 반복 횟수 설정
                        alpha=0.001,
                        eta=0.001,
                        iterations=200,
                        eval_every=None)

    # 각 문서별로 주제 분포 추정
    # doc_topic_dists = lda_model[corpus]

    # 추정된 주제 별로 가장 높은 비중의 단어 10개씩 출력
    # pprint(lda_model.show_topics(num_topics=10, num_words=5, formatted=False))

    # for i, topic_list in enumerate(lda_model[corpus]):
    #     if i==50:
    #         break
    #     print(doc_list[i],'문서의 topic 비율은',topic_list)

    # 각 주제명 가져오기
    topic_name = []
    for topics in lda_model.show_topics(num_topics=num_topics, num_words=1, formatted=False):
        topic_name.append(topics[1][0][0])

    # 파일별 주제명 가져오기
    file_topic = []
    for a in lda_model[corpus]:
        main_topic = []
        topic_per = []
        for b in a:
          main_topic.append(b[0])
          topic_per.append(b[1])
        file_topic.append(main_topic[np.argmax(topic_per)])
          
    # for i in file_topic:
    #   print(i)
    print(topic_name)
    print(file_topic)

    # 파일별 주제 이름 변경하기
    for i in range(len(topic_name)):
      file_topic = [topic_name[i] if x == i else x for x in file_topic]
    print(file_topic)

    # 결과 시각화
    lda_visualization = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(lda_visualization, 'file_name.html')

    return file_topic



# classification('admin')