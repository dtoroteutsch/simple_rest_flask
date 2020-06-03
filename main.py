from flask import Flask, g, jsonify, abort, request

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

@app.errorhandler(400)
def bad_request(error):
    return jsonify(generate_response(400, error='It is necessary define the parameters'))

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify(generate_response(422, error='Unprocessable entity'))

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

@app.route('/rest/api/v1.0/courses/', methods=['POST'])
def post_course():
    if not request.json:
        abort(400)
    title = request.json.get('title', '')
    description = request.json.get('description', '')
    course = Course.new(title, description)
    if course is None:
        abort(422)
    return jsonify(generate_response(data=course.to_json()))

@app.route('/rest/api/v1.0/courses/<int:course_id>', methods=['PUT'])
def put_course(course_id):
    course = get_course(course_id)
    if not request.json:
        abort(400)
    course.title = request.json.get('title', course.title)
    course.description = request.json.get('description', course.description)
    if course.save():
        return jsonify(generate_response(data=course.to_json()))
    else:
        abort(422)

def get_course(course_id):
    try:
        #select * from courses where courses.id = course_id
        return Course.get(Course.id == course_id)
    except Course.DoesNotExist:
        abort(404)

def generate_response(status=200, data=None, error=None):
    return {
        'status': status,
        'data': data,
        'error': error
        }

if __name__ == '__main__':
    initialize()
    app.run(port=PORT, debug=DEBUG)
