import ftplib
session = ftplib.FTP()
session.connect('localhost', 9021) # 두 번째 인자는 port number
session.login("admin", "admin1234")   # FTP 서버에 접속
 
uploadfile = open('C:/Users/smhrd/Downloads/sql.txt' ,mode='rb') #업로드할 파일 open
 
session.encoding='utf-8'
session.storbinary('./uploads/sql.txt', uploadfile) #파일 업로드
 
uploadfile.close() # 파일 닫기
 
session.quit() # 서버 나가기
print('파일전송함')