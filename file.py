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
            file_path = f'./uploads/{user_seq}/{file_topic[i]}/' # 파일 경로
            file_name, file_ext = os.path.splitext(file_list[i]) # 파일 이름, 확장자 분리
            sql = """INSERT INTO file_info(user_seq, file_path, file_name, file_ext, file_upload)
                     VALUES(:1, :2, :3, :4, SYSDATE)"""
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


# 서버에 파일 업로드
def upload(user_id, file_name, nowtime):
    # 저장 경로
    file_path = f'./uploads/{user_id}/{nowtime}/'
    # 폴더 생성(폴더가 있으면 생성하지 않음)
    os.makedirs(file_path, exist_ok=True)
    for f in file_name:
        f.save(file_path + f.filename)
    return file_path
    

# 업로드된 파일 주제별로 폴더에 이동
def replace_file(file_path, file_list, file_topic):
    for i in range(len(file_list)):
        file_destination = f'{file_path}{file_topic[i]}/' # 이동할 경로
        # 폴더 생성(폴더가 있으면 생성하지 않음)
        os.makedirs(file_destination, exist_ok=True) 
        # 지정된 경로로 파일 이동
        os.replace(file_path+file_list[i], file_destination+file_list[i]) 
        


# 모든 하위 폴더의 파일 리스트
def file_list_in_dir(file_path):
    file_list = []
    try:
        time_dir_list = os.listdir(file_path) # 사용자별 폴더 리스트 저장
        if time_dir_list:
            for time_dir in time_dir_list:
                file_dir_list = os.listdir(file_path+time_dir) # 분류명 폴더 리스트 저장
                for file_dir in file_dir_list:
                    file_name_list = os.listdir(file_path+time_dir+'/'+file_dir) # 파일명 리스트 저장
                    for file_name in file_name_list:
                        file_list.append(file_path+time_dir+'/'+file_dir+'/'+file_name) # 파일 리스트에 추가
    except Exception as e:
        print(e)
    finally:
        return file_list # 파일 리스트 반환

# 파일 크기 단위 변경
def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024))) # 단위 계산
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i]) # 크기 단위 변경후 반환

