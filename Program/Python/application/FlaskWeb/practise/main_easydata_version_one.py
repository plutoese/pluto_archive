# coding=UTF-8

from flask import Flask, render_template, redirect, url_for, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import SubmitField, SelectMultipleField
from library.datalayout.class_Layout import *

# 0. 初始化
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

# 1. 区域数据接口
AD = AdminCode()
# 默认参数是CEIC
regionData = RegionalData()
variables = regionData.variables()

# 2. 表单类
# 变量表单类
class VariablesForm(Form):
    variable = SelectMultipleField(u'变量选择', choices= [(variables[i],variables[i]) for i in range(len(variables))])
    submit = SubmitField('Submit')

# 年份表单类
class YearForm(Form):
    pass
    #year = SelectMultipleField(u'时间选择', choices= [(str(i),str(i)) for i in range(1979,2015)])
    #submit = SubmitField('Submit')

# 区域表单类
class RegionForm(Form):
    pass
    #year = SelectMultipleField(u'区域选择', choices= [(str(i),str(i)) for i in range(1979,2015)])
    #submit = SubmitField('Submit')

# index.html
@app.route('/',methods=['GET','POST'])
def index():
    vform = VariablesForm()
    if vform.validate_on_submit():
        session['variable'] = vform.variable.data
        vform.variable.data = ''
        return redirect(url_for('time'))
    return render_template('index.html',vform=vform)

# time.html
@app.route('/time',methods=['GET','POST'])
def time():
    querydict = {'variable':session.get('variable')}
    year = regionData.period(**querydict)
    YearForm.year = SelectMultipleField(u'时间选择', choices= [(str(i),str(i)) for i in year])
    YearForm.submit = SubmitField('Submit')
    yform = YearForm()
    if yform.validate_on_submit():
        session['year'] = yform.year.data
        yform.year.data = ''
        return redirect(url_for('region'))
    return render_template('time.html',yform=yform)

# time.html
@app.route('/region',methods=['GET','POST'])
def region():
    year = [int(y) for y in session.get('year')]
    querydict = {'variable':session.get('variable'),'year':year}
    region = regionData.region(**querydict)
    RegionForm.region = SelectMultipleField(u'区域选择', choices= region)
    RegionForm.submit = SubmitField('Submit')
    rform = RegionForm()
    if rform.validate_on_submit():
        session['region'] = rform.region.data
        rform.region.data = ''
        return redirect(url_for('result'))
    return render_template('region.html',rform=rform)

@app.route('/result')
def result():
    vars = session.get('variable')
    year = [int(y) for y in session.get('year')]
    regions = [AD.getByAcode(code) for code in session.get('region')]
    querydict = {'region':regions,'variable':vars,'year':year}
    query = regionData.query(**querydict)
    layout = Layout(query)
    data = layout.stackToNormal()
    file = r'C:\Room\Warehouse\GitWork\Program\Python\application\FlaskWeb\practise\result.xlsx'
    data.to_excel(file)
    return send_file('result.xlsx')
    #return render_template('result.html',variable=session.get('variable'),year=session.get('year'),region=session.get('region'))

if __name__ == '__main__':
    app.run(debug=True)