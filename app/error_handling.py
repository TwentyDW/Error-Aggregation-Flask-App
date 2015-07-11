import datetime, redis, hashlib, pytz, time, os, sys, json, traceback
from error_object import Error_Object

db = redis.StrictRedis("localhost")
mytz = pytz.timezone('US/Pacific') # can change

def write_str_to_file(string, filename):
  location = os.path.join("C:/users/derekw/desktop/work/flaskapp/app/", filename)
  with open(location, "a") as file:
    file.write(string)

def store_error(errorstring, flaskrequest):
	error_time = datetime.datetime.now(mytz)

	#hash the error's name
	unhashed_error = errorstring + traceback.format_exc() # unhashed_error is error string + stack trace string
	hashobject = hashlib.md5(unhashed_error.encode())
	hashederror = hashobject.hexdigest() # hash of (error string + stack trace string)

	# update info about error
	if db.hexists("errors", hashederror):
		error_instance_dict_json = db.hget("errors", hashederror)
		error_instance_dict = json.loads(error_instance_dict_json)
		error_instance = Error_Object("","","","","","","",-5)
		error_instance.__dict__ = error_instance_dict
		error_instance.last_occurrence = error_time.strftime("%Y/%m/%d %H:%M:%S")  # update last occurrence time stamp
		error_instance.count += 1 # increase error count by 1
	else:
		error_instance = Error_Object(errorstring, traceback.format_exc(), error_time.strftime("%Y/%m/%d %H:%M:%S"), error_time.strftime("%Y/%m/%d %H:%M:%S"), flaskrequest.url, flaskrequest.method,  1)

	error_instance_dict_json = json.dumps(error_instance.__dict__, ensure_ascii=True)
	db.hset("errors", hashederror, error_instance_dict_json)
	
	write_str_to_file(error_instance_dict_json + "\n--------\n", "errorlog.txt")
  
def report_errors():
	report = "list of json error objects:\n"
	array_of_jsons = db.hvals("errors")

	for i in range(0, len(array_of_jsons)):
		report += array_of_jsons[i]

	return report
	
  