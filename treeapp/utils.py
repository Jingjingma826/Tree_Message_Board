# treeapp/utils.py
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



# Function to upload profile image
def upload_image(file, user_id, cursor, db_connection):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('treeapp\static\img', filename)
        file.save(filepath)

        # Update the profile_image field in the database
        cursor.execute('UPDATE users SET profile_image = %s WHERE user_id = %s', (filename, user_id))
        db_connection.commit()
        return 'Profile image updated successfully!'
    return 'Failed to update profile image.'

# Function to remove profile image
def remove_image(user_id, cursor, db_connection):
    cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()
    if result:
        filename = result['profile_image']
        if filename:
            filepath = os.path.join('static/img', filename)
            if os.path.exists(filepath):
                os.remove(filepath)

            # Update the profile_image field in the database
            cursor.execute('UPDATE users SET profile_image = NULL WHERE user_id = %s', (user_id,))
            db_connection.commit()
            return 'Profile image removed successfully!'
    return 'Failed to remove profile image.'

# Function to check if the file type is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
