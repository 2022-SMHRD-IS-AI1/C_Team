import os
import time
import docx2txt
        # doc_list = docx2txt.process('./new_folder/'+file_list[i])
file_list = os.listdir('./new_folder')
for i in range(5):
        print('./new_folder/'+file_list[i])
        name, extention = os.path.splitext(file_list[i])
        path = os.getcwd()
        date = time.ctime(os.path.getmtime(path))
        print('파일명 : ' + name)
        print('파일경로 : ' + path)
        print('파일확장자 : ' + extention)
        print('파일 생성일 : ' + date)