import os
import re
from tqdm import tqdm
from gensim import corpora
from gensim.models import LdaModel
import kiwi2
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import numpy as np


# 텍스트 전처리 함수
def preprocess(text):
    # 소문자 변환
    text = text.lower()
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    return text

async def classification(file_path):
    # 폴더 내 문서 경로 설정
    doc_folder_path = file_path
    doc_list = os.listdir(doc_folder_path)

    # 전처리된 문서를 저장할 리스트
    processed_docs = []

    # 폴더 내 모든 문서에 대해 전처리 수행
    for doc in tqdm(doc_list):
        # Kiwi에서 문서별 토큰 가져오기
        token = kiwi2.tokenize(doc, file_path)
        # 전처리 수행
        processed_doc = preprocess(token)
        # 전처리된 문서 리스트에 추가
        processed_docs.append(processed_doc)

    # 문서를 단어별로 분리하여 단어장 생성
    dictionary = corpora.Dictionary([doc.split() for doc in tqdm(processed_docs)])

    # 문서-단어 행렬 생성
    corpus = [dictionary.doc2bow(doc.split()) for doc in tqdm(processed_docs)]

    # LDA 모델 생성
    lda_model = LdaModel(corpus=corpus,
                        id2word=dictionary,
                        random_state=5,
                        num_topics=10, # 주제 개수 설정
                        passes=20, # 알고리즘 반복 횟수 설정
                        alpha='auto',
                        eta='auto',
                        iterations=400,
                        eval_every=None)

    # 각 주제명 가져오기
    topic_name = []
    for topics in lda_model.show_topics(num_topics=10, num_words=1, formatted=False):
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

    # 파일별 주제 이름 변경하기
    for i in range(len(topic_name)):
      file_topic = [topic_name[i] if x == i else x for x in file_topic]

    # 결과 시각화
    lda_visualization = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(lda_visualization, 'file_name.html')

    return file_topic
