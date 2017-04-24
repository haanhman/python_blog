from pymysql.cursors import DictCursor

from config import app
from flaskext.mysql import MySQL
mysql = MySQL()

#MySQL Config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123123'
app.config['MYSQL_DATABASE_DB'] = 'python_blog'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8'
mysql.init_app(app)

db = mysql.connect().cursor(DictCursor)