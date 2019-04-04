#!/bin/env python36
# server.py
# 20190322


import socket, json, socketserver
import sys

from settings import *


BUF_SIZE=1024


class Server(socketserver.TCPServer, socketserver.ForkingMixIn):
  ''' inherite every thin from TCPServer and ForkingMixIn '''
  pass

class LoginServerHandler(socketserver.BaseRequestHandler):
  def handle(self):
    recv_data = self.request.recv(BUF_SIZE)
    data = RequestData(recv_data, self)
    data.response()
    '''
    data = byte_to_obj(recv_data)
    if auth(data):
      self.request.sendall(b'Login OK.')
    else:
      self.request.sendall(b'Authentication Failed')
    '''

class FileTransferHandler(socketserver.StreamRequestHandler):
  def handle(self):
    pass


def byte_to_obj(byte_data):
  return json.loads(byte_data.decode('utf-8'))

def auth(data):
  expect_username = 'test'
  expect_password = 'abc123'
  try:
    if data['request_type'] == 'login':
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
    self.data = byte_to_obj(byte_data)
    self.handler = handler
    self.call_response = {
      'login': self.login,
      'push': self.push,
    }

  def response(self):
    print('recv: ',self.data)
    try:
      self.call_response[self.data['request_type']]()
    except KeyError as e:
      print('Caution: received invalid data.')

  def login(self):
    recv_username = self.data['username']
    if data_valid(self.data) and auth(self.data):
      self.handler.request.sendall(b'Login OK')
      self.handler.request.sendall(b'Ready for recv data')
    else: 
      self.handler.request.sendall(b'Auth Failed')

  def push(self, data):
    pass

def key_gen(time, user, client,  ):
  pass


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', action='store', dest='host', required=False)
  parser.add_argument('--port', action='store', dest='port', type=int, required=False)
  given_args = parser.parse_args()
  HOST = (given_args.host or 'localhost')
  PORT = (given_args.port or DEFAULT_PORT)

  run()
