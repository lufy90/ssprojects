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
  if os.path.isdir(src):
    return ''
  else:
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

def diff(a, b):
  '''a = {f_name1: md5sum1, f_name2:md5sum2}, b = [(1,1),(2,2),(5,5)]'''
  re = []
  ak = list(a.keys())
  bk = list(b.keys())
  for i in ak:
    if (i in bk) and (a[i] == b[i]):
      bk.remove(i)
      pass
    elif (i in bk):
      bk.remove(i)
      print('%-10s %s' % ('Modified:', i))
    else:
      print('%-10s %s' % ('New:', i))

  for j in bk:
    print('%-10s %s' % ('Deleted:', j))

def file_mata(p, l, content=[]):
  ''' content: [file_name, chksum] '''
  if p[-1] is '/':
    p = p[:-1]
  try:
    for i in os.listdir(p):
      tmp_name = p + '/' + i
      if os.path.isdir(tmp_name):
        content.append([tmp_name[l:], ''])
        file_mata(tmp_name, l, content=content)
      else:
        content.append([tmp_name[l:], md5sum(tmp_name)])
  except Exception as e:
    print(e)
 


def test():
  a,b = {}, {}
  for i in os.listdir(sys.argv[1]):
    try:
      a[i] = md5sum(sys.argv[1] + '/' +i)
    except os.error as e:
#      print(e)
      a[i] = ''
#  print('a:',a)

  for j in os.listdir(sys.argv[2]):
    try:
      b[j] = md5sum(sys.argv[2] + '/' +j)
    except os.error as e:
#      print(e)
      b[j] = ''
#  print('b:',b)

  diff(a,b)

if __name__ == '__main__':
  test()
