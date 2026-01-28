from flask import Blueprint,render_template,request,g,redirect,url_for
from .forms import QuestionForm
from models import QuestionModel
from exts import db
from models import UserModel


# 创建问答蓝图实例，设置蓝图名称为"qa"，URL前缀为"/"
bp = Blueprint("qa",__name__,url_prefix="/")

# 定义根路径路由，处理首页访问请求
# 在 qa.py 文件中修改 index 函数
@bp.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页10个帖子
    questions_pagination = QuestionModel.query.order_by(QuestionModel.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    questions = questions_pagination.items
    return render_template("index.html", questions=questions, pagination=questions_pagination)



@bp.route("/qa/public_cgw",methods=['GET','POST'])
def public_question():
    if request.method == 'GET':
        # GET请求返回注册页面模板
        return render_template("public_question.html")
    else:
        # POST请求处理注册表单提交
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            # 注册成功后重定向到首页页面
            return redirect("/")
        else:
            # 如果表单验证失败，打印错误信息并重定向回问答界面
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/top_list")
def top_list():
    # 获取热门问题（按浏览量排序）
    questions = QuestionModel.query.order_by(
        QuestionModel.view_count.desc()
    ).limit(10).all()  # 限制为10条

    # 获取热门创作者（按积分排序）
    creators = UserModel.query.order_by(
        UserModel.points.desc()
    ).limit(10).all()  # 限制为10条

    return render_template("top_list.html", questions=questions, creators=creators)

