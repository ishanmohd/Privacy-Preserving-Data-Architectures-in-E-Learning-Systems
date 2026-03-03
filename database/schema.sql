create database elearning_privacy;
use elearning_privacy;

CREATE TABLE users_identity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARBINARY(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    mfa_secret VARCHAR(64) NOT NULL
);

CREATE TABLE user_mapping (
    user_id INT PRIMARY KEY,
    pseudo_id VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_identity(id)
        ON DELETE CASCADE
);

CREATE TABLE learning_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pseudo_id VARCHAR(100),
    course VARCHAR(100),
    score INT
);

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO learning_data (pseudo_id, course, score)
VALUES
('test1', 'Math', 85),
('test2', 'Math', 90),
('test3', 'CS', 78),
('test4', 'CS', 82);

select * from learning_data;

CREATE TABLE quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pseudo_id VARCHAR(100),
    quiz_name VARCHAR(100),
    answers TEXT,
    score INT,
    evaluated BOOLEAN DEFAULT FALSE
);

CREATE TABLE doubts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pseudo_id VARCHAR(100),
    question TEXT,
    reply TEXT
);
