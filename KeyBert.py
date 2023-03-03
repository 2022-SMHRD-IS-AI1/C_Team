import pandas as pd

# 데이터 전처리

df_train = pd.read_csv('./data/ratings_train.csv')
df_test = pd.read_csv('./data/ratings_test.csv')
print(df_train.head())

df_train.info()

df_train.dropna(inplace=True)
df_train.info()

df_test.dropna(inplace=True)
df_test.info()


# document -> 문제, label -> 답
# 훈련용 문제, 답
text_train = df_train['document'] # df_train.iloc[:,1]
y_train =  df_train['label']
# 테스트용 문제, 답
text_test = df_test['document']
y_test = df_test['label']

# 크기 확인
print('훈련용:', text_train.shape, y_train.shape)
print('테스트용:', text_test.shape, y_test.shape)


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

print(text_train[:3])


# 1. CountVectorizer 적용해보기
# 객체 생성
cnt_vect = CountVectorizer()
# 단어사전 구축(가방, 모음집)
cnt_vect.fit(text_train[:3])
# 분리된 문장으로 만든 단어 사전 출력
print(len(cnt_vect.vocabulary_.keys()))
print(cnt_vect.vocabulary_.keys())

# 문장 -> 토큰화 & 수치화
# 단어의 빈도수를 수치값으로 입력
cnt_vect.transform(text_train[:3]).toarray()


# 2. TfidfVectorizer
# 객체 생성
tf_idf_vect = TfidfVectorizer()
# 단어사전 구축 fit
tf_idf_vect.fit(text_train[:3])
# 분리된 문장으로 만든 단어 사전 출력
print(tf_idf_vect.vocabulary_.keys())
# 문장 -> 토큰화 & 수치화
# 단어의 빈도수 뿐만아니라 문장 내의 중요도 가치를 부여한 수치
tf_idf_vect.transform(text_train[:3]).toarray()


from kiwipiepy import Kiwi
kiwi = Kiwi()
#kiwi.load_user_dictionary('user_dictionary.txt')
kiwi.prepare()







#import konlpy
#konlpy.jvm.init_jvm(jvmpath=None, max_heap_size=8192)

from konlpy.tag import Kkma



# 객체 생성
kkma = Kkma()


# 문장 1개 테스트해보기
print(text_train[0])


# 명사 추출
print(kkma.nouns(text_train[0]))


# # tf-idf와 kkma.nouns() 한국어 명사 추출 연결하기
# def myTokenizer(text):
#   return kkma.nouns(text)


# # tf-idf 연결
# tmp_tfidf_vect = TfidfVectorizer(tokenizer = myTokenizer)
# tmp_tfidf_vect.fit(text_train[:3]) # 단어사전 만들기
# # 어휘 확인
# print(tmp_tfidf_vect.vocabulary_)


# 3개 문장만 적용해보기
def myTokenizer2(text):
  d = pd.DataFrame(kkma.pos(text), columns = ['morph', 'tag'])
  d.set_index('tag', inplace = True)
  # |: 또는 shift + \
  if ('VV' in d.index) | ('VA' in d.index) | ('NNG' in d.index):
    # vv,va,vvg 품사 형태소의 밸류값만 반환
    return d.loc[d.index.intersection(['VV','VA','NNG']),'morph'].values
  else:
    return []


# tf-idf 연결
tmp_tf_idf_vect = TfidfVectorizer(tokenizer = myTokenizer2)
# 단어 구축
tmp_tf_idf_vect.fit(text_train[:3])
# 단어 사전
print(tmp_tf_idf_vect.vocabulary_)


# 최종 vect 생성
final_vect = TfidfVectorizer(tokenizer = myTokenizer2)
# 10000개 문장 데이터 연결해서 단어 모음 fit
final_vect.fit(text_train[:10000])


X_train = final_vect.transform(text_train[:10000])
X_test = final_vect.transform(text_test[:10000])


# def BERT(title):

#     array_text = pd.DataFrame(df[df['title'] == title]['text']).to_numpy()

#     bow = []
#     from keybert import KeyBERT
#     kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
#     for j in range(len(array_text)):
#         keywords = kw_extractor.extract_keywords(array_text[j][0])
#         bow.append(keywords)
    
#     new_bow = []
#     for i in range(0, len(bow)):
#         for j in range(len(bow[i])):
#             new_bow.append(bow[i][j])
            
#     keyword = pd.DataFrame(new_bow, columns=['keyword', 'weight'])
#     print(keyword.groupby('keyword').agg('sum').sort_values('weight', ascending=False).head(20))
