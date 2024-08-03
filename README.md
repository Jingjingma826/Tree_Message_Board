# Tree Message Board

Welcome to the Tree  Message Board! This web-based forum is designed to help homeowners resolve common disputes related to trees and hedges. Whether it's about overhanging branches, root damage, or blocked views, our platform offers a space for constructive discussions and advice from fellow tree enthusiasts.

## Project Overview

The Tree Message Board is a web application that allows users to:

- Register and Log In/Out: Create an account, log in, log out and manage your profile.
- Post and delete Messages: Share issues or questions about trees and hedges with the community.
- Reply to Messages: Engage in conversations and provide or receive advice.
- Role-Based Access Control: Different roles (Admins, Moderators, Members) with specific permissions to manage content and users.


## Features

Hashing password: All of the passwords have to be hashed when new users register to be a member.

#### User Roles:
There are three user roles in this system:

- Administrator: Can view all users profile, manage all users’ status and roles, and moderate messages and replies.
- Moderator: Can moderate messages and replies, and assist with managing discussions , updating their own profile.
- Member: Can update their own profile, post and delete their own messages, reply to others, and manage their own profile.
- Session Handling: Secure login and logout functionality, ensuring that users' sessions are managed properly.
- Access Control: Role-based permissions to ensure appropriate access levels and actions for different types of users.
- Message Posting and Replying: Users can post new messages, reply to existing ones, and participate in community discussions.

Anyone who registers via the app will be a **Member**. The only way to create
**Staff** or **Admin** accounts in this simple app is to insert them directly
into the database.

## Getting this Example Running

To run the example yourself, you'll need to:

1. Open the project in Visual Studio Code.
2. Create yourself a virtual environment.
3. Install all of the packages listed in requirements.txt (Visual Studio will
   offer to do this for you during step 2).
4. Use the [Database Creation Script](<Create Database.sql>) to create your own
   copy of the **loginexample** database.
5. Use the [Database Population Script](<Populate Database.sql>) to populate
   the **tree_message_board** ***users*** table with example users.
6. Modify [connect.py](treeapp/connect.py) with the connection details for
   your local database server.
7. Run [The Python/Flask application](run.py).

At that point, you should be able to register yourself a new **user** account
or log in using one of the **user**, **staff**, or **admin** accounts listed in
the [Database Population Script](<Populate Database.sql>).

Enjoy!

## Database Scripts

Database:

- [MySQL script to create the necessary database](<Create Database.sql>)
- [MySQL script to populate the database with users](<Populate Database.sql>)
- [Python script to create password hashes](password_hash_generator.py)

## User Passwords:

| Username        | Passwaord   |  Role  |
| :--------  | :-----  | :----:  |
| member1 | member1pass | member |
| member2 | member2pass | member |
| member3 | member3pass | member |
| member4 | member4pass | member |
| member5 | member5pass | member |
| member6 | member6pass | member |
| member7 | member7pass | member |
| member8 | member8pass | member |
| member9 | member9pass | member |
| member10 | member10pass | member |
| member11 | member11pass | member |
| member12 | member12pass | member |
| member13 | member13pass | member |
| member14 | member14pass | member |
| member15 | member15pass | member |
| member16 | member16pass | member |
| member17 | member17pass | member |
| member18 | member18pass | member |
| member19 | member19pass | member |
| member20 | member20pass | member |
| moderator1 | moderator1pass | moderator |
| moderator2 | moderator2pass | moderator |
| moderator3 | moderator3pass | moderator |
| moderator4 | moderator4pass | moderator |
| moderator5 | moderator5pass | moderator |
| admin1 | admin1pass | administrator|
| admin2 | admin2pass | administrator|

## Technology Stack:

- Python
- Flask
- Jinja
- MySQL
- HTML
- Bootstrap
- CSS
- JAVAScript

