import datetime, redis, hashlib, pytz, time, os, sys, json

##### identify using hash of error string and stack trace combined



db = redis.StrictRedis("localhost")
mytz = pytz.timezone('US/Pacific')

def write_str_to_file(string, filename):
  location = os.path.join("C:/users/derekw/desktop/work/flaskapp/app/", filename)
  with open(location, "a") as file:
    file.write(string)

def store_error(errorstring):

  # also test traceback here to see if it produces the same result	
  error_time = datetime.datetime.now(mytz)
  
  # write to local file
  write_str_to_file(errorstring, "errorlog.txt")
  write_str_to_file(error_time.strftime(" %Y/%m/%d %H:%M:%S\n"), "errorlog.txt")
  
  #hash the error's name
  unhashed_error = errorstring
  hashobject = hashlib.md5(unhashed_error.encode())
  hashederror = hashobject.hexdigest()
  
  for i in range(0, db.llen("list_of_errors")): # loop to check if hashederror is in list already
    if hashederror == db.lindex("list_of_errors", i):
      break
  else:
    db.lpush("list_of_errors", hashederror) # if hashederror is not in list, add it
  
  if db.llen(hashederror) == 0 or db.lindex(hashederror, 0) != unhashed_error:
    db.lpush(hashederror, unhashed_error)
  else: 
    pass
	
  db.rpush(hashederror, error_time.strftime("%Y%m%d%H%M%S"))
	
	#==============================
	# update info about error
	if db.get(hashederror):
	  error_instance_json = db.get(hashederror)
		error_instance = json.loads(error_instance_json)
		error_instance.set_last_occurrence(error_time)  # update last occurrence time stamp
		error_instance.set_count(error_instance.get_count + 1) # increase error count by 1
	else:
	  error_instance = Error_Object(unhashed_error, """stack trace string""", error_time, error_time, 1)
		
	error_instance_json = json.dumps(error_instance, ensure_ascii=True)
	db.set(hashederror, error_instance_json)
		
	
  
    
def count_errors(beginning, end):
  errorcount = {}
  for i in range(0, db.llen("list_of_errors")):
    for j in range(1, db.llen(db.lindex("list_of_errors", i))):	
      errortimestamp = int(db.lindex(db.lindex("list_of_errors", i), j))
      if errortimestamp <= end and errortimestamp >= beginning: 
        if db.lindex("list_of_errors", i) in errorcount:
          errorcount[db.lindex("list_of_errors", i)] += 1
        else:
          errorcount[db.lindex("list_of_errors", i)] = 1
  return errorcount
	
	
  