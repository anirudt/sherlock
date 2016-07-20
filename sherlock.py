#!/usr/bin/python
import getpass
import os
import re
import paramiko, socket
import optparse
from threading import Thread

desc = "Quick automated tool developed to find your Linux machine using your credentials. For finding machines on the same subnet, just run sherlock without any arguments. For finding machines on another subnet of the same network, use the '-e' for options."

found = None

def parseCmd():
    p = optparse.OptionParser(description=desc)
    p.add_option('-e', '--ext', dest='ext', default='', help='take external subnet ip if required')
    p.add_option('-w', '--win', dest='win', default='', help='set = y if acting on a windows machine')
    p.add_option('-r', '--red', dest='red', action='store_true', default=False, help='redirects and connects you to the ssh connection')
    (opts, args) = p.parse_args()
    return opts

def getInput(opts):
    ip = opts.ext
    win = opts.win
    # Get auth
    print "Welcome to Sherlock IP finder."
    username = raw_input("Username: ")
    password = getpass.getpass()
    if not ip:
        idx= int(raw_input("Enter net interface: 1 - eth0, 2 - wlan0: "))
        netif = ['eth0', 'wlan0']
        # Get the IP address
        f = os.popen('ifconfig '+ netif[idx-1] +' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
        your_ip = f.read()
    else:
        your_ip = ip
        
    j = 0
    for i in range(3):
        j = your_ip.find('.', j+1)

    if win == 'y' or win == 'Y':
        ip = []
        for i in range(2,256):
            ip.append(your_ip[:j+1]+str(i))

    else:
        os.system('nmap -sP ' + your_ip[:j+1] + '* > /tmp/up.addr')
        f = open('/tmp/up.addr', 'r').read()

        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        patt = re.compile(pattern)
        ip = patt.findall(f)
    return [ip, username, password]

def worker(host, username, password):
    global found
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "Trying for " + host + " ...."
        ssh.connect(host, username = username, password = password)
        print "Connected for " + host
        found = host
        return True
    except (paramiko.ssh_exception.BadHostKeyException, paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.SSHException, socket.error) as e:
        print e
        return False

def findMc(ip, username, password):
    threads = []
    for host in ip:
        t = Thread(target=worker, args = (host, username, password))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    if found is not None:
        print "The correct destination is " + found

if __name__ == '__main__':
    opts = parseCmd()
    [ip, username, password] = getInput(opts)
    hostname = findMc(ip, username, password)
    if opts.red:
        print "Redirecting you to the SSH connection"
        os.system('sshpass -p '+password+' ssh '+username+'@'+hostname)
