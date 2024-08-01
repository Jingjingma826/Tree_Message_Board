from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from treeapp import app
from treeapp import connect
import mysql.connector

db_connection = None
def getCursor():
    global db_connection


    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect (user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost,  auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    
    return cursor

@app.route('/moderator/home')
def moderator_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = getCursor()
        # Retrieve the first name of the logged-in user from the database
        cursor.execute('SELECT first_name FROM users WHERE user_id = %s', (session['id'],))
        user_info = cursor.fetchone()
        # Extract the first name from the query result
        first_name = user_info['first_name']
        # Render the moderator's home page with the user's username, first name, and role
        return render_template('moderator_home.html', username=session['username'], first_name=first_name, user_role=session['role'])
    
    
    # If the user is not logged in, redirect them to the login page    
    return redirect(url_for('login'))










