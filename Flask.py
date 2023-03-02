from flask import Flask
import Connection
app = Flask(__name__)

@app.route("/")
def connection():
    id = input()
    pw = input()
    Connection.connect(id, pw)
    return 

if __name__ == "__main__":
    app.run()





