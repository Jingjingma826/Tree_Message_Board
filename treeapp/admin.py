from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from treeapp import app
from treeapp import connect
import mysql.connector
from datetime import datetime

db_connection = None
def getCursor():
    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect (user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost,  auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    
    return cursor

@app.route('/admin/home')
def admin_home():
    # Check if user is logged in
    if 'loggedin' in session:
        if session['role'] == 'admin':
            cursor = getCursor()
            cursor.execute('SELECT first_name FROM users WHERE user_id = %s', (session['id'],))
            user_info = cursor.fetchone()
            
            first_name = user_info['first_name']
            # User is logged in, show them the home page and role is admin
            return render_template('admin_home.html', username=session['username'], user_role=session['role'], first_name=first_name)
        else:
            return render_template('error.html', user_role=session['role'])
        
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = getCursor()
        # Handle POST requests for searching users
        if request.method == 'POST':
            search_term = request.form['search_term']
            search_query = '''
                SELECT user_id, username, first_name, last_name, email 
                FROM users 
                WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s
            '''
            # Execute the search query with the provided search term
            cursor.execute(search_query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        else:
            # Handle GET requests for displaying all users
            cursor.execute('SELECT user_id, username, first_name, last_name, email FROM users')
        users = cursor.fetchall()

        # Render the 'manage_users.html' template with the users data and user role
        return render_template('manage_users.html', users=users,user_role=session['role'])
    
    # Redirect to the login page if the user is not logged in or not an admin
    return redirect(url_for('login'))

@app.route('/admin/user_profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    # Check if the user is logged in and has an admin role
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = getCursor()
        msg = ''

        # Handle POST requests for updating user profile
        if request.method == 'POST':
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            birth_date = datetime.strptime(request.form['birth_date'], '%d/%m/%Y') # Parse birth date
            location = request.form['location']
            role = request.form['role']  
            status = request.form['status']  

            # Update the user's profile information in the database
            cursor.execute('''
                UPDATE users
                SET email = %s, first_name = %s, last_name = %s, birth_date = %s, location = %s
                WHERE user_id = %s
            ''', (email, first_name, last_name, birth_date, location,  role, status, user_id))
            db_connection.commit()
            msg = 'Profile updated successfully!'

        # Retrieve the user's current profile information
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        account = cursor.fetchone()

        # Format birth date to a string if it exists
        if account and account['birth_date']:
            birth_date_str = account['birth_date'].strftime('%d/%m/%Y')
            account['birth_date'] = birth_date_str

        # Render the profile page with the user's information and status message
        return render_template('profile.html', account=account, username=session['username'], user_role=session['role'], msg=msg, is_admin=True)
    
    # Redirect to the login page if the user is not logged in or not an admin
    return redirect(url_for('login'))

