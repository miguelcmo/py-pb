from flask import Flask
from flask import request

app = Flask(__name__)

def do_the_login():
    return "Logged-in user!"

def show_the_login_form():
    return """
        <form method="POST" action="/login">
            <label>Username:</label>
            <input type="text" name="username"><br>
            <label>Password:</label>
            <input type="password" name="password">
            <br>
            <button type="submit">Login</button>
        </form>
        """

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
    
# its posible to separate methods in different function using a decorator for each method
# @app.get('/login')
# def login_get():
#     return show_the_login_form()

# @app.post('/login')
# def login_post():
#     return do_the_login()