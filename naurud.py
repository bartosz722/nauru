import time
import os
import sys
import traceback

log_file_name = '/tmp/nauru.log'

def main():
  try:
    if(not check_pid(sys.argv[1])):
      return

    while True:
      log('dupppa')
      time.sleep(5)
        
  except:
    log('Exception!')
    log(traceback.format_exc())
 
    
def check_pid(pid_file):
  log('pid_file: {}'.format(pid_file))
  
  pid = os.getpid()
  log('PID: {}'.format(pid))
  
  if(os.path.exists(pid_file)):
    log('Daemon already running!')
    return False
      
  with open(pid_file, 'w') as outfile:
    outfile.write(str(pid))

  log('PID stored to a file')
  return True
  

def log(txt):  
  with open(log_file_name, "a") as log_file:
    log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + " " + txt + "\n")
    
    
main()
