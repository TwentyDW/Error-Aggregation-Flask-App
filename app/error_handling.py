import datetime, redis, hashlib, pytz, time, os, sys

db = redis.StrictRedis("localhost")
mytz = pytz.timezone('US/Pacific')

def write_str_to_file(string, filename):
  location = os.path.join("C:/users/derekw/desktop/work/flaskapp/app/", filename)
  with open(location, "a") as file:
    file.write(string)

def store_error(errorstring):
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
    db.lpush("list_of_errors", hashederror)
  
  if db.llen(hashederror) == 0 or db.lindex(hashederror, 0) != unhashed_error:
    db.lpush(hashederror, unhashed_error)
  else: 
    pass
	
  db.rpush(hashederror, error_time.strftime("%Y%m%d%H%M%S"))
  
    
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
  