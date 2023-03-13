import kiwi_keybert as KK
import os
# from gensim.models.word2vec import Word2Vec

# model = Word2Vec()
# model.init_sims(replace=True)

# wv_result = model.wv.most_similar('3D')

# print(wv_result)

# KeyBERT_model(Kiwi_model(0,1))

file_list = os.listdir('./new_folder')

for i in range(10):
    token = KK.Kiwi_tokenize(file_list[i])
    result = KK.KeyBERT_model(token)