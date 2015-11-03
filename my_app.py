from flask import Flask, render_template, session, redirect, request, url_for
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
from bisect import bisect_left

from forms import NameForm
from math import floor

app = Flask(__name__)
Mobility(app)

app.secret_key = 'CHANGE_ME'

### ROUTING ###
@app.route('/', methods=['GET','POST'])
def index():
	form = NameForm(request.form)
	if request.method == 'POST' and form.validate():
		session["name"] = name_alter(form.name.data)
	return render_template('index.html', form=form)

#clears the session and then redirects back to index
@app.route('/logout')
def logout():
	session["name"] = ""
	return redirect(url_for('tool'))

@app.route('/tool', methods=['GET','POST'])
def tool():
	form = NameForm(request.form)
	if request.method == 'POST' and form.validate():
		session["name"] = name_alter(form.name.data)
	return render_template('tool.html', form=form)

@app.route('/rbeca')
def rbeca():
	return render_template('rbeca.html')

@app.route('/help')
def help():
	return render_template('help.html')

def percentile(meas):
    mw_HE1S = open("Data/mw_HE1S.txt", "r")
    list_mw_HE1S = []
    for line in mw_HE1S:
        remove_n = line.rstrip()
        int_form = int(remove_n)
        list_mw_HE1S.append(int_form)
    list_mw_HE1S.insert(bisect_left(list_mw_HE1S, meas), meas)
    indexx = list_mw_HE1S.index(meas)
    stats = float(indexx)/float(len(list_mw_HE1S))
    return stats*100

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

def name_alter(name):
    if isfloat(name) and ((float(name)/floor(float(name)))!=1):
        return "You are in the " + str(percentile(round(float(name)))) + " percentile!"
    if isint(name):
        return "You are in the " + str(percentile(int(name))) + " percentile!"
    if isinstance(name, basestring):
	return "Please enter a numerical value within the graph above!"  

if __name__ == "__main__":
    app.run(debug=True, port=8080)
