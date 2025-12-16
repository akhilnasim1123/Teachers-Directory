# Teacher Directory 🎓

A modern, responsive web application built with **Django** for efficiently managing teacher profiles. Designed with a clean UI, robust authentication, and intuitive data management features.

![Teacher Directory Dashboard](https://via.placeholder.com/800x400?text=Teacher+Directory+Dashboard)

## 🚀 Features

*   **Teacher Management**: Browse, search, add, edit, and delete teacher profiles.
*   **Bulk Import**: Upload teachers via CSV (supports `,` and `|` separators) with a preview step.
*   **Dynamic Subjects**: Tag teachers with subjects instantly during creation or editing.
*   **Secure Authentication**: Role-based access with secure login and logout flows.
*   **Interactive UI**: Modern interface with Modals for smoother interactions (Edit, Delete, Logout).
*   **Responsive Design**: Built with a custom CSS system for desktop and mobile.

## 🛠️ Tech Stack

*   **Backend**: Python, Django 3.2+
*   **Database**: SQLite (Default) / MySQL (Production ready)
*   **Frontend**: HTML5, CSS3 (Custom Grid/Flexbox), JavaScript (Vanilla)

## 📦 Installation
Follow these steps to set up the project locally.

### Prerequisites
*   Python 3.8 or higher
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/akhilnasim1123/Teachers-Directory.git
cd Teachers-Directory
```

### 2. Set Up Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Apply migrations to create the database schema.
```bash
python manage.py migrate
```

### 5. Create a Superuser
To access the admin panel and system, create a superuser account.
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 6. Run the Server
Start the development server.
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## 🔑 Usage

### Administrator Access
*   **Login**: Access the system using the superuser credentials you created.

### Importing Data
Navigate to **Import Teachers** in the sidebar. You can upload a CSV file with the following column order:
1.  First Name
2.  Last Name
3.  Profile Image Filename
4.  Email Address
5.  Phone Number
6.  Room Number
7.  Subjects (separated by `,` or `|`)

