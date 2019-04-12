#!/bin/env python36
# server.py
# 20190322


import socket, json, socketserver
import sys, os
import pickle

from lib import bytes_to_obj, obj_to_bytes, md5sum
from settings import *
from user import User



class Server(socketserver.TCPServer, socketserver.ForkingMixIn):
  ''' inherite every thin from TCPServer and ForkingMixIn '''
  pass

class LoginServerHandler(socketserver.BaseRequestHandler):
  def handle(self):
    recv_data = self.request.recv(BUF_SIZE)
    data = RequestData(recv_data, self)
    data.response()
    '''
    data = bytes_to_obj(recv_data)
    if auth(data):
      self.request.sendall(b'Login OK.')
    else:
      self.request.sendall(b'Authentication Failed')
    '''

class FileTransferHandler(socketserver.StreamRequestHandler):
  def handle(self):
    self.data = self.rfile.readline().strip()
    
    pass

def auth(data):
  expect_username = 'test'
  expect_password = 'abc123'
  try:
    recv_username = data['username']
    recv_pasword = data['userkey']
    if (recv_username, recv_pasword) == (expect_username, expect_password):
      return True
    else:
      return False
  except KeyError as e:
    return False
    print(e)

def data_valid(recv_data, exp_data=DATA_STRUCT):
  try:
    cout = 0
    for i in exp_data:
      if (type(recv_data[i[0]]) is i[1]) and \
         (len(recv_data[i[0]]) <= i[2]) and \
         (recv_data[i[0]] or i[3]):
        cout += 1
    if cout == len(exp_data):
      return True
    else:
      return False
  except KeyError as e:
    return False

 
def run():
  with Server((HOST, PORT), LoginServerHandler) as server:
    print('Listening on (%s,%s)' % (HOST,PORT))
    server.serve_forever()

class RequestData():
  ''' resolve incoming data and make response.'''
  def __init__(self, byte_data, handler):
    self.data = bytes_to_obj(byte_data)
    self.user = User(self.data['username'])
    self.handler = handler
    self.call_response = {
      'login': self.login,
      'push': self.push,
      'list': self.listfiles,
      'logout': self.logout,
      'stat': self.status,
    }

  def response(self):
    print('recv: ',self.data)
    if data_valid(self.data) and auth(self.data):
      self.call_response[self.data['request_type']]()
    else:
      code, key = 1, None
      sendbackdata = {'code':code, 'userkey': key}
      self.handler.request.sendall(obj_to_bytes(sendbackdata))

  def login(self):
    code, key = 0, key_gen()
    sendbackdata = {'code':code, 'content': key}
    self.handler.request.sendall(obj_to_bytes(sendbackdata))

  def push(self):
    code = 0
    sendbackdata = {'code':code}
    try:
      dir_name = self.data['content'][0]
      file_name = self.data['content'][1]
      file_md5sum = self.data['content'][2]
    except IndexError as e:
      print(e)
      print('Reseive bad push data')
      sys.exit(4)
    data_dir = self.user.root_dir + '/' + dir_name
    cache_dir = data_dir + '/' + S_CACHE_DIR

    if not os.path.exists(data_dir):
      os.mkdir(data_dir)
      os.mkdir(cache_dir)   # cache file.
      with open(cache_dir + '/' + 'meta', 'wb') as f:
        pickle.dump({}, f)

    full_file_name = data_dir + '/' + file_name
    if not file_md5sum:    # file_md5sum = '', get a directory.
      self.handler.request.sendall(obj_to_bytes(sendbackdata))
      print('Get dir: %s' % file_name)
      try:
        os.mkdir(full_file_name)
        print('Transfer OK: ', file_name)
      except Exception as e:
        print(e)
        print('Transfer failed: ', file_name)
    else:
      print('Get file: %s' % file_name)
      try:
        transfer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transfer_sock.bind((DEFAULT_HOST, DEFAULT_TRANSFER_PORT))
        transfer_sock.listen(1)
        self.handler.request.sendall(obj_to_bytes(sendbackdata))
        conn, addr = transfer_sock.accept()
      except socket.error as e:
        print(e)
      with open(full_file_name, 'wb') as f:
        while True:
          trsf_data = conn.recv(BUF_SIZE)
          if not trsf_data:
            break
          f.write(trsf_data)
        conn.close()
        print('file wrote: ', full_file_name)
      transfer_sock.close()

    try:
      if md5sum(full_file_name) == file_md5sum:
        print('Transfer OK: ', file_name)
        # sendback OK.
        with open(cache_dir + '/' + 'meta', 'rb') as f:
          file_meta = pickle.load(f)

        file_meta[file_name] = file_md5sum

        with open(cache_dir + '/' + 'meta', 'wb') as f:
          pickle.dump(file_meta, f)
      else:
        print('Transfer failed: ', file_name)
    except os.error as e:
      print('Transfer failed: ', file_name)
      print(e)
        
  def listfiles(self):
    code = 0
    dir_name = self.data['content'][0]

    full_dir_name = self.user.root_dir + '/' + dir_name
    try:
      send_back_content = os.listdir(full_dir_name)
    except os.error as e:
      code = 1
      send_back_content = [str(e)]
     
    sendbackdata = {'code':code, 'content': send_back_content}
    self.handler.request.sendall(obj_to_bytes(sendbackdata))

  def logout(self):
    code = 0
    send_back_content = None
    sendbackdata = {'code':code, 'content': send_back_content}
    self.handler.request.sendall(obj_to_bytes(sendbackdata))

  def status(self):
    #code = 0
    dir_name = self.data['content'][0]
    data_dir = self.user.root_dir + '/' + dir_name
    if not os.path.exists(data_dir):
      code = 1
      file_meta = None
    else:
      cache_dir = data_dir + '/' + S_CACHE_DIR
      with open(cache_dir + '/' + 'meta', 'rb') as f:
        file_meta = pickle.load(f)
    sendbackdata = {'code':code, 'content':file_meta}
    self.handler.request.sendall(obj_to_bytes(sendbackdata))


def key_gen():
  return 'abc123'


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', action='store', dest='host', required=False)
  parser.add_argument('--port', action='store', dest='port', type=int, required=False)
  given_args = parser.parse_args()
  HOST = (given_args.host or 'localhost')
  PORT = (given_args.port or DEFAULT_PORT)
  try:
    run()

  except Exception as e:
    print(e)
    sys.exit(0)
