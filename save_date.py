import os
import cx_Oracle
from datetime import datetime


def save_date_to_db(file_path):  
    # 파일 생성일 확인
    created_time = os.path.getctime(file_path)
    # 파일 생성일 형식 저장
    created_time = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')

    # Oracle 데이터베이스에 저장
    with cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8") as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO file_info(file_date) VALUES (:created_time)", {'created_time': created_time})
        conn.commit()