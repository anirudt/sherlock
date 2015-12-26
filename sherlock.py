#!/usr/bin/python
import getpass
import os
import re
import paramiko, socket
import optparse

desc = "Quick automated tool developed to find your Linux machine using your credentials. For finding machines on the same subnet, just run sherlock without any arguments. For finding machines on another subnet of the same network, use the '-e' for options."

def parseCmd():
    p = optparse.OptionParser(description=desc)
    p.add_option('-e', '--ext', dest='ext', default='', help='take external subnet ip if required')
    p.add_option('-w', '--win', dest='win', default='', help='set = y if acting on a windows machine')
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
    opts = parseCmd()
    [ip, username, password] = getInput(opts)
    findMc(ip, username, password)
