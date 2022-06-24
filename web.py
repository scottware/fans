from flask import Flask, render_template, send_file, request
# import matplotlib.pyplot as plt

import database
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, ValidationError
import configparser
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route("/data")
def data():
    result = database.select_today()
    return str(result);
    # return "Hello World!"


# @app.route("/foo")
# def foo():
#     results = database.select_today()
#
#     x = []
#     y = []
#     for result in results:
#         x.append(result[0])
#         y.append(result[1])
#     print(x)
#     print(y)
#     plt.plot(x, y)
#     plt.savefig('new_plot.png')
#
#     return render_template('index.html', times=results)


@app.route("/bar")
def bar():
    return send_file('new_plot.png', mimetype='image/png')



@app.route("/", methods=['GET', 'POST'])
def index():
    configuration = configparser.ConfigParser()
    configuration.read('config.ini')

    form = SettingForm()
    if form.validate_on_submit():
        configuration['APP']['target_temp']=form.target_temp.data
        configuration['APP']['mode']=form.mode.data
        configuration['APP']['status']=form.status.data

        with open('config.ini', 'w') as configfile:
            configuration.write(configfile)

    form.status.default = configuration['APP']['status']
    form.mode.default = configuration['APP']['mode']
    form.target_temp.default = configuration['APP']['target_temp']
    form.process()

    current_climate= database.select_last()
    current_climate=current_climate[0]
    fan_status = "off"
    if current_climate[4] == 1:
        fan_status = "on"

    return render_template('settings.html', settings=configuration['APP'], form=form, current_climate=current_climate,\
                           fan_status=fan_status)



@app.route("/tojson", methods=['GET', 'POST'])
def tojson():
    configuration = configparser.ConfigParser()
    configuration.read('config.ini')

    if request.method == 'POST':
        configuration['APP']['target_temp']=str(request.json['target_temp'])
        configuration['APP']['mode']=request.json['mode']
        configuration['APP']['status']=request.json['system_state']

        with open('config.ini', 'w') as configfile:
            configuration.write(configfile)

#    if request.method == 'GET':
    file = open('webstate.json', 'r')
    state = json.load(file)
    file.close()

    # current_climate= database.select_last()
    # current_climate=current_climate[0]
    #
    # state = {}
    # state['time'] = current_climate[0].timestamp()
    # state['inside_temp'] = current_climate[2]
    # state['outside_temp'] = current_climate[1]
    # state['target_temp_saved'] = configuration['APP']['target_temp']
    # state['target_temp'] = current_climate[3]
    # state['system_state'] = configuration['APP']['status']
    # state['fan_state'] = "on" if current_climate[4] == 1 else "off"
    # state['mode'] = configuration['APP']['mode']
    # print(json.dumps(state))
    return  json.dumps(state)



def tempRange(min=-1, max=-1):
    message = 'Temperature range must be between %d and %d.' % (min, max)

    def _length(form, field):
        l = int(field.data)
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length

class SettingForm(FlaskForm):
    target_temp = StringField('target_temp', validators=[DataRequired(),tempRange(50,85)])
    status = RadioField('status', choices=[('on', 'On'), ('off', 'Off')])
    mode = RadioField('mode', choices=[('cool', 'Cool'), ('heat', 'Heat')])
    submit = SubmitField('Update')



if __name__ == "__main__":
    app.run()
