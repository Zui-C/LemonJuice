# 配置项大写
JSON_AS_ASCII = False
SECRET_KEY = ''
# 数据库的配置变量
HOSTNAME = ''
PORT     = ''
DATABASE = ''
USERNAME = ''
PASSWORD = ''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True


