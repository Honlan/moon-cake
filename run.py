# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from flask import *
import MySQLdb
import MySQLdb.cursors
import warnings
warnings.filterwarnings("ignore")
from config import *
import random
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "1DA2DG3HYK9KU1T6WRSFSF2GCSG6GSDSYL9UL1Q2S3X4A1"

def connectdb():
	db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = MySQLdb.cursors.DictCursor)
	db.autocommit(True)
	cursor = db.cursor()
	return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
	db.close()
	cursor.close()

@app.route('/',methods=['GET'])
def index():
	cake = None
	user = None
	if not session.get('username') == None:
		username = session.get('username')
		(db,cursor) = connectdb()
		cursor.execute('select * from user where name=%s',[username])
		user = cursor.fetchone()
		cursor.execute('select * from moonCake where id=%s',[user['moonCakeId']])
		cake = cursor.fetchone()
		closedb(db,cursor)
	return render_template('index.html',user=user,cake=cake)

@app.route('/add',methods=['POST'])
def add():
	data = request.form
	username = data['username']
	(db,cursor) = connectdb()
	if cursor.execute('select * from user where name=%s',[username]) > 0:
		user = cursor.fetchone()
		cursor.execute('select * from moonCake where id=%s',[user['moonCakeId']])
		cake = cursor.fetchone()
		closedb(db,cursor)
		session['username'] = username 
		return json.dumps({"name": username, "cake": cake})
	else:
		moonCakeId = random.randint(1, 27)
		cursor.execute('insert into user(name,moonCakeId,timestamp) values(%s,%s,%s)',[username,moonCakeId,str(int(time.time()))])
		cursor.execute('select * from moonCake where id=%s',[moonCakeId])
		cake = cursor.fetchone()
		closedb(db,cursor)
		session['username'] = username 
		return json.dumps({"name": username, "cake": cake})

if __name__ == '__main__':
	app.run(debug=True)