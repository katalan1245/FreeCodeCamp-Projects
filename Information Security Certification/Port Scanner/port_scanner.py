import socket
from common_ports import ports_and_services
import re

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    ip, isIP = getIP(target)

    try:
      socket.inet_aton(ip)
    except socket.error:
      return "Error: Invalid IP address" if isIP else "Error: Invalid hostname"
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    start, end = port_range

    for port in range(start, end+1):
      if isPortOpen(ip, port):
        open_ports.append(port)

    sock.close()
    if not verbose:
      return open_ports
    
    desc = ""
    try:
      desc = "Open ports for "+ socket.gethostbyaddr(ip)[0] + " " + ip + "\n"
    except:
      desc = "Open ports for {unkown host} (%s)\n" % ip
    
    desc += "PORT     SERVICE\n"
    for port in open_ports:
      if port in ports_and_services.keys():
        desc += str(port) + "     " + ports_and_services[port] + "\n"

    return desc

def getIP(target):
  res = re.match(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$", target)
  if res:
    return target, True
  return socket.gethostbyname(target), False

def isPortOpen(ip, port):
  tmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  tmp.settimeout(5)
  res = tmp.connect_ex((ip, port))
  tmp.close()
  return res == 0