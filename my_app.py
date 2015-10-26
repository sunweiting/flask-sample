from flask import Flask, render_template, session, redirect, request, url_for
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
from bisect import bisect_left

from forms import NameForm

app = Flask(__name__)
Mobility(app)

app.secret_key = 'CHANGE_ME'

### ROUTING ###
@app.route('/', methods=['GET','POST'])
@mobile_template('{mobile/}index.html')
def index(template):
	form = NameForm(request.form)
	if request.method == 'POST' and form.validate():
		session["name"] = name_alter(form.name.data)
	return render_template(template, form=form)

#clears the session and then redirects back to index
@app.route('/logout')
def logout():
	session["name"] = ""
	return redirect(url_for('index'))

@app.route('/tool')
def tool():
	return "Hello World"

def percentile(meas):
    mw_HE1S = open("Data/mw_HE1S.txt", "r")
    list_mw_HE1S = []
    for line in mw_HE1S:
        remove_n = line.rstrip()
        int_form = int(remove_n)
        list_mw_HE1S.append(int_form)
    list_mw_HE1S.insert(bisect_left(list_mw_HE1S, meas), meas)
    indexx = list_mw_HE1S.index(meas)
    list_length = len(list_mw_HE1S)
    stats = float(indexx)/float(list_length)
    return stats*100

def name_alter(name):
    return "You are in the " + str(percentile(int(name))) + " percentile!"

if __name__ == "__main__":
    app.run(debug=True, port=8080)
