from flask import Flask, g, jsonify

from models import initialize
from models import Course
from models import DATABASE

app = Flask(__name__)
PORT = 9000
DEBUG = True

#opening the database connection
@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()

#closing the database connection
@app.after_request
def after_request(request):
    g.db.close()
    return request

@app.route('/rest/api/v1.0/courses', methods=['GET'])
def get_courses():
    #select * from courses;
    courses = Course.select()
    courses = [course.to_json() for course in courses]
    return jsonify(courses)

if __name__ == '__main__':
    initialize()
    app.run(port=PORT, debug=DEBUG)
