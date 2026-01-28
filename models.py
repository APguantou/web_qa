from exts import db
from datetime import datetime
from sqlalchemy import func

class UserModel(db.Model):
    __tablename__ = "user_02"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, server_default=func.current_timestamp())
    post_count = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha_02"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(200), nullable=False)


class QuestionModel(db.Model):
    __tablename__ = "question_02"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, server_default=func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey("user_02.id"))
    author = db.relationship("UserModel", backref="questions")
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)


class QuestionFavoriteModel(db.Model):
    __tablename__ = "question_favorites_02"
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_02.id"), nullable=False)
    ques_id = db.Column(db.Integer, db.ForeignKey("question_02.id"), nullable=False)
    create_time = db.Column(db.DateTime, server_default=func.current_timestamp())

    user = db.relationship("UserModel", backref="favorites")
    question = db.relationship("QuestionModel", backref="favorited_by")


class QuestionLikeModel(db.Model):
    __tablename__ = "question_likes_02"
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_02.id"), nullable=False)
    ques_id = db.Column(db.Integer, db.ForeignKey("question_02.id"), nullable=False)
    create_time = db.Column(db.DateTime, server_default=func.current_timestamp())
    user = db.relationship("UserModel", backref="likes")
    question = db.relationship("QuestionModel", backref="liked_by")


class QuestionCommentModel(db.Model):
    __tablename__ = "question_comments_02"
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_02.id"), nullable=False)
    ques_id = db.Column(db.Integer, db.ForeignKey("question_02.id"), nullable=False)
    comment_content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, server_default=func.current_timestamp())
    user = db.relationship("UserModel", backref="comments")
    question = db.relationship("QuestionModel", backref="comments")
