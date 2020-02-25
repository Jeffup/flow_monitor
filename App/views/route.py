from flask import render_template

from App.models import SettingForm
from settings import NETCARD, FILTER

def init_route(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = SettingForm()
        global FILTER
        form.filterstr.data = FILTER
        if form.validate_on_submit():
            global NETCARD
            NETCARD = form.netcard.data
            FILTER = form.filterstr.data
            print(NETCARD,FILTER)
        return render_template('index.html', form=form)

    @app.route('/monitor', methods=['GET','POST'])
    def monitor():
        form = SettingForm()
        global FILTER
        form.filterstr.data = FILTER
        if form.validate_on_submit():
            global NETCARD
            NETCARD = form.netcard.data
            FILTER = form.filterstr.data
            print(NETCARD,FILTER)
        return render_template('monitor.html', form=form)