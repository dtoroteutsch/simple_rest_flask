import os
import datetime
from peewee import *

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')

if not MYSQL_USER:
    raise ValueError("MYSQL_USER variable is not defined")
if not MYSQL_PASS:
    raise ValueError("MYSQL_PASS variable is not defined")

DATABASE = MySQLDatabase('rest', host='localhost', user=MYSQL_USER, passwd='MYSQL_PASS')

class Course(Model):
    class Meta:
        database = DATABASE

    title = CharField(unique=True, max_length=250)
    description = TextField()
    createdAt = DateTimeField(default=datetime.datetime.now())
