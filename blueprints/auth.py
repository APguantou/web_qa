from flask import Blueprint, render_template, jsonify, redirect, url_for, session, request, flash
from models import EmailCaptchaModel, UserModel, QuestionModel, QuestionLikeModel, QuestionFavoriteModel, QuestionCommentModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from exts import mail, db
from flask_mail import Message
import random
import string

# 创建认证蓝图实例
bp = Blueprint("auth", __name__, url_prefix="/auth")


# ==================== 用户认证相关路由 ====================
@bp.route("/login_cgw", methods=['GET', 'POST'])
def login():
    """用户登录路由"""
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/logout_cgw")
def logout():
    """用户登出路由"""
    session.clear()
    return redirect("/")


@bp.route("/register_cgw", methods=['GET', 'POST'])
def register():
    """用户注册路由"""
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(
                username=username,
                password=generate_password_hash(password),
                email=email
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            return render_template("register.html", form_errors=form.errors)


# ==================== 邮箱验证码相关路由 ====================
@bp.route("/send_email_captcha", methods=['POST'])
def send_email_captcha():
    """发送邮箱验证码"""
    email = request.form.get('email')
    if not email:
        return jsonify({"success": False, "message": "邮箱不能为空"}), 400

    captcha = ''.join(random.choices(string.digits, k=6))

    captcha_record = EmailCaptchaModel(
        email=email,
        captcha=captcha,
    )
    db.session.add(captcha_record)
    db.session.commit()

    message = Message(
        subject="密码重置验证码",
        recipients=[email],
        body=f"您的验证码是：{captcha}，5分钟内有效。"
    )
    mail.send(message)

    return jsonify({"success": True, "message": "验证码已发送"})


@bp.route("/reset_pwd_cgw", methods=['POST'])
def reset_password():
    """重置密码路由"""
    # 获取表单数据
    email = request.form.get('email')
    email_captcha = request.form.get('email_captcha')
    new_password = request.form.get('new_password')
    # 参数校验
    if not all([email, email_captcha, new_password]):
        return jsonify({"success": False, "message": "所有字段均不能为空"}), 400

    # 验证邮箱验证码
    captcha_record = EmailCaptchaModel.query.filter_by(email=email).first()
    if not captcha_record or captcha_record.captcha != email_captcha:
        return jsonify({"success": False, "message": "邮箱验证码错误"}), 400

    # 查询用户并更新密码
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    user.password = generate_password_hash(new_password)
    db.session.delete(captcha_record)  # 删除验证码记录
    db.session.commit()

    return jsonify({"success": True, "message": "密码重置成功"})


# ==================== 用户页面相关路由 ====================
@bp.route("/user_page_cgw")
def user_page():
    """用户个人页面路由"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = UserModel.query.get(user_id)

    # 查询用户相关内容
    user_questions = QuestionModel.query.filter_by(author_id=user_id).order_by(
        QuestionModel.create_time.desc()
    ).all()

    # 查询我的点赞
    liked_questions = QuestionModel.query.join(QuestionLikeModel).filter(
        QuestionLikeModel.user_id == user_id
    ).order_by(QuestionLikeModel.create_time.desc()).all()

    # 查询我的收藏
    favorited_questions = QuestionModel.query.join(QuestionFavoriteModel).filter(
        QuestionFavoriteModel.user_id == user_id
    ).order_by(QuestionFavoriteModel.create_time.desc()).all()

    # 查询我的评论
    commented_questions = QuestionModel.query.join(QuestionCommentModel).filter(
        QuestionCommentModel.user_id == user_id
    ).order_by(QuestionCommentModel.create_time.desc()).all()

    return render_template(
        "user_page.html",
        user=user,
        user_questions=user_questions,
        liked_questions=liked_questions,
        favorited_questions=favorited_questions,
        commented_questions=commented_questions
    )


# ==================== 忘记密码相关路由 ====================
@bp.route("/forget_pwd_cgw")
def forget_pwd():
    """忘记密码页面路由"""
    return render_template("forget_pwd.html")


# ==================== 邮件测试相关路由 ====================
@bp.route("/mail/test_cgw")
def mail_test():
    """邮件测试路由"""
    message = Message(
        subject="邮箱测试",
        recipients=["759668916@qq.com"],
        body="这是一条测试邮件"
    )
    mail.send(message)
    return "邮件发送成功"


# ==================== 帖子删除相关路由 ====================
@bp.route("/auth/api/questions/delete/<int:question_id>", methods=['DELETE'])
def delete_question(question_id):
    """删除帖子路由"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "用户未登录"}), 401
    try:
        # 查询要删除的帖子
        question = QuestionModel.query.get_or_404(question_id)

        # 检查当前用户是否有权限删除该帖子（只有作者才能删除）
        if question.author_id != user_id:
            return jsonify({"success": False, "message": "您没有权限删除此帖子"}), 403

        # 删除帖子及其关联数据（如点赞、收藏、评论等）
        db.session.delete(question)
        db.session.commit()

        return jsonify({"success": True, "message": "帖子删除成功"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500
