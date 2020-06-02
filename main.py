from flask import Flask

app = Flask(__name__)
PORT = 9000
DEBUG = True

@app.route('/rest/api/v1.0/courses', methods=['GET'])
def get_courses():
    return '<h2>Hello World</h2>'

if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)
