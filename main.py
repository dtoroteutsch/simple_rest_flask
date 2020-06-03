from flask import Flask, g, jsonify, abort

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

@app.errorhandler(404)
def not_found(error):
    return jsonify(generate_response(404, error='Resource not found'))

@app.route('/rest/api/v1.0/courses', methods=['GET'])
def get_courses():
    #select * from courses;
    courses = Course.select()
    courses = [course.to_json() for course in courses]
    return jsonify(generate_response(data=courses))

@app.route('/rest/api/v1.0/courses/<int:course_id>', methods=['GET'])
def show_course(course_id):
    course = get_course(course_id)
    return jsonify(generate_response(data=course.to_json()))

def get_course(course_id):
    try:
        #select * from courses where courses.id = course_id
        return Course.get(Course.id == course_id)
    except Course.DoesNotExist:
        abort(404)

def generate_response(status=200, data=None, error=None):
    return {
        'status': 200,
        'data': data,
        'error': error
        }

if __name__ == '__main__':
    initialize()
    app.run(port=PORT, debug=DEBUG)
