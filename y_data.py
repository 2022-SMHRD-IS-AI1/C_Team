import os

# 답데이터 만들기

def y_data(file_list):
    for i in range(len(file_list)):
        result = file_list[i].split(" ")
        print(result[0])
    return result


file_list = os.listdir('./new_folder')

y_data(file_list)