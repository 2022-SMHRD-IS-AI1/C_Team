# from kiwipiepy import Kiwi
# kiwi = Kiwi()
# #kiwi.load_user_dictionary('user_dictionary.txt')
# kiwi.prepare()

# result = kiwi.tokenize('테스트입니다.')
# for token in result:
#     print(f"{token.form}\t{token.tag}")

# import pandas as pd
# #df = pd.read_excel('rawdata.xlsx')
# df = pd.read_csv('./data/ratings_test.csv')
# morph_analysis = lambda x: kiwi.tokenize(x) if type(x) is str else None
# df['형태소분석결과'] = df['document'].apply(morph_analysis)

# print(df['형태소분석결과'].head())


# from collections import Counter
# '''주요 품사, 용언 품사 정의'''
# 주요품사 = ['NNG', 'NNP', 'VV', 'VA', 'XR', 'SL']
# 용언품사 = ['VV', 'VA']
# '''Counter를 활용해 가장 많이 나온 n개의 품사 결과를 돌려주는 pos_count() 함수'''
# def pos_count(df, col, output_filename, n=100):
#     카운터 = Counter()
    
#     for index, row in df.iterrows(): 
#         if row[col]:
#             필터링결과 = [(token.form, token.tag) for token in row[col] if token.tag in 주요품사]
#             카운터.update(필터링결과)
            
#     with open(output_filename, "w", encoding='utf-8-sig') as output_file:
#         print("형태소,품사,개수", file=output_file)
#         for (형태소, 품사), 개수 in 카운터.most_common(n):
#             if 품사 in 용언품사:
#                 형태소 += "다"
#             print(f"{형태소},{품사},{개수}", file=output_file)

# pos_count(df, '형태소분석결과', './data/주요어휘빈도.csv')

import os
import docx2txt
from keybert import KeyBERT


file_list = os.listdir('./new_folder')
text = docx2txt.process('./new_folder/'+file_list[0])

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(3, 3), stop_words=None,
                                     use_maxsum=True, nr_candidates=20, top_n=5)
print(keywords)
