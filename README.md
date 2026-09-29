# Student Grade Management System
A CLI application to manange academic records and data created with the help of Python and MySQL.

## Features
- Add Students on the basis of Registration Number and attendence
- Add marks for CAT-1, CAT-2, Term End and Practicals respectivily
- Calculate weighted CGPA using VIT grading formula
- Check debarred students (attendance below 75%)
- Search, update and delete student recodrs as per the entered exam category

## Requirements
- Python 3.x
- MySQL 8.0
- pip

## Setup Instructions
 
### Step 1 - Clone the repository 
git clone https://github.com/verma-daksh/grade-manager
cd grade-manager

### Step 2 - Install dependencies
pip install pymysql python-dotenv

### Step 3 - Setup MySQL
- Open MySQL and create a database :
'''sql
CREATE DATABASE project1;
'''
### step 4 - Create .env file
Create a fie named ' .env' in the project 
folder with :
DB_HOST=localhost 
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=project1

### Step 5 - Run the program
python main.py


## Project Structure
grade-manager/
├── main.py # Main program with menu
├── database.py # All database functions
├── .env # credentials (not pushed to GitHub)
└── README.md

## Tech Stack
- Python 3
- MySQL 8.0
- PyMySQL
- python-dotenv

