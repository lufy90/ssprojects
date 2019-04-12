#!/bin/env python36
# user.py
# 20190403

from settings import DATA_DIR 
import os
from database import Sqlite3

class User():
  def __init__(self, name):
    self.name = name
    self.root_dir = DATA_DIR + '/' + self.name

  def create(self, password):
    os.mkdir(self.root)

  def auth(self, data):
    pass

 
