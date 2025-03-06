-- Starting up database
CREATE DATABASE easybook;
USE easybook;

-- Making admin account
INSERT INTO users (name, email, password, permission) 
VALUES ('admin', 'admin@gmail.com', 'admin', 'admin');

-- Creating users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    permission ENUM('customer', 'employee', 'admin') NOT NULL
);

-- Useful commands
SELECT * FROM users;
