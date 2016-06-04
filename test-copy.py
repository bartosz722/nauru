import shutil
import os

# Copy all files from src_dir and subdirs to dst_dir. Files existing in 
# dst_dir are overwritten. Dir dst_dir must exist.
# All symlinks are skipped.
# File permissions are kept, file ownes are not kept.
# Dir permissions and owners are not kept.

# TODO: owner ans permissions MUST be kept

def copy_dir_to_other_dir(src_dir, dst_dir):
  # Remove trailing '/'
  src_dir = os.path.normpath(src_dir)
  dst_dir = os.path.normpath(dst_dir)
  
  for walk in os.walk(src_dir):
    curr_src_dir = walk[0]
    curr_dst_dir = curr_src_dir.replace(src_dir, dst_dir, 1)
    os.makedirs(curr_dst_dir, exist_ok=True)
    
    for f in walk[2]:      
      src_file_path = os.path.join(curr_src_dir, f)      
      dst_file_path = os.path.join(curr_dst_dir, f)
      
      if os.path.islink(src_file_path):
        print('Skip symlink:', src_file_path)
        continue                                         
            
      print('src_file_path:', src_file_path)  
      print('dst_file_path:', dst_file_path)      
      shutil.copyfile(src_file_path, dst_file_path, follow_symlinks=False)
      
copy_dir_to_other_dir('/tmp/nn', '/tmp/zzz')
