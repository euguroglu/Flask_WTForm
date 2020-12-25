from flask import render_template, Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, AnyOf, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = "Mysecret"
#second way to disable crsf csrf_token(by false)
app.config['WTF_CRSF_ENABLED'] = True
#adding different secret key to crsf_enabled
app.config['WTF_CSRF_SECRET_KEY'] = 'mysecretkey'
#time limit for filling form(10 SECOND FOR EXAMPLE)
app.config['WTF_CSRF_TIME_LIMIT'] = 10



class LoginForm(FlaskForm):
    username = StringField('Your Username',validators=[InputRequired(),Length(min=4,max=8,message='Must be between 4 and 8 characters')])
    password = PasswordField('password',validators=[InputRequired(),AnyOf(values=['secret','password'])])
    age = IntegerField('age',default=24)
    true = BooleanField('true')
    email = StringField('email',validators=[Email()])

class NameForm(LoginForm):
    firstname = StringField('firstname')
    lastname = StringField('lastname')

#Prepopulation example
class User():
    def __init__(self,username,age,email):
        self.username = username
        self.age = age
        self.email = email

@app.route('/',methods=['GET','POST'])
def index():
    myuser = User('Enes',28,'euguroglu@trial.com')
#one way to disable crsf token
    form = NameForm(obj=myuser,crsf_enabled=False)

    if form.validate_on_submit():
        return '<h1>Username: {} Password: {} Age: {} True: {}</h1>'.format(form.username.data,form.password.data,form.age.data,form.true.data)

    return render_template('index.html',form=form)

if __name__ == "__main__":
    app.run(debug=True)
