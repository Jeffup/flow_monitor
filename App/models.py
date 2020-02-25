from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

# 模态框wtf类
from App.function import get_netcard


class SettingForm(FlaskForm):
    csrf_enabled = False
    choice = get_netcard()

    netcard = SelectField('选择网卡：',choices=choice ,_name='netcard')
    filterstr = TextAreaField(_name='filterstr', )
    submit = SubmitField('Submit')