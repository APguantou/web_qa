from .forms import QuestionForm
from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from models import QuestionModel
from exts import db
from models import UserModel
from models import QuestionCommentModel


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


#添加JS-index路由
@bp.route("JS_index_cgw")
def JS_index():
    return render_template("JS_index.html")

def check_user_liked(user_id, question_id):
    # 实现检查用户是否已点赞的逻辑
    from models import QuestionLikeModel
    like_record = QuestionLikeModel.query.filter_by(
        user_id=user_id,
        ques_id=question_id
    ).first()
    return bool(like_record)

def check_user_favorited(user_id, question_id):
    # 实现检查用户是否已收藏的逻辑
    from models import QuestionFavoriteModel
    favorite_record = QuestionFavoriteModel.query.filter_by(
        user_id=user_id,
        ques_id=question_id
    ).first()
    return bool(favorite_record)


# 添加question_detail路由
@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    # 查询问题详情
    question = QuestionModel.query.get_or_404(question_id)

    # 增加浏览量
    question.view_count += 1
    db.session.commit()

    # 获取当前用户ID
    current_user_id = g.user.id if hasattr(g, 'user') and g.user else None

    # 查询当前用户是否点赞该问答
    user_is_like = False
    if current_user_id:
        from models import QuestionLikeModel
        like_record = QuestionLikeModel.query.filter_by(
            user_id=current_user_id,
            ques_id=question_id
        ).first()
        user_is_like = bool(like_record)

    # 查询当前用户是否收藏该问答
    user_is_favorite = False
    if current_user_id:
        from models import QuestionFavoriteModel
        favorite_record = QuestionFavoriteModel.query.filter_by(
            user_id=current_user_id,
            ques_id=question_id
        ).first()
        user_is_favorite = bool(favorite_record)

    # 查询当前问答的所有评论
    from models import QuestionCommentModel
    comments = QuestionCommentModel.query.filter_by(ques_id=question_id).all()

    return render_template("question_detail.html",
                         question=question,
                         user_is_like=user_is_like,
                         user_is_favorite=user_is_favorite,
                         comments=comments,
                         user=g.user if hasattr(g, 'user') else None)



@bp.route("/api/questions/<int:question_id>/like", methods=['POST'])
def like_question(question_id):
    question = QuestionModel.query.get_or_404(question_id)

    if not g.user:
        return jsonify({"success": False, "message": "请先登录"})

    user_id = g.user.id

    # 检查用户是否已点赞
    from models import QuestionLikeModel
    like_record = QuestionLikeModel.query.filter_by(
        user_id=user_id,
        ques_id=question_id
    ).first()

    if like_record:
        # 用户已点赞，取消点赞
        db.session.delete(like_record)
        question.like_count = max(0, question.like_count - 1)
        liked = False
    else:
        # 用户未点赞，添加点赞
        new_like = QuestionLikeModel(user_id=user_id, ques_id=question_id)
        db.session.add(new_like)
        question.like_count += 1
        liked = True

    db.session.commit()

    return jsonify({
        "success": True,
        "liked": liked,
        "like_count": question.like_count
    })



@bp.route("/api/questions/<int:question_id>/favorite", methods=['POST'])
def favorite_question(question_id):
    question = QuestionModel.query.get_or_404(question_id)

    if not g.user:
        return jsonify({"success": False, "message": "请先登录"})

    user_id = g.user.id

    # 检查用户是否已收藏
    from models import QuestionFavoriteModel
    favorite_record = QuestionFavoriteModel.query.filter_by(
        user_id=user_id,
        ques_id=question_id
    ).first()

    if favorite_record:
        # 用户已收藏，取消收藏
        db.session.delete(favorite_record)
        question.favorite_count = max(0, question.favorite_count - 1)
        favorited = False
    else:
        # 用户未收藏，添加收藏
        new_favorite = QuestionFavoriteModel(user_id=user_id, ques_id=question_id)
        db.session.add(new_favorite)
        question.favorite_count += 1
        favorited = True

    db.session.commit()

    return jsonify({
        "success": True,
        "favorited": favorited,
        "favorite_count": question.favorite_count
    })



@bp.route("/api/questions/<int:question_id>/comments", methods=['POST'])
def add_comment(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    content = request.json.get('content')

    if not content or not g.user:
        return jsonify({"success": False, "message": "内容不能为空或未登录"})

    # 创建评论
    from models import QuestionCommentModel  # 假设存在评论模型
    comment = QuestionCommentModel(
        comment_content=content,  # 修改字段名为 comment_content
        ques_id=question_id,      # 修改字段名为 ques_id
        user_id=g.user.id         # 修改字段名为 user_id
    )

    db.session.add(comment)
    question.comment_count += 1  # 增加问题的评论数
    db.session.commit()

    # 刷新对象以确保获取最新的数据库值
    db.session.refresh(comment)

    # 安全地处理时间字段，避免 None 值错误
    create_time_str = comment.create_time.strftime('%Y-%m-%d %H:%M:%S') if comment.create_time else '刚刚'

    return jsonify({
        "success": True,
        "message": "评论成功",
        "comment": {
            "id": comment.comment_id,
            "content": comment.comment_content,
            "create_time": create_time_str,
            "author_name": g.user.username
        }
    })



