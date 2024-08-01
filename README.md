# Tree_Message_Board
COMP639 Individual Assignment Semester 2 2024

Tree Message Board

Welcome to the Tree Talk Message Board! This web-based forum is designed to help homeowners resolve common disputes related to trees and hedges. Whether it's about overhanging branches, root damage, or blocked views, our platform offers a space for constructive discussions and advice from fellow tree enthusiasts.

Project Overview

The Tree Talk Message Board is a web application that allows users to:
Register and Log In/Out: Create an account, log in, log out and manage your profile.
Post and Messages: Share issues or questions about trees and hedges with the community.
Reply to Messages: Engage in conversations and provide or receive advice, delete replies.
Role-Based Access Control: Different roles (Admins, Moderators, Members) with specific permissions to manage content and users.

Features

Hashing password: All of the passwords have to be hashed when new users register to be a member.
User Roles:
Admin: Can view all users profile, manage all users’ status and roles, and moderate messages and replies.
Moderator: Can moderate messages and replies, and assist with managing discussions , updating their own profile.
Member: Can update their own profile, post and delete their own messages, reply to others, and manage their own profile.
Session Handling: Secure login and logout functionality, ensuring that users' sessions are managed properly.
Access Control: Role-based permissions to ensure appropriate access levels and actions for different types of users.
Message Posting and Replying: Users can post new messages, reply to existing ones, and participate in community discussions.

Getting Started
To get started with the Tree Talk Message Board:
Clone the Repository:
git clone https://github.com/Jingjingma826/tree_message_board.git

Navigate to the Project Directory:
cd tree_message_board

Install Dependencies:
pip install -r requirements.txt

Run the Application:
python run.py

Visit the Application: Open your web browser and go to http://127.0.0.1:5000/ to access the Tree Talk Message Board.

Login password: Inorder to make it’s simpler to login, all of the password look like as below:

Users=[ UserAccount('member1', 'member1pass')...
        UserAccount('moderator1', 'moderator1pass')...
        UserAccount('admin1', 'admin1pass')...]

Contributing

We welcome contributions to improve the Tree Talk Message Board! Please follow these steps to contribute:
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

Contact
For any questions or feedback, please reach out to crystal.ma@lincolnuni.ac.nz
