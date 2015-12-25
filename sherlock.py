#!/usr/bin/python
import getpass
import os
import re
import paramiko, socket

#def parseCmd():

def getInput():
    # Get auth
    print "Welcome to Sherlock IP finder."
    username = raw_input("Username: ")
    password = getpass.getpass()
    idx= int(raw_input("Enter net interface: 1 - eth0, 2 - wlan0: "))
    netif = ['eth0', 'wlan0']
    # Get the IP address
    f = os.popen('ifconfig '+ netif[idx-1] +' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    your_ip = f.read()

    j = 0
    for i in range(3):
        j = your_ip.find('.', j+1)

    os.system('nmap -sP ' + your_ip[:j+1] + '* > /tmp/up.addr')
    f = open('/tmp/up.addr', 'r').read()

    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    patt = re.compile(pattern)
    ip = patt.findall(f)
    return [ip, username, password]

def findMc(ip, username, password):
    i = 1
    while i < len(ip):
        ip_addr = ip[i]
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            print "Trying for " + ip_addr + '....'
            ssh.connect(ip_addr, username=username, password=password)
            print "Connected."
            break
        except (paramiko.ssh_exception.BadHostKeyException, paramiko.ssh_exception.AuthenticationException,
                paramiko.ssh_exception.SSHException, socket.error) as e:
            print e
            i+=1
            continue
        print ip_addr + " done"
    if i >= len(ip):
        print "Desired machine is not found"
    else:
        print "Your desired IP is " + ip[i]


if __name__ == '__main__':
    #ip, ret = parseCmd()
    [ip, username, password] = getInput()
    findMc(ip, username, password)
