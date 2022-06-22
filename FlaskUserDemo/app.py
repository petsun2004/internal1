import uuid, os, hashlib
from flask import Flask, request, render_template, redirect, session, abort, flash
app = Flask(__name__)

# Register the setup page and import create_connection()
from utils import create_connection, setup
app.register_blueprint(setup)

# my first home page which is my login page
@app.route('/')
def home():
    return render_template("login.html")

# backend for my login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM user_infor WHERE email=%s AND password=%s"
                values = (
                    request.form['email'],
                    encrypted_password
                )
                cursor.execute(sql, values)
                result = cursor.fetchone()
        if result:
            session['logged_in'] = True
            session['first_name'] = result['first_name']
            session['role'] = result['role']
            session['user_id'] = result['user_id']
            return redirect("/dashboard")
        else:
            flash("Invalid username or password.")
            return redirect("/login")
    else:
        return render_template('login.html')


if __name__ == '__main__':
    import os

    # This is required to allow sessions.
    app.secret_key = os.urandom(32)

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)


