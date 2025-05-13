# 📚 Digital Classroom

**Digital Classroom** is a Python desktop application designed to manage coaching classes efficiently. It includes modules for attendance, exams, payments, fees, student, and teacher management.

## 🛠️ Built With

- **Python 3.x**
- **CustomTkinter** – Modern GUI toolkit for Tkinter
- **MySQL** – Relational database backend
- **PIL (Pillow)** – For handling image assets
- **Tkinter** – Standard GUI framework for Python
- **Matplotlib** - For Displaying Report (Exam, Attendance)

## 🔑 Features

- Dashboard with stats: students, teachers, fees, etc.
- Teacher and Student management modules
- Fee tracking, payment records, and due calculations
- Attendance tracking (subject-wise, date-wise)
- Exam scheduling and marks management
- Settings for academic years, classes, subjects, payment modes

## 📁 Project Structure

DigitalClassroom/<br/>
├── main.py # Entry point of the application<br/>
├── admin/ # Admin panel modules<br/>
├── utils/ # Utility scripts (DB connection, helpers)<br/>
├── icons/ # Image resources<br/>
├── database/ # SQL setup files<br/>
└── README.md # Project documentation

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aman-vishwa28/Digital_classroom.git

2. **Set up MySQL database:**
- Create a database (e.g., digital_classroom)
- Table needed (.sql file is not provided)
  
3. **Install dependencies:**
  ```bash
  pip install customtkinter pillow mysql-connector-python
```

4. **Run the application:**
  ```bash
  python main.py
```

## 🧠 Future Enhancements

- AI-powered chatbot for student queries
- Report card generator
- Online exam support with face detectio
- SMS/Email notifications
