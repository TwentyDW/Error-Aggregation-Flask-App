import json
	
class Error_Object():
  
	def __init__(self, __message_string, __stack_trace, __first_occurrence, __last_occurrence, __details, __count):
		self.message_string = __message_string # name of error
		self.stack_trace = __stack_trace # full stack trace given by traceback.format_exc()
		self.first_occurrence = __first_occurrence # time of first occurrence in string format
		self.last_occurrence = __last_occurrence # time of most recent occurrence in string format
		self.count = __count # number of times occurred
		self.details = __details # additional details, such as URL being accessed and the HTTP method
		
	def set_dict(self, dictobject):
		self.__dict__ = dictobject
		
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
		
	def set_details(self, __details):
		self.count = __count
	
	def get_details(self):
		return self.details