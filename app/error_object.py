class Error_Object():
	def __init__(self, __hash, __message_string, __stack_trace, __first_occurrence, __last_occurrence, __url, __method, __count):
		self.hash = __hash # hash of (error string + stack trace string) 
		self.message_string = __message_string # name of error
		self.stack_trace = __stack_trace # full stack trace given by traceback.format_exc()
		self.first_occurrence = __first_occurrence # time of first occurrence in string format
		self.last_occurrence = __last_occurrence # time of most recent occurrence in string format
		self.count = __count # number of times occurred
		self.context = Context(__url, __method) # additional details, such as URL being accessed and the HTTP method
		
class Context():
	def __init__(self, __url, __method):
		self.url = __url
		self.method = __method
	
		