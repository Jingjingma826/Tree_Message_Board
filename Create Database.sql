-- -----------------------------------------------------
-- Schema Tree
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS tree;
CREATE SCHEMA tree;
USE tree;

/* ----- Create the tables: ----- */

CREATE TABLE IF NOT EXISTS tree.users (
  user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(20) NOT NULL UNIQUE,
  password_hash CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
  email VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  birth_date DATE NOT NULL ,
  location VARCHAR(50) NOT NULL,
  profile_image VARCHAR(255),
  role ENUM('member', 'moderator', 'admin') NOT NULL,
  status ENUM ('active','inactive')NOT NULL
);

CREATE TABLE IF NOT EXISTS tree.messages (
  message_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  FOREIGN KEY (user_id) REFERENCES tree.users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tree.replies (
  reply_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  message_id INT NOT NULL,
  user_id INT NOT NULl,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  FOREIGN KEY (message_id) REFERENCES tree.messages(message_id) ON DELETE CASCADE, 
  FOREIGN KEY (user_id) REFERENCES tree.users(user_id) ON DELETE CASCADE 
);
