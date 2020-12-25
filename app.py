from flask import render_template, Flask
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,FieldList, PasswordField, BooleanField, IntegerField, Form,FormField
from wtforms.validators import InputRequired, Length, AnyOf, Email
from collections import namedtuple

app = Flask(__name__)
app.config['SECRET_KEY'] = "Mysecret"
#second way to disable crsf csrf_token(by false)
app.config['WTF_CRSF_ENABLED'] = True
#adding different secret key to crsf_enabled
app.config['WTF_CSRF_SECRET_KEY'] = 'mysecretkey'
#time limit for filling form(10 SECOND FOR EXAMPLE)
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
#Recaptcha
app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] =  ''

#Field enclosures example
class TelephoneForm(Form):
    country_code = IntegerField('country_code')
    area_code = IntegerField('area_code')
    number = StringField('number')
#Field list example
class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')

class LoginForm(FlaskForm):
    username = StringField('Your Username',validators=[InputRequired(),Length(min=4,max=8,message='Must be between 4 and 8 characters')])
    password = PasswordField('password',validators=[InputRequired(),AnyOf(values=['secret','password'])])
    age = IntegerField('age',default=24)
    true = BooleanField('true')
    email = StringField('email',validators=[Email()])
    #Field enclosures example
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    #Field list example
    years = FieldList(FormField(YearForm))
    recaptcha = RecaptchaField()

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

    group = namedtuple('Group',['year','total'])
    g1 = group(2005,1000)
    g2 = group(2006,1500)
    g3 = group(2007,1700)

    years = {'years':[g1,g2,g3]}
#one way to disable crsf token
    form = NameForm(obj=myuser,crsf_enabled=False,data=years)

    del form.mobile_phone

    if form.validate_on_submit():
        return '<h1>Username: {} Password: {} Age: {} True: {}</h1>'.format(form.username.data,form.password.data,form.age.data,form.true.data)

    return render_template('index.html',form=form)

@app.route('/dynamic',methods=['GET','POST'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    DynamicForm.name = StringField('name')
    names = ['middle_name','last_name','nickname']
    for name in names:
        setattr(DynamicForm,name,StringField(name))
    form = DynamicForm()

    if form.validate_on_submit():
        return 'Form has been validated. Name: {}'.format(form.name.data)

    return render_template('dynamic.html',form=form,names=names)

if __name__ == "__main__":
    app.run(debug=True)
