import pymysql
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
import time
import sys

DATABASES = {
	'LOCAL':{
		'HOST': 'localhost',
		'USERNAME': 'root',
		'PASSWORD': '',
		'PORT': 3306,
		'NAME': 'db_casetrek'
	}
}