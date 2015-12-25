#What?
A tool to locate your Unix PC on the same network by using your credentials.

##Package Dependencies
- [paramiko](http://docs.paramiko.org/)
- [nmap](https://nmap.org/)

##Usage
Clone the project in your directory. Ensure that the Python package dependencies are met.

Run:
```
# For locating machines within same subnet
$ ./sherlock.py

# For finding machines within another subnet, and say you are currently on 192.168.0.*
$ ./sherlock.py -e 192.168.1.123

# For help
$ ./sherlock.py -h
```

##TODO:
- Hide error messages and log them.
- install script
