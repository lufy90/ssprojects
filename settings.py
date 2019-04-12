#!/bin/env python36
# settings.py
# 20190329
# ssgit settings.

# Common

DEFAULT_HOST='localhost'
DEFAULT_USER=''
DEFAULT_PORT=8888
DEFAULT_ONLINE_TIME=3600
DEFAULT_TRANSFER_PORT=8889
BUF_SIZE=1024


FSIZE_MAX=1024
DSIZE_MAX=4096

# For client only
LOGIN_TIMEOUT=10
C_CACHE_DIR='./.c_cache'


# For server only

# According DATA_STRUCT to validating a data fragment server received.
DATA_STRUCT = {
#         ''' name, type, max length, if blank is allowed.'''
            ('request_type', str, 16, False),
            ('username', str, 16, False),
            ('userkey', str, 128, False),
            ('content', list, 1024, True),
           }

DATA_DIR = '/tmp/ssgit'
S_CACHE_DIR='.cache'
