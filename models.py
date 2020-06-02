import os
import datetime
from peewee import *

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')

if not MYSQL_USER:
    raise ValueError("MYSQL_USER variable is not defined")
if not MYSQL_PASS:
    raise ValueError("MYSQL_PASS variable is not defined")

DATABASE = MySQLDatabase('rest', host='localhost', user=MYSQL_USER, passwd=MYSQL_PASS)

class Course(Model):
    class Meta:
        database = DATABASE
        db_table = 'courses'

    title = CharField(unique=True, max_length=250)
    description = TextField()
    createdAt = DateTimeField(default=datetime.datetime.now())

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
            }

def create_course():
    title = 'Flask Course'
    description = 'Free flask course'

    #select * from courses where courses.title = $title
    if not Course.select().where(Course.title == title):
        Course.create(title=title, description=description)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Course], safe=True)
    create_course()
    DATABASE.close()
