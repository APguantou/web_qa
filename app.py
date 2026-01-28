# 导入Flask核心组件和全局对象
from flask import Flask,session,g
# 导入应用配置
import config
# 导入数据库和邮件扩展实例
from exts import db,mail
# 导入数据库迁移工具
from flask_migrate import Migrate
# 导入用户模型
from models import UserModel
# 导入问答蓝图和认证蓝图
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

# 创建Flask应用实例
app = Flask(__name__)
# 从配置对象加载应用配置
app.config.from_object(config)

# ------------初始化----------------
# 初始化数据库扩展
db.init_app(app)
# 初始化邮件扩展
mail.init_app(app)
# 初始化数据库迁移工具
migrate = Migrate(app,db)

# ------------蓝图注册---------------
# 注册问答功能蓝图
app.register_blueprint(qa_bp)
# 注册认证功能蓝图
app.register_blueprint(auth_bp)


# ------------请求处理---------------
# 请求预处理装饰器：在每个请求前执行用户身份检查
@app.before_request
def my_before_request():
    # 从会话中获取用户ID
    user_id = session.get("user_id")
    if user_id:
        # 如果存在用户ID，则查询用户对象并存储到g对象中
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        # 如果不存在用户ID，则将g.user设为None
        setattr(g,"user",None)


# 上下文处理器：向所有模板注入当前用户信息
@app.context_processor
def my_context_processor():
    # 返回包含当前用户的字典，供模板使用
    return {"user":g.user}


# 应用入口点
if __name__ == '__main__':
    # 启动开发服务器
    app.run()
