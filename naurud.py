import time
import os
import sys
import traceback
import shutil
import stat

log_file_name = '/var/log/nauru.log'

original_dir = None
copy_dir = None
owner = None
owner_group = None

# Arguments:
# 1 - path to pid file
# 2 - original dir
# 3 - copy dir
# 4 - user name
# 5 - group name

def main():
  try:
    if not parse_args(sys.argv):
      return
    
    if(not check_and_create_pid(sys.argv[1])):
      return    

    while True:
      time.sleep(60 * 3)
      log("Copy files")
      copy_dir_to_other_dir(original_dir, copy_dir)
      log("chown")
      chown_recursive(copy_dir, owner, owner_group)
      log("Cycle done")      
        
  except:
    log('Exception!')
    log(traceback.format_exc())
 
def log(txt):  
  with open(log_file_name, "a") as log_file:
    log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + " " + txt + "\n")
    
def check_and_create_pid(pid_file):
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
  
def parse_args(argv):
  global original_dir
  global copy_dir
  global owner
  global owner_group
  
  if len(argv) != 6:
    log('Invalid number of arguments: {}'.format(len(argv)))
    return False

  for i in range(2, 6):
    if not argv[i]:
      log('Invalid parameters')
      return False
    
  original_dir = argv[2]
  copy_dir = argv[3]
  owner = argv[4]
  owner_group = argv[5]
  
  log("original_dir: {}\ncopy_dir:{}\nowner: {}\nowner_group: {}"
      .format(original_dir, copy_dir, owner, owner_group))
  return True
    
# Copy all files from src_dir and subdirs to dst_dir. Files existing in 
# dst_dir are overwritten. Paths src_dir and dst_dir must be absolute.
# Only regular files are copied, all symlinks are skipped.
# File and dir permissions and owners are not kept.
def copy_dir_to_other_dir(src_dir, dst_dir):
  # Remove trailing '/'
  src_dir = os.path.normpath(src_dir)
  dst_dir = os.path.normpath(dst_dir)
  
  for walk in os.walk(src_dir, followlinks=False):
    curr_src_dir = walk[0]
    curr_dst_dir = curr_src_dir.replace(src_dir, dst_dir, 1)
    os.makedirs(curr_dst_dir, exist_ok=True)
    
    for f in walk[2]:      
      src_file_path = os.path.join(curr_src_dir, f)      
      dst_file_path = os.path.join(curr_dst_dir, f)
      
      if not stat.S_ISREG(os.lstat(src_file_path).st_mode):
        log('Skip nonregular file: ' + src_file_path)
        continue                                         
            
      log("Copy '{}' to '{}'".format(src_file_path, dst_file_path))
      shutil.copyfile(src_file_path, dst_file_path, follow_symlinks=False)

# Recursively change owner of dirs and regular files.
def chown_recursive(path, user=None, group=None):
  chown_dir_or_regular_file(path, user, group)
  for walk in os.walk(path, followlinks=False):
    files_and_dirs = walk[1] + walk[2]
    for x in files_and_dirs:
      curr_path = os.path.join(walk[0], x)
      chown_dir_or_regular_file(curr_path, user, group)
  
def chown_dir_or_regular_file(path, user=None, group=None):
  mode = os.lstat(path).st_mode
  if stat.S_ISREG(mode) or stat.S_ISDIR(mode):
    shutil.chown(path, user, group)
    
main()
