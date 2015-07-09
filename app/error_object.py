""" use json.dumps to convert obj to string

error object:
  - name string
	- stack trace string
	- first occurrence timestamp
	- last occurence timestamp
	- count"""
	
class Error_Object():
  
	def __init__(self, __message_string, __stack_trace, __first_occurrence, __last_occurrence, __count):
	  self.message_string = __message_string
		self.stack_trace = __stack_trace
		self.first_occurrence = __first_occurrence
		self.last_occurrence = __last_occurrence
		self.count = __count
		
	def set_message_string(self, __message_string):
	  self.message_string = __message_string
		
	def get_message_string(self):
	  return self.message_string
		
	def set_stack_trace(self, __stack_trace):
	  self.stack_trace = __stack_trace
	
	def get_stack_trace(self):
	  return self.stack_trace
		
	def set_first_occurrence(self, __first_occurrence):
	  self.first_occurrence = __first_occurrence
	
	def get_first_occurrence(self):
	  return self.first_occurrence
		
	def set_last_occurrence(self, __last_occurrence):
	  self.last_occurrence = __last_occurrence
	
	def get_last_occurrence(self):
	  return self.last_occurrence
		
	def set_count(self, __count):
	  self.count = __count
	
	def get_count(self):
	  return self.count