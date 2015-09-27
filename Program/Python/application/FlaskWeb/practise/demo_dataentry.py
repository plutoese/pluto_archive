# coding=UTF-8

from flask import Flask, render_template, redirect, url_for, session, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from library.datalayout.class_Layout import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

AD = AdminCode()
regionData = RegionalData()
variables = regionData.variables()

class VariablesForm(Form):
    variable = SelectMultipleField(u'变量选择', choices= [(str(i),variables[i]) for i in range(len(variables))])
    submit = SubmitField('Submit')

class YearForm(Form):
    year = SelectMultipleField(u'时间选择', choices= [(str(i),str(i)) for i in range(1979,2015)])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    vform = VariablesForm()
    if vform.validate_on_submit():
        session['variable'] = vform.variable.data
        vform.variable.data = ''
        return redirect(url_for('time'))
    return render_template('index.html',vform=vform)

@app.route('/time',methods=['GET','POST'])
def time():
    yform = YearForm()
    if yform.validate_on_submit():
        session['year'] = yform.year.data
        yform.year.data = ''
        return redirect(url_for('result'))
    return render_template('time.html',yform=yform)

@app.route('/result')
def result():
    return render_template('result.html',variable=session.get('variable'),year=session.get('year'))

if __name__ == '__main__':
    app.run(debug=True)