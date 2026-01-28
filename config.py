# 应用密钥，用于会话加密和其他安全相关功能
SECRET_KEY = "13053979852@Cgw" #（！！！改为自己的！！！）

# 数据库配置参数
HOSTNAME = '127.0.0.1'  # 数据库主机地址
PORT = '3306'           # 数据库端口号
DATABASE = 'webnew'     # 数据库名称
USERNAME = 'root'       # 数据库用户名
PASSWORD = '123456'       # 数据库密码（！！！改为自己的！！！）

# 构建数据库连接URI
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# Flask-SQLAlchemy使用的数据库URI配置
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮件服务器配置
MAIL_SERVER = "smtp.qq.com"                 # SMTP服务器地址，默认使用qq邮箱
MAIL_USE_SSL = True                         # 启用SSL加密连接
MAIL_PORT = 465                             # SMTP服务器端口，默认465

MAIL_USERNAME = "759668916@qq.com"         # 发送邮件的邮箱账号（！！！改为自己的！！！）
MAIL_PASSWORD = "psqylvbkcgcbbfgd"          # 邮箱授权码（非登录密码）（！！！改为自己的！！！）
MAIL_DEFAULT_SENDER = "759668916@qq.com"   # 默认发件人（！！！改为自己的！！！）
