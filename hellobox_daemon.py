import daemon
from hellobox import main

dc=daemon.DaemonContext()

logfile = open("/tmp/hellobox.log", "w")

dc.stdout = logfile
dc.stderr = logfile

with dc:
	main()
