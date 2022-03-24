from flask import (render_template, redirect, url_for, request, flash)
import json

from FlaskBlogApp.Forms import SignupForm, LoginForm, NewArticleForm

from FlaskBlogApp import app, db, bcrypt

from FlaskBlogApp.models import User, Article

from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def root(name=None):
	articles = Article.query.all()
	return render_template("index.html", articles=articles)

@app.route("/signup/", methods=["GET", "POST"])
def signup():

	form = SignupForm()

	if request.method == 'POST' and form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		password2 = form.password2.data
		
		encrypted_password = bcrypt.generate_password_hash(password).decode('UTF-8')

		user = User(username=username, email=email, password=encrypted_password)
		db.session.add(user)
		db.session.commit()

		flash(f'O λογαριασμός για τον χρήστη <b>{username}</b> δημιουργήθηκε επιτυχώς', 'success')
		return redirect(url_for('login'))

	return render_template("signup.html", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():

	if current_user.is_authenticated:
		return redirect(url_for("root"))

	form = LoginForm()

	if request.method == 'POST' and form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		
		user = User.query.filter_by(email=email).first()

		if user and bcrypt.check_password_hash(user.password, password):
			flash(f"H είσοδος του χρήστη με mail {email} έγινε επιτυχώς", "success")
			login_user(user,remember=form.remember_me.data)

			next_link = request.args.get("next")

			if next_link:
				return redirect(next_link)
			else:
				return redirect(url_for("root"))
			#return redirect(url_for("root"))

		else:
			flash(f"Η είσοδός του χρήστη με email {email} ήταν ανεπιτυχής.", "warning")

	return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
	logout_user()

	flash("Eγινε αποσύνδεση του χρήστη.", "success")
	return redirect(url_for("root"))

@app.route("/new_article/", methods=["GET", "POST"])
@login_required
def new_article():
	form = NewArticleForm()

	if request.method == 'POST' and form.validate_on_submit():
		article_title = form.article_title.data
		article_body = form.article_body.data
		print(article_title,article_body)
	return render_template("new_article.html", form=form)