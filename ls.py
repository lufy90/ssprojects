#!/bin/env python
# ls.py
# list files.


import os, sys




def ls(path):
  try:
    for i in os.listdir(path):
      tmp_path = path + '/' + str(i)
      if os.path.isdir(tmp_path):
        ls(tmp_path)
      else:
        print(tmp_path)
  except OSError as e:
    print(e)

if __name__ == '__main__':
  ls(sys.argv[1])
    
