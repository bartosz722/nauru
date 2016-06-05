=== Installation of the nauru service ===

Adapt definitions in nauru shell script.

Copy naurud.py to /usr/local/lib

Copy nauru shell script to /etc/init.d

Run command:
$ update-rc.d nauru defaults
It will create symbolic links in /etc/rc?.d directories. You can try option -n (don't do anything).

Adapt and copy nauru-logrotate to /etc/logrotate.d (optional step).

Start the service by rebooting system or running command:
$ /etc/nauru start


=== Q&A ===

Q: Why is this not written completly in shell?
A: Because copying files and sleeping in shell runs a new process. There is nothing wrong with that, I just wanted to write some code in Python;)


=== TODO ===

In python part: copy only when source file is newer.

Method save_in_copy_dir() in shell part need to have bool parameter 'update'. If false then copying is made without -u flag. This mode should be used when service is stopped. Because python script may be killed during copy and we want to ensure that no data is lost.

