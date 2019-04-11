#!/bin/env python
# db classes

import sqlite3

class Base_db_operations(object):
  # Copied from django db/backends/base/schema.py
  sql_create_table = "CREATE TABLE %(table)s (%(definition)s)"
  sql_rename_table = "ALTER TABLE %(old_table)s RENAME TO %(new_table)s"
  sql_delete_table = "DROP TABLE %(table)s CASCADE"
  sql_create_column = "ALTER TABLE %(table)s ADD COLUMN %(column)s %(definition)s"
  sql_alter_column = "ALTER TABLE %(table)s %(changes)s"
  sql_alter_column_type = "ALTER COLUMN %(column)s TYPE %(type)s"
  sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s CASCADE"
  sql_rename_column = "ALTER TABLE %(table)s RENAME COLUMN %(old_column)s TO %(new_column)s"

  # By self
  sql_insert_data = "INSERT INTO %(table)s VALUES (%(data)s)"

  def conn(self):
    return None

  def create_tb(self, tb_name, definition):
    conn = self.conn()
    cu = conn.cursor()
    sql = self.sql_create_table % {
      "table": tb_name,
      "definition": definition
    }
    cu.execute(sql)
    conn.commit()
  
  def insert_dt(self, tb, dt):
    conn = self.conn()
    cu = conn.cursor()
    sql = self.sql_insert_data % {
      "table": tb,
      "data": dt
    }
    cu.execute(sql)
    conn.commit()

class Sqlite3(Base_db_operations):
  def __init__(self, path):
    self.path = path

  def conn(self):
    return sqlite3.connect(self.path)

  def create_db(self):
    conn = self.conn()
    conn.commit()




