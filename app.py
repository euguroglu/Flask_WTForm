from flask import render_template, Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = "Mysecret"

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>Username: {} Password: {}</h1>'.format(form.username.data,form.password.data)

    return render_template('index.html',form=form)

if __name__ == "__main__":
    app.run(debug=True)
