#!/bin/env python36
# settings.py
# 20190329
# ssgit settings.

DEFAULT_HOST='localhost'
DEFAULT_USER=''
DEFAULT_PORT=8888
DEFAULT_ONLINE_TIME=3600


# For client only
LOGIN_TIMEOUT=10



# For server only

# According DATA_STRUCT to validating a data fragment server received.
DATA_STRUCT = {
#         ''' name, type, max length, if blank is allowed.'''
            ('request_type', str, 16, False),
            ('username', str, 16, False),
            ('userkey', str, 128, False),
            ('content', dict, 1024, True),
           }

