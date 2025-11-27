##### Launching a Hello World app #####
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello world!</p>"


##### Run the app with flask run #####
"""
    Because the name of the app is app.py or in case of wsgi.py
    You can run the app witn the command flask run
"""


##### Escaping HTML characters, this is an example of Cross-Site Scripting (XSS) #####
from flask import request
from markupsafe import escape

@app.route("/hello")
def hello():
    name = request.args.get("name", "Miguel")
    return f"Hello, {name}"
    #return f"Hello, {escape(name)}"
# submit this url /hello?name=<script>alert("This is an example of Cross-Site Scripting (XSS)")</script>


##### Defining multiple routes #####
@app.route("/profile")
def profile():
    return "Profile page"

@app.route("/products")
def products():
    return "Products page"


##### Adding variable sections to URLs #####
#from markupsafe import escape

@app.route("/user/<username>")
def show_user_profile(username):
    # show a profile user with the variable username
    return f"User {escape(username)}"

@app.route("/post/<int:post_id>")
def show_post(post_id):
    # show a especific post with its post_id, the id must be an integer
    return f"Post {post_id}"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    # show the subpath after /path/
    return f"Subpath {escape(subpath)}"


##### trailing slashes does not affect the route #####
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'


##### Building url with url_for #####
from flask import url_for

# @app.route('/')
# def index():
#     return 'index'

@app.route('/login')
def login():
    return 'login'

# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))