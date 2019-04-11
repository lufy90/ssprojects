#!/bin/env python36
# lib.py
# 20190408

import json
import hashlib
import sys
import os

def bytes_to_obj(byte_data):
  return json.loads(byte_data.decode('utf-8'))

def obj_to_bytes(obj):
  return bytes(json.dumps(obj), encoding='utf-8')

def md5sum(src):
  ha = hashlib.md5()
  with open(src, 'rb') as f:
    for chunck in iter(lambda: f.read(2048), b''):
      ha.update(chunck)

  return ha.hexdigest()

def get_dir_name(d):
  return os.path.abspath(d).split('/')[-1]


def ls(p='.'):
  if p[-1] is '/':
    p = p[:-1]
  try:
    for i in os.listdir(p):
      if os.path.isdir(p + '/' + i):
        ls(p + '/' + i)
      else: print(p+'/'+i)
  except Exception as e:
    print(e)


def test():
  print(md5sum(sys.argv[1]))



if __name__ == '__main__':
  test()
