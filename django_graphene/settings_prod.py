import os
from .settings import *


DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')

if DB_NAME and DB_HOST and DB_USER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'HOST': DB_HOST,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'PORT': DB_PORT,
            'OPTIONS': {
                'init_command': 'SET storage_engine=InnoDB',
                'charset': 'utf8',
                'use_unicode': True,
            },
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci',
        }
    }

DEBUG = False
