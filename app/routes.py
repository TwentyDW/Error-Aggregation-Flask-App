from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_mail import Mail, Message
from raygun4py import raygunprovider
from raygun4py.middleware import flask
from myforms import TimeForm
import error_handling, mail_msg

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
  return redirect (url_for('error_page'), code = 302)

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
  
@app.route('/email_errors', methods=['GET', 'POST'])
def email_errors():
  beginningform = TimeForm(request.form)
  endform = TimeForm(request.form)

  if request.method == 'POST':
		beginning = beginningform.year + beginningform.month + beginningform.day + beginningform.hour + beginningform.min + beginningform.sec
		end = endform.year + endform.month + endform.day + endform.hour + endform.min + endform.sec
		
		
		begformatted = "%s/%s/%s %s:%s:%s" %(beginningform.month, beginningform.day, beginningform.year, beginningform.hour, beginningform.min, beginningform.sec)
		endformatted = "%s/%s/%s %s:%s:%s" %(endform.month, endform.day, endform.year, endform.hour, endform.min, endform.sec)
		report = "Between %s and %s, the following errors occurred:\n" %(begformatted, endformatted)
		
		errorcount = error_handling.count_errors(int(beginning), int(end))
		for error in errorcount:
			report += "%d of error \"%s\"\n" %(errorcount[error], error_handling.db.lindex(error, 0))	

		# move this to mail module
		ADMINS = ["derekw@arubanetworks.com"]
		msg = Message("Error Aggregation Report", sender = "derek.wang29@gmail.com", recipients = ADMINS)
		msg.body = report
		mail = Mail(app)
		mail.send(msg)

		return render_template('email_errors.html', form = beginningform) 

  elif request.method == 'GET':
    return render_template('email_errors.html')		
  
if __name__ == '__main__':
  app.run(debug=True)