#What?
A tool to locate your Unix PC on the same network by using your credentials.
There are essentially 2 modes of operation, either using nmap on Linux machines for searching, or using it on a Windows machine which may not have nmap.

This is essentially in situations where ZeroConf may not be suitable. For systems compatible with ZeroConf, please visit the Avahi website.

##Package Dependencies
- [paramiko](http://docs.paramiko.org/)
- [nmap](https://nmap.org/)
- [sshpass](http://sourceforge.net/projects/sshpass/)

##Usage
Clone the project in your directory. Ensure that the Python package dependencies are met.

Run:
```
# For locating machines within same subnet
$ ./sherlock.py

# For finding machines within another subnet, and say you are currently on 192.168.0.*
$ ./sherlock.py -e 192.168.1.123

# For finding machines while on a Windows machine
$ ./sherlock.py -w=y -e 192.168.0.1

# For directly connecting to the machine
$ ./sherlock.py -r

# For help
$ ./sherlock.py -h
```

##TODO:
- Hide error messages and log them.
- install script
