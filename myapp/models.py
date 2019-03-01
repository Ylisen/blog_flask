# -*- coding: utf-8 -*-
from myapp import db
from datetime import datetime
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True)
	password = db.Column(db.String(64))
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)

	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return self.id
	def __repr__(self):
		return '<User %r>' % (self.username)

	@classmethod
	def login_check(cls,username,password):
		user = cls.query.filter(db.and_(User.username == username, User.password == password)).first()
		if not user:
			return None
		return user

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100))
	content = db.Column(db.String(140))
	time = db.Column(db.DateTime,default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'))
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # 评论文章id
    content = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户id
    to_user = db.Column(db.Integer)  # 回复的用户,无则None
    to_id = db.Column(db.Integer)   # 回复目标id，无回复则None  #

    c_post = db.relationship('Post', backref=db.backref('comments', order_by=id.desc()))
    c_user = db.relationship('User', backref=db.backref('comments'))


# 回复评论模型
# class Reply(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # 根评论id
#     reply_type = db.Column(db.Integer, nullable=False)  # 回复类型; 1针对评论回复，2对回复进行回复
#     reply_id = db.Column(db.Integer, nullable=False)  # 回复评论的id; 当回复类型1时为comment_id，2时为此表id
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户id:当前登录状态下用户id
#     content = db.Column(db.String(100), nullable=False)  # 回复内容
#     to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 回复目标用户id
