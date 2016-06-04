=== Installation of the nauru service ===

Adapt definitions in nauru shell script.

Copy naurud.py to ...

Copy nauru shell script to /etc/init.d.

Run command:
$ update-rc.d nauru defaults
It will create symbolic links in /etc/rc?.d directories. You can try option -n (don't do anything).

Adapt and copy nauru-logrotate to /etc/logrotate.d (optional step).

Start the service by rebooting system or running command:
$ /etc/nauru start
