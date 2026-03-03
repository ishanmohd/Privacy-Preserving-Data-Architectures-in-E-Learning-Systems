# 🔐 Privacy Preserving Data Architectures in E-Learning Systems

A secure, role-based E-Learning web application designed with privacy-preserving mechanisms including encryption, pseudonymization, and differential privacy analytics.

This project demonstrates secure data architecture practices applied to educational platforms.

---

## 📖 Project Overview

This system implements a privacy-focused E-Learning platform where:

- Students can securely submit assignments, quizzes, and doubts.
- Instructors can evaluate and manage academic content.
- Admin can monitor privacy-safe analytics.
- Sensitive data is encrypted and protected at rest.

The platform emphasizes secure data handling and privacy-preserving techniques.

---

## 🚀 Key Features

### 👨‍🎓 Student Module
- Secure login (JWT-based authentication)
- Submit encrypted assignments
- Submit quizzes
- Raise academic doubts
- View quiz scores
- View graded assignments
- Access study posts & video lectures
- Download password-protected PDFs

---

### 👩‍🏫 Instructor Module
- View quiz submissions
- Evaluate quizzes
- View and reply to doubts
- Grade assignments
- Upload password-protected study PDFs
- Create study posts with optional video lectures

---

### 👨‍💼 Admin Module
- Privacy-safe analytics dashboard
- Differential privacy applied to average scores
- Monitor:
  - Total quizzes
  - Doubts
  - Study posts
  - Video lectures
  - Assignments uploaded & graded
  - Active learners
  - Course-wise engagement

---

## 🔒 Privacy & Security Mechanisms

- JWT-based Authentication
- Role-Based Access Control (RBAC)
- Pseudonym Mapping (User anonymization)
- File Encryption using Fernet (AES-based symmetric encryption)
- Password-protected PDFs
- Differential Privacy for analytics
- Secure file storage (encrypted at rest)
- Optional simulated secure payment module (HMAC-based)

---

## 🏗️ System Architecture

Frontend (HTML, CSS, JS)  
        ↓  
Flask Backend (REST APIs)  
        ↓  
MySQL Database  
        ↓  
Encryption Layer (Fernet)  
        ↓  
Privacy & Analytics Module  

---

## 🛠️ Tech Stack

Backend:
- Python
- Flask
- Flask-JWT-Extended
- Flask-CORS

Database:
- MySQL

Security & Encryption:
- Cryptography (Fernet)
- PyPDF (Password-protected PDFs)
- HMAC (Optional simulated payments)

Frontend:
- HTML
- CSS
- JavaScript
- Chart.js (Analytics visualization)

---

## 🗄️ Database Tables

- users
- user_mapping (pseudonymization)
- quizzes
- doubts
- assignments
- study_posts
- learning_data

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/privacy-preserving-elearning-system.git
cd privacy-preserving-elearning-system
