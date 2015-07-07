from flask.ext.wtf import Form
from wtforms import Form, TextField

class TimeForm(Form):
  day = TextField('Day (DD)')
  month = TextField('Month (MM)')
  year = TextField('Year (YY)')
  hour = TextField('Hour (HH)')
  min = TextField('Minute (mm)')
  sec = TextField('Second (ss)')