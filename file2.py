import cx_Oracle
import os
import os.path, time

if not cx_Oracle.init_oracle_client:
    cx_Oracle.init_oracle_client(lib_dir=r".\Oracle\instantclient_21_9")

# db 연결
def connect():
    return cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")
    
# 파일 정보 db에 저장
def db_update(user_id, file_path, file_name, file_ext):
    con = connect() # db 연결
    cursor = con.cursor() # cursor 객체(튜플) 생성
    try: 
        # sql문
        sql = "SELECT user_seq FROM c_user WHERE user_mail = :1"
        user_seq = cursor.execute(sql, [user_id]) # sql문 실행
        sql = "INSERT INTO file_info(user_seq, file_path, file_name, file_ext, file_upload) VALUES(:1, :2, :3, :4, 'SYSDATE')"
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

def upload(user_id, file_name):
   
    os.makedirs(f'./uploads/{user_id}', exist_ok=True)

    for f in file_name:
        f.save(f'./uploads/{user_id}/' + f.filename)
    


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


