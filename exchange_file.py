import os
import docx2txt
from kiwipiepy import Kiwi

file_list = os.listdir('./C_team/new_folder')

kiwi = Kiwi(load_default_dict=True)

kiwi.prepare()

text = docx2txt.process('./C_team/new_folder/'+file_list[0])

kiwi.add_user_word("3D", "NNG")
result = kiwi.analyze(text)

for token, pos, _, _ in result[0][0]:
    if pos.startswith('NN'):
        print(token)