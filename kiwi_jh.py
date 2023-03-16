import os
import docx2txt
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from keybert import KeyBERT
import numpy as np


kiwi = Kiwi(load_default_dict=True)
kiwi.load_user_dictionary('userDict.txt')

kiwi.prepare()

keyBERT_model = KeyBERT(model='distiluse-base-multilingual-cased-v1')


file_list = os.listdir('./new_folder')

stopwords = ({'개발', '기술', '솔루션', '데이터', '사용자', '사업', '모델', '사용', '개월', '기능', '수집', '분석', '방법', '기반', '개선',
              '제공', '목표', '사용', '시스템', '등', '수', '처리', '평가', '성능', '전략', '인식', '기획', '객체',
              '현실', '증강', '다양', '경험','러닝', '운영', '이용', '계획','관리','배포','고려','검증','테스트','적용','소프트웨어',
              '것','목적','다음','안','활용','업무','기업','비지니스','선정','최종','튜닝','결정','의사','컨텐츠','버스','운행',
              '응용','비용','이미지', '유지','보수','엔지니어'})
def Kiwi_tokenize(file_name):
    doc = ''
    # token = []
    result = ''
    명사 = ('NN')

    doc = docx2txt.process('./new_folder/'+file_name)
    kiwi_tokenize = kiwi.tokenize(doc)

    for i in kiwi_tokenize:
        if i[1].startswith(명사) and i[0] not in stopwords:
            result += i[0] + ' '
            
    
    print(result)
    return result

# def KeyBERT_model(token):
#     result = []

#     keywords = keyBERT_model.extract_keywords(token, keyphrase_ngram_range=(1, 1))

    
#     print(keywords)
#     if keywords:
#         result.append(keywords)
        
#     else:
#         result.append("Null")
        
    
#     return result