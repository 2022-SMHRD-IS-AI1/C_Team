import cx_Oracle
import os
import os.path, time
from tqdm import tqdm

if not cx_Oracle.init_oracle_client:
    cx_Oracle.init_oracle_client(lib_dir=r".\Oracle\instantclient_21_9")

# db 연결
def connect():
    return cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")
    
# 파일 정보 db에 저장
def db_update(user_seq, file_list, file_topic):
    con = connect() # db 연결
    cursor = con.cursor() # cursor 객체(튜플) 생성
    try: 
        # sql문
        for i in tqdm(range(len(file_list))):
            file_path = f'./uploads/{user_seq}/{file_topic[i]}/'
            file_name, file_ext = os.path.splitext(file_list[i])
            sql = "INSERT INTO file_info(user_seq, file_path, file_name, file_ext, file_upload) VALUES(:1, :2, :3, :4, SYSDATE)"
            cursor.execute(sql, [user_seq, file_path, file_name, file_ext]) # sql문 실행
        con.commit() # 커밋
        result = True # result에 성공여부 초기화 (True : 성공)

    except Exception as e: # 예외 처리
        print(e) # 예외 메시지 출력
        result = False # result에 성공여부 초기화 (False : 실패)

    finally: # 예외 여부와 관계없이 실행
        cursor.close() # cursor 객체 닫기
        con.close() # db 연결 닫기

    return result # result(성공여부) 리턴

async def upload(user_id, file_name):

    file_path = f'./uploads/{user_id}/'
    os.makedirs(file_path, exist_ok=True)

    for f in file_name:
        f.save(file_path + f.filename)
    return file_path
    
# file_list = os.listdir('./new_folder')

# for i in range(5):
#    # print('./new_folder/'+file_list[i])
#     name, extention = os.path.splitext(file_list[i])
#     path = os.getcwd()
#     date = time.ctime(os.path.getmtime(path))
#     print('파일명' +name)
#     print('파일경로' +path)
#     print('파일확장자' + extention)
#     print('파일 생성일' + date)


def replace_file(user_seq, file_list, file_topic):
    for i in range(len(file_list)):
        file_path = f'./uploads/{user_seq}/'
        file_destination = f'./uploads/{user_seq}/{file_topic[i]}/'
        os.makedirs(file_destination, exist_ok=True)
        os.replace(file_path+file_list[i], file_destination+file_list[i])
        
def file_list_in_dir(file_path):
    file_list = []
    try:
        list_dir = os.listdir(file_path)
        if list_dir:
            for dir_name in list_dir:
                dir_file_list = os.listdir(file_path+dir_name)
                for file_name in dir_file_list:
                    file_list.append(dir_name+'/'+file_name)
    except Exception as e:
        print(e)
    finally:
        return file_list


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

