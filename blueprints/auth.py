from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import random
import string
from models import EmailCaptchaModel, UserModel, QuestionModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from exts import mail, db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login_cgw", methods=['GET', 'POST'])
def login():
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
    session.clear()
    return redirect("/")


@bp.route("/forget_pwd_cgw", methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        return render_template("forget_pwd.html")


@bp.route("/register_cgw", methods=['GET', 'POST'])
def register():
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
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/mail/test_cgw")
def mail_test():
    message = Message(
        subject="邮箱测试",
        recipients=["759668916@qq.com"],
        body="这是一条测试邮件"
    )
    mail.send(message)
    return "邮件发送成功"


@bp.route("/captcha/email_cgw")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(
        subject="web开发验证码",
        recipients=[email],
        body=f"你的验证码是:{captcha},请小心保管"
    )
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/user_page_cgw")
def user_page():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = UserModel.query.get(user_id)
    user_questions = QuestionModel.query.filter_by(author_id=user_id).order_by(
        QuestionModel.create_time.desc()
    ).all()

    return render_template("user_page.html", user=user, user_questions=user_questions)


@bp.route("/delete_account_cgw", methods=['POST'])
def delete_account():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "用户未登录"}), 401

    try:
        # 查询用户
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "用户不存在"}), 404

        # 删除用户的提问（依赖于外键关系可能会自动删除，但这里显式删除更安全）
        user_questions = QuestionModel.query.filter_by(author_id=user_id).all()
        for question in user_questions:
            db.session.delete(question)

        # 删除用户本身
        db.session.delete(user)
        db.session.commit()

        # 清除 session
        session.clear()

        return jsonify({"success": True, "message": "账户已成功删除"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500

