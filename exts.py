from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# 初始化数据库扩展实例
db = SQLAlchemy()

# 初始化邮件扩展实例
mail = Mail()

