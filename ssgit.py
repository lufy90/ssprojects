#!/bin/env python36
# ssgit.py
# 

import cmdmain
from settings import *
import socket
import getpass
import sys,os
import pickle
from lib import bytes_to_obj, obj_to_bytes, md5sum, file_mata
from lib import diff
from stat import S_IRUSR, S_IWUSR


class Options(cmdmain.Options):
  def __init__(self, name, args=None):
    super(Options, self).__init__(name, args)
    self.call_options = {
      'help': self.usage,
      'login': self.login,
      'logout': self.logout,
      'push': self.push,
      'pull': self.pull,
      'list': self.listfiles,
      'stat': self.status,
      'rm': self.remove,
      }


  def usage(self, args):
    ''' print this help. '''
    print('Usage:')
    for i in self.call_options.keys():
      print(' %-6s %s' % (i, self.call_options[i].__doc__))

  def login(self, args):
    ''' login to server: login test.com '''
    if not args:
      args = DEFAULT_HOST
    else:
      args = args[0]
    try:
      client=Client(host=args)
    except socket.error as e:
      print(e)
      sys.exit(2)

    name = input('Name: ')
    password = getpass.getpass('Password: ')
    data = SendData('login', name, password, )
    client.send(data.data)
    recv_data = client.sock.recv(1024)
    client.close()
    try:
      recv_obj_data = bytes_to_obj(recv_data)
    except Exception as e: 
      print('Bad respond from server.')
      sys.exit(4)

    os.path.exists(C_CACHE_DIR) or os.makedirs(C_CACHE_DIR)
    with open(C_CACHE_DIR+'/'+'client', 'wb') as f:
      if recv_obj_data['code'] is 0:
        cache_data = {'username': name, 'server': args, 
                      'userkey': recv_obj_data['content']}
        print('Login OK')
      else:
        cache_data = {}
        print('Auth failed')
        sys.exit(1)
      pickle.dump(cache_data, f)
      os.chmod(C_CACHE_DIR+'/'+'client', S_IRUSR|S_IWUSR)

  def get_cache(self):
    with open(C_CACHE_DIR+'/'+'client', 'rb') as f:
      try:
        data = pickle.load(f)
      except EOFError as e:
        data = None
    if data:
      return data
    else:
      print('Please login first')
      sys.exit(2)
      
 
  def push(self, args):
    ''' push directory to server: push dir '''
    if not args:
      print('Must push a directory.')
      sys.exit(2)

    else:
      args = args[0]

    tmp_data = self.get_cache()
    path = os.path.abspath(args)
    dir_name = path.split('/')[-1]
    filemata = []
#    self.file_mata(path, dir_name, len(path)+1, content=filemata)

    file_mata(path, len(path)+1, content=filemata)

    for fm in filemata: 
      fm.insert(0, dir_name)

      data = SendData('push', tmp_data['username'], tmp_data['userkey'], 
                    content=fm)
      try: 
        client = Client(tmp_data['server'])
      except Exception as e:
        print(e)
        sys.exit(2)

      client.send(data.data)
      print('send: ', data.data)
      recv_data = bytes_to_obj(client.recv())
      client.close()
      print('client recved: ', recv_data)
      try: 
        if recv_data['code'] is 0:
          print('Pushing %s ...' % fm[1])
          if fm[2]:
            client1 = Client(tmp_data['server'], DEFAULT_TRANSFER_PORT)
            with open(path+'/'+fm[1], 'rb') as f:
              sd = f.read(BUF_SIZE)
              while sd:
                client1.send(sd)
                sd = f.read(BUF_SIZE)
            client1.close()
          else:
            pass

        else:
          print('Auth failed, re-login with ssgit login')
          sys.exit(1)
      except Exception as e:
        print(e)
        sys.exit(4) 

  def file_mata(self, p, dir_name, l, content=[]):
    ''' content: [dir_name, file_name, chksum] '''
    if p[-1] is '/':
      p = p[:-1]
    try:
      for i in os.listdir(p):
        tmp_name = p + '/' + i
        if os.path.isdir(tmp_name):
          content.append([dir_name, tmp_name[l:], ''])
          self.file_mata(tmp_name, dir_name, l, content=content)
        else:
          content.append([dir_name, tmp_name[l:], md5sum(tmp_name)])
    except Exception as e:
      print(e)

  def listfiles(self, args):
    ''' list server files '''
    if not args:
      args = ['']

    tmp_data = self.get_cache()
    for d in args:
      client = Client(tmp_data['server'])
      data = SendData('list', tmp_data['username'], tmp_data['userkey'], 
                      content=[d])
      client.send(data.data)
      recv_data = bytes_to_obj(client.recv())
      client.close()
      if recv_data['code'] == 0:
        print('Directory name:', d)
        for i in recv_data['content']:
          print(i)
      else:
        print(recv_data['content'][0])

  def pull(self, args):
    ''' pull <dirs on server> '''
    pass
      
  def logout(self, args): 
    ''' logout from server ''' 
    args = None
    tmp_data = self.get_cache()
    client = Client(tmp_data['server'])
    data = SendData('logout', tmp_data['username'], tmp_data['userkey'],)
    client.send(data.data)
    recv_data = bytes_to_obj(client.recv())
    client.close()
    if recv_data['code'] == 0:
      print('Logout from ', tmp_data['server'])
    else:
      print('Failed logout from ', tmp_data['server'])
      sys.exit(2)
    with open(C_CACHE_DIR+'/'+'client', 'wb') as f:
      cache_data = {}
      pickle.dump(cache_data, f)

  def status(self, args):
    ''' print status of args '''
    if not args:
      args = '.'
    else: args = args[0]
    path = os.path.abspath(args)
    dir_name = path.split('/')[-1]

    tmp_data = self.get_cache()
    data = SendData('stat', tmp_data['username'], tmp_data['userkey'],
                     content=[dir_name])

    client = Client(tmp_data['server'])
    client.send(data.data)

    recv_data = bytes_to_obj(client.recv())
    client.close()
#    print('recv_data:', recv_data)
    if recv_data['code'] != 0:
      print(recv_data['content'])
      sys.exit(2)

    else:b = recv_data['content']

    filemata = []
    file_mata(path, len(path)+1, content=filemata)
#    print('filemata:', filemata)
    a = {}
    for fm in filemata:
#      print(fm)
      a[fm[0]] = fm[1]

    diff(a,b)

  def remove(self, args):
    ''' remove files on server '''
    pass

class Client():
  def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=LOGIN_TIMEOUT):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(timeout)
    self.host = host
    self.port = port
    try:
      self.sock.connect((host, port))
    except socket.timeout as e:
      print('Connection timeout.')
      sys.exit(1)

  def send(self, data):
    self.sock.sendall(data)

  def recv(self):
    return self.sock.recv(BUF_SIZE)

  def close(self):
    self.sock.close()

class SendData():
  def __init__(self, request_type, username, userkey, content=[]):
    data = {}
    data['request_type'] = request_type
    data['username'] = username
    data['userkey'] = userkey
    data['content'] = content
    self.data = obj_to_bytes(data)

if __name__ == '__main__':
  main = cmdmain.Main()
  main.execute(Options)
