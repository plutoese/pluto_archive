# coding=UTF-8

from flask import Flask, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField, StringField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

class selectForm(Form):
    #language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    nameform = StringField('Please fill in your name')
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form = selectForm()
    if form.validate_on_submit():
        name = form.nameform.data
        form.nameform.data = 'good'
    return render_template('default.html',form=form,name=name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__ == '__main__':
    app.run(debug=True)