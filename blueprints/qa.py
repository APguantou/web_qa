from .forms import QuestionForm
from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from models import QuestionModel, UserModel, QuestionCommentModel, QuestionLikeModel, QuestionFavoriteModel
from exts import db
import requests

# 创建问答蓝图实例
bp = Blueprint("qa", __name__, url_prefix="/")

# 天气 API 配置
WEATHER_API_URL = "http://gfeljm.tianqiapi.com/api"
WEATHER_API_PARAMS = {
    "unescape": 1,
    "version": "v63",
    "appid": "77169278",
    "appsecret": "B5zsBnJX"
}

def update_user_points(user_id, points):
    """更新用户积分"""
    try:
        user = UserModel.query.get(user_id)
        if user:
            user.points = (user.points or 0) + points
            db.session.commit()
    except Exception as e:
        print(f"更新用户积分失败: {e}")
        db.session.rollback()

def get_weather(city="Beijing"):
    """获取天气信息"""
    try:
        params = WEATHER_API_PARAMS.copy()
        params["city"] = city
        response = requests.get(WEATHER_API_URL, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city"),
                "temperature": data.get("tem"),
                "description": data.get("wea")
            }
        else:
            print(f"API 请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"获取天气异常：{e}")
        return None

@bp.route("/api/weather")
def api_weather():
    """天气 API 路由"""
    weather_data = get_weather()
    if weather_data:
        return jsonify(weather_data)
    return jsonify({"error": "无法获取天气信息"}), 500

@bp.route("/")
def index():
    """首页路由"""
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    weather_data = get_weather()

    if search_query:
        questions_pagination = QuestionModel.query.filter(
            db.or_(
                QuestionModel.title.contains(search_query),
                QuestionModel.content.contains(search_query)
            )
        ).order_by(QuestionModel.create_time.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        questions_pagination = QuestionModel.query.order_by(
            QuestionModel.create_time.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

    questions = questions_pagination.items
    return render_template(
        "index.html",
        questions=questions,
        pagination=questions_pagination,
        search_query=search_query,
        weather=weather_data
    )

@bp.route("/qa/public_cgw", methods=['GET', 'POST'])
def public_question():
    """发布问题路由"""
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            update_user_points(g.user.id, 10)
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/top_list")
def top_list():
    """热榜路由"""
    questions = QuestionModel.query.order_by(QuestionModel.view_count.desc()).limit(10).all()
    creators = UserModel.query.order_by(UserModel.points.desc()).limit(10).all()
    return render_template("top_list.html", questions=questions, creators=creators)

@bp.route("JS_index_cgw")
def JS_index():
    """JS 首页路由"""
    return render_template("JS_index.html")

def check_user_liked(user_id, question_id):
    """检查用户是否已点赞"""
    like_record = QuestionLikeModel.query.filter_by(user_id=user_id, ques_id=question_id).first()
    return bool(like_record)

def check_user_favorited(user_id, question_id):
    """检查用户是否已收藏"""
    favorite_record = QuestionFavoriteModel.query.filter_by(user_id=user_id, ques_id=question_id).first()
    return bool(favorite_record)

@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    """问题详情路由"""
    question = QuestionModel.query.get_or_404(question_id)
    question.view_count += 1
    db.session.commit()

    current_user_id = g.user.id if hasattr(g, 'user') and g.user else None
    user_is_like = check_user_liked(current_user_id, question_id)
    user_is_favorite = check_user_favorited(current_user_id, question_id)
    comments = QuestionCommentModel.query.filter_by(ques_id=question_id).all()

    return render_template("question_detail.html",
                         question=question,
                         user_is_like=user_is_like,
                         user_is_favorite=user_is_favorite,
                         comments=comments,
                         user=g.user if hasattr(g, 'user') else None)

@bp.route("/api/questions/<int:question_id>/like", methods=['POST'])
def like_question(question_id):
    """点赞问题 API"""
    question = QuestionModel.query.get_or_404(question_id)
    if not g.user:
        return jsonify({"success": False, "message": "请先登录"})

    user_id = g.user.id
    like_record = QuestionLikeModel.query.filter_by(user_id=user_id, ques_id=question_id).first()

    if like_record:
        db.session.delete(like_record)
        question.like_count = max(0, question.like_count - 1)
        liked = False
        update_user_points(question.author_id, -2)
    else:
        new_like = QuestionLikeModel(user_id=user_id, ques_id=question_id)
        db.session.add(new_like)
        question.like_count += 1
        liked = True
        update_user_points(question.author_id, 2)

    db.session.commit()
    return jsonify({"success": True, "liked": liked, "like_count": question.like_count})

@bp.route("/api/questions/<int:question_id>/favorite", methods=['POST'])
def favorite_question(question_id):
    """收藏问题 API"""
    question = QuestionModel.query.get_or_404(question_id)
    if not g.user:
        return jsonify({"success": False, "message": "请先登录"})

    user_id = g.user.id
    favorite_record = QuestionFavoriteModel.query.filter_by(user_id=user_id, ques_id=question_id).first()

    if favorite_record:
        db.session.delete(favorite_record)
        question.favorite_count = max(0, question.favorite_count - 1)
        favorited = False
        update_user_points(question.author_id, -5)
    else:
        new_favorite = QuestionFavoriteModel(user_id=user_id, ques_id=question_id)
        db.session.add(new_favorite)
        question.favorite_count += 1
        favorited = True
        update_user_points(question.author_id, 5)

    db.session.commit()
    return jsonify({"success": True, "favorited": favorited, "favorite_count": question.favorite_count})

@bp.route("/api/questions/<int:question_id>/comments", methods=['POST'])
def add_comment(question_id):
    """添加评论 API"""
    question = QuestionModel.query.get_or_404(question_id)
    content = request.json.get('content')

    if not content or not g.user:
        return jsonify({"success": False, "message": "内容不能为空或未登录"})

    comment = QuestionCommentModel(
        comment_content=content,
        ques_id=question_id,
        user_id=g.user.id
    )

    db.session.add(comment)
    question.comment_count += 1
    db.session.commit()
    update_user_points(g.user.id, 2)

    db.session.refresh(comment)
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
