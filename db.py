import cx_Oracle
from flask import Flask, session, render_template, redirect, request, url_for

# 
app = Flask(__name__)
app.secret_key = 'qwer1234'

cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\smhrd\Oracle\instantclient_21_9")
con = cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")
cursor = con.cursor()


app.config['db_connection'] = con

# 인서트 문
# data1 = 'test5'
# data2 = 'test5'
# data3 = 'N'
# data4 = 'A'
# cursor.execute("""INSERT INTO c_user(user_mail, user_pw, user_admin, price_type)VALUES(:1, :2, :3, :4)"""
#                ,[data1, data2, data3, data4])
# con.commit()

@app.route('/', methods=['GET', 'POST'])
def main():
    

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
 
        cursor = con.cursor()
 
        cursor.execute("SELECT * FROM c_user WHERE user_mail = (:1) AND user_pw = (:2)",[id,pw])
 
        data = cursor.fetchall()
        cursor.close()
        con.close()
 
        if data:
            session['login_user'] = id
            return redirect(url_for('home2.html'))
        else:
            print('invalid input data detected !')
    return render_template('main.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    

    if request.method == 'POST':
      
        id = request.form['regi_id']
        pw = request.form['regi_pw']
        user_admin = 'N'
        price_type = 'A'
       
        cursor = con.cursor()
 
        
        cursor.execute("INSERT INTO c_user(user_mail, user_pw, user_admin, price_type) VALUES (:1, :2,:3,:4)",[id,pw,user_admin,price_type])
        con.commit()   
 
        cursor.close()
        #con.close()
        return render_template('main.html')
    return render_template('register.html')
 
@app.route('/home2.html', methods=['GET', 'POST'])
def home():
    error = None
    id = session['login_user']
    return render_template('home2.html', error=error, name=id)


if __name__ == '__main__':
    app.run()


 
