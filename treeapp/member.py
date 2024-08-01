from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
import mysql.connector
from flask_hashing import Hashing
from treeapp import app
from treeapp import connect
from .utils import upload_image, remove_image
hashing = Hashing(app) 
from datetime import datetime

app.secret_key = 'my_secret_key'
PASSWORD_SALT = 'my_secret_key'

DEFAULT_USER_ROLE = 'member'

db_connection = None
def getCursor():

    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect (user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost,  auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    
    return cursor


# Define routes for the home page and login page, accepting both GET and POST requests
@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():  
    msg = '' # Initialize message variable to store feedback for the user
    # Check if the request method is POST and if username and password are in the form data
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        user_password = request.form['password']
        cursor = getCursor()
        cursor.execute('SELECT user_id, username, password_hash, email, first_name, last_name,  birth_date, location, profile_image, role, status from users WHERE username = %s', (username,))
        
        # Check if an account was found
        account = cursor.fetchone()
        if account is not None:
            if account['status'] == 'inactive':
                msg = 'Account is inactive. Please contact support.'
            else:
                password_hash = account['password_hash']
                # Verify the provided password against the stored password hash
                if hashing.check_value(password_hash, user_password, PASSWORD_SALT):
                    # Set session variables to indicate the user is logged in and store user details
                    session['loggedin'] = True
                    session['id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']

                    # Redirect the user based on their role
                    if session['role'] == 'member':
                        return redirect(url_for('member_home'))
                    elif session['role'] == 'moderator':
                        return redirect(url_for('moderator_home'))
                    else:
                        return redirect(url_for('admin_home'))
                else:
                    msg = 'Incorrect password!'
        else:
            msg = 'Incorrect username'

    return render_template('index.html', msg=msg)


# Define route for registration page, accepting both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    # Check if "username", "password", "confirm_password", "email", "first_name", "last_name", "birth_date", and "location" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'confirm_password' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        first_name = request.form.get('first_name')  
        last_name = request.form.get('last_name')   
        birth_date = datetime.strptime(request.form['birth_date'], '%d/%m/%Y')  # Parse birth date
        location = request.form.get('location')  
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        elif password != confirm_password:
            msg = 'Passwords do not match!'
        elif len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            msg = 'Password must be at least 8 characters long and contain both letters and numbers!'
        else:
            # Account doesn't exist and the form data is valid, now insert new account into accounts table
            password_hash = hashing.hash_value(password, PASSWORD_SALT)
            cursor.execute('INSERT INTO users (username, password_hash, email, first_name, last_name,  birth_date, location, role,status) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)',
                           (username, password_hash, email, first_name, last_name,  birth_date, location, DEFAULT_USER_ROLE,'active'))
            db_connection.commit()
            msg = 'You have successfully registered! Please re-login!'
    elif request.method == 'POST': 
        # Form is empty or missing required fields
        msg = 'Please fill out the form!'

    return render_template('register.html',  msg=msg)


@app.route('/member/home')
def member_home():
    if 'loggedin' in session:
        cursor = getCursor()
        # Fetch the first name of the logged-in user from the database
        cursor.execute('SELECT first_name FROM users WHERE user_id = %s', (session['id'],))
        user_info = cursor.fetchone()

        # Retrieve first name from the fetched user information
        first_name = user_info['first_name']
        return render_template('member_home.html', username=session['username'], first_name=first_name, user_role=session['role'],message='')
    
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    cursor = getCursor()
    msg = request.args.get('msg', '')    
    user_id = session['id']
    is_admin = session.get('role') == 'admin'
    user_to_edit_id = request.args.get('user_id') if is_admin and request.args.get('user_id') else user_id

    if request.method == 'POST':
        if is_admin and user_to_edit_id != user_id:
            # Administrators can update user roles and status
            if 'role' in request.form and 'status' in request.form:
                role = request.form['role']
                status = request.form['status']
                cursor.execute('UPDATE users SET role = %s, status = %s WHERE user_id = %s', (role, status, user_to_edit_id))
                db_connection.commit()
                msg = 'Role and status updated successfully!'
                return redirect(url_for('profile', user_id=user_to_edit_id, msg=msg))
        else:
            # Users can update their own personal information
            if 'email' in request.form:
                email = request.form['email']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                birth_date = datetime.strptime(request.form['birth_date'], '%d/%m/%Y')
                location = request.form['location']
                cursor.execute('''
                    UPDATE users 
                    SET email = %s, first_name = %s, last_name = %s, birth_date = %s, location = %s
                    WHERE user_id = %s
                ''', (email, first_name, last_name, birth_date, location, user_id))
                db_connection.commit()
                msg = 'Profile updated successfully!'
            elif 'new_password' in request.form:
                # update passward
                new_password = request.form['new_password']
                confirm_new_password = request.form['confirm_new_password']
                if new_password != confirm_new_password:
                    msg = 'Passwords do not match!'
                else:
                    cursor.execute('SELECT password_hash FROM users WHERE user_id = %s', (user_id,))
                    account = cursor.fetchone()
                    current_password_hash = account['password_hash']
                    if hashing.check_value(current_password_hash, new_password, PASSWORD_SALT):
                        msg = 'New password must be different from the current password!'
                    elif len(new_password) < 8 or not re.search(r'[A-Za-z]', new_password) or not re.search(r'[0-9]', new_password):
                        msg = 'Password must be at least 8 characters long and contain both letters and numbers!'
                    else:
                        new_password_hash = hashing.hash_value(new_password, PASSWORD_SALT)
                        cursor.execute('''
                            UPDATE users 
                            SET password_hash = %s
                            WHERE user_id = %s
                        ''', (new_password_hash, user_id))
                        db_connection.commit()
                        msg = 'Password updated successfully!'
    # Fetch the user's profile information
    cursor.execute('SELECT username, password_hash, email, first_name, last_name, birth_date, location, profile_image, role, status FROM users WHERE user_id = %s', (user_to_edit_id,))
    account = cursor.fetchone()
    # Convert birth date to string format for display
    if account and account['birth_date']:
        birth_date_str = account['birth_date'].strftime('%d/%m/%Y')
        account['birth_date'] = birth_date_str
    return render_template('profile.html', account=account, username=session['username'], user_role=session['role'], msg=msg, is_admin=is_admin, user_to_edit_id=user_to_edit_id)


@app.route('/replace_profile_image', methods=['POST'])
def replace_profile_image():
    if 'loggedin' in session: 
        # Check if user has a valid role (admin, moderator, or member)
        if session['role'] in ['admin', 'moderator', 'member']:        
            # Get the uploaded file from the request
            file = request.files['profile_image']
            # Call the function to upload the image and update profile
            msg = upload_image(file, session['id'], getCursor(), db_connection)
        # Redirect to the profile page with a message
        return redirect(url_for('profile', msg=msg))
    return redirect(url_for('login'))

@app.route('/remove_profile_image', methods=['POST'])
def remove_profile_image():
    if 'loggedin' in session: 
        if session['role'] in ['admin', 'moderator', 'member']:        
            msg = remove_image(session['id'], getCursor(), db_connection)
        return redirect(url_for('profile', msg=msg))
    return redirect(url_for('login'))


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'loggedin' in session:
        cursor = getCursor()
        msg = request.args.get('msg', '')

        if request.method == 'POST':
            if 'message_content' in request.form:
                # Posting a new message
                message_content = request.form['message_content']
                user_id = session['id']
                if message_content:
                    cursor.execute('''
                        INSERT INTO messages (user_id, title, content, created_at) 
                        VALUES (%s, %s, %s, NOW())
                    ''', (user_id, 'New Message Title', message_content))
                    db_connection.commit()
                    msg = 'Post new message successfully!'
            elif 'reply_content' in request.form and 'message_id' in request.form:
                # Posting a reply
                message_id = request.form['message_id']
                reply_content = request.form['reply_content']
                cursor.execute('INSERT INTO replies (user_id, message_id, content, created_at) VALUES (%s, %s, %s, NOW())', (session['id'], message_id, reply_content))
                db_connection.commit()
                msg = 'Reply posted successfully!'
            # return redirect(url_for('messages', msg=msg))

        # Get all messages
        cursor.execute('''
            SELECT m.message_id, m.user_id, m.title, m.content, m.created_at, u.username
            FROM messages m
            JOIN users u ON m.user_id = u.user_id
        ''')
        messages = cursor.fetchall()
        
        # Get all replies
        cursor.execute('''
            SELECT r.reply_id, r.message_id, r.user_id, r.content, r.created_at, u.username
            FROM replies r
            JOIN users u ON r.user_id = u.user_id
            ORDER BY r.created_at ASC
        ''')
        replies = cursor.fetchall()
        return render_template('messages.html', messages=messages, replies=replies, user_role=session['role'], msg=msg)
    return redirect(url_for('login'))


@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if 'loggedin' in session:
        cursor = getCursor()

        # Delete the message with the given message_id
        cursor.execute('DELETE FROM messages WHERE message_id = %s', (message_id,))
        # Delete all replies associated with the deleted message
        cursor.execute('DELETE FROM replies WHERE message_id = %s', (message_id,))

        db_connection.commit()
        msg = 'Message deleted successfully!'
        return redirect(url_for('messages', msg=msg))
    return redirect(url_for('login'))

@app.route('/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply(reply_id):
    if 'loggedin' in session:
        cursor = getCursor()

        # Delete the reply with the given reply_id
        cursor.execute('DELETE FROM replies WHERE reply_id = %s', (reply_id,))

        db_connection.commit()
        msg = 'Reply deleted successfully!'
        return redirect(url_for('messages', msg=msg))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
   session.pop('loggedin', None) # Remove 'loggedin' key from session to log the user out
   session.pop('id', None) # Remove 'id' key from session to clear user ID
   session.pop('username', None) # Remove 'username' key from session to clear username
   return redirect(url_for('login')) # Redirect the user to the login page after logging 

if __name__ == '__main__':
    app.run(debug=True)