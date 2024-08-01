from collections import namedtuple
from flask import Flask
from flask_hashing import Hashing
import mysql.connector

PASSWORD_SALT = 'my_secret_key'
UserAccount = namedtuple('UserAccount', ['user_id','username', 'password_hash'])

app = Flask(__name__)
hashing = Hashing(app)

db_config = {
    'user': 'root',
    'password': 'Mjj19840318@',
    'host': 'localhost',
    'database': 'tree',
    'auth_plugin': 'mysql_native_password'
}

# Establish the database connection
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor(dictionary=True)  # Use dictionary cursor to get column names

# Fetch the users from the database
cursor.execute("SELECT user_id, username, password_hash FROM users")
users = cursor.fetchall()

for user in users:
    # Hash the user's password
    password_hash = hashing.hash_value(user['password_hash'], PASSWORD_SALT)
    
    # Update the user's password in the database
    cursor.execute(
        "UPDATE users SET password_hash = %s WHERE user_id = %s",
        (password_hash, user['user_id'])
    )

db_connection.commit()

cursor.close()
db_connection.close()