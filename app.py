from flask import render_template, Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = "Mysecret"

class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(),Length(min=4,max=8,message='Must be between 4 and 8 characters')])
    password = PasswordField('password',validators=[InputRequired()])

@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>Username: {} Password: {}</h1>'.format(form.username.data,form.password.data)

    return render_template('index.html',form=form)

if __name__ == "__main__":
    app.run(debug=True)
