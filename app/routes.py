from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_mail import Mail, Message
from raygun4py import raygunprovider
from raygun4py.middleware import flask
import error_handling

app = Flask(__name__)
raygun = raygunprovider.RaygunSender("VaBnbg4l+u9r+2qgdGtx1A==") # raygun
flask.Provider(app, 'VaBnbg4l+u9r+2qgdGtx1A==').attach() # raygun
app.config.from_object('config')

""" to do: fix form and create mail module"""

@app.errorhandler(Exception)
def internal_error(error):
  send_error_to_raygun()
  error = str(error)
  error_handling.store_error(error)
  return redirect (url_for('error_page'), code = 302) # will change

def send_error_to_raygun():
  err = error_handling.sys.exc_info()
  raygun.send_exception()
  
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/error_page')
def error_page():
 return render_template('error_page.html')  
  
@app.route('/error1')
def error1():
  print 5/0
  return error

@app.route('/error2')
def error2():
  print 4 + spam * 3
  return error
  
@app.route('/error3')
def error3():
  print '2' + 2
  return error

@app.route('/error4')
def error4():
  raise ValueError('Test ValueError')
  return error
  
@app.route('/email_errors')
def email_errors():

		return render_template('email_errors.html') 
  
@app.route('/emailed_errors', methods=['GET', 'POST'])
def emailed_errors():

	begyear = request.form['begyear']
	begmonth = request.form['begmonth']
	begday = request.form['begday']
	beghour = request.form['beghour']
	begmin = request.form['begmin']
	begsec = request.form['begsec']
	endyear = request.form['endyear']
	endmonth = request.form['endmonth']
	endday = request.form['endday']
	endhour = request.form['endhour']
	endmin = request.form['endmin']
	endsec = request.form['endsec']

	report = error_handling.report_errors()

	# move this to mail module
	ADMINS = ["derekw@arubanetworks.com"]
	msg = Message("Error Aggregation Report", sender = "derek.wang29@gmail.com", recipients = ADMINS)
	msg.body = report
	mail = Mail(app)
	mail.send(msg)
	
	return render_template('emailed_errors.html')

if __name__ == '__main__':
  app.run(debug=True)