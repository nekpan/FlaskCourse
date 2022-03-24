from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from FlaskBlogApp.models import User


def validate_email(form, email):
	email = User.query.filter_by(email=email.data).first()
	if email:
		raise ValidationError("Αυτό το email υπάρχει ήδη")

class SignupForm(FlaskForm):
	username = StringField(label="Username",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
					Length(min=3,max=15,message="Aυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

	email = StringField(label="email",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
					Email(message="Παρακαλώ εισάγετε ένα σωστό email"),validate_email])

	password = StringField(label="password",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
		Length(min=3,max=15,message="Aυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])	

	password2 = StringField(label="Επιβεβαίωση password",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
		Length(min=3,max=15,message="Aυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
		EqualTo('password',message="Tα δύο πεδία password πρέπει να είναι ίδια.")])

	submit = SubmitField("Εγγραφή")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Αυτό το username υπάρχει ήδη")

class LoginForm(FlaskForm):
	email = StringField(label="email",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
					Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

	password = StringField(label="password",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό.")])	
	
	remember_me = BooleanField(label="Remember Me")

	submit = SubmitField("Είσοδος")	

class NewArticleForm(FlaskForm):
	article_title = StringField(label="Τίτλος Άρθρου",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
		Length(min=3,max=50,message="Aυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

	article_body = TextAreaField(label="Άρθρο",
		validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
		Length(min=5,message="Aυτό το πεδίο πρέπει να έχει τουλάχιστον 5 χαρακτήρες")])

	submit = SubmitField("Αποστολή")	