Teacher Directory Project
=========================

Overview
--------
The Teacher Directory is a web application built with Django for managing teacher profiles. 
It allows administrators to list, view, add, edit, and delete teachers. 
Key features include:
- Secure Authentication
- Bulk Import via CSV (supporting comma and pipe separators)
- Dynamic "Add Subject" functionality
- Responsive and Modern UI with Modals

Prerequisites
-------------
- Python 3.8+
- Django 3.2+
- Pillow (for image handling)
- django-environ

Setup Instructions
------------------
1. **Environment Setup**
    Ensure you have Python installed. It is recommended to work in a virtual environment.
    
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

2. **Install Dependencies**
    
    pip install -r requirements.txt

    (If requirements.txt is missing, install manually: pip install django pillow django-environ)

3. **Database Setup**
    Apply the database migrations to set up the schema.
    
    python manage.py migrate

4. **Run the Server**
    Start the development server.
    
    python manage.py runserver

    Acccess the application at: http://127.0.0.1:8000/

Usage Guidelines
----------------

### Login
- Use your administrator credentials to log in.
- Default for demo: username `admin`, password `admin`.

### Dashboard / Directory
- View all teachers in a clean card layout.
- Use the sidebar (or top nav on mobile) to navigate.

### Teacher Management
- **Add Teacher**: Click "Add Teacher" in the directory header.
- **Import Teachers**: Use the "Import Teachers" link in the sidebar to upload a CSV file.
    - Supported columns: First Name, Last Name, Profile picture, Email Address, Phone Number, Room Number, Subjects taught.
    - Subjects can be separated by commas (,) or pipes (|).
- **Edit/Delete**: Click on a teacher card to view details. Use the "Edit Profile" or "Delete" buttons. Actions are confirmed via modals.

### Logout
- Click "Logout" in the sidebar and confirm your action in the modal.

Structure
---------
- `accounts/`: Main application logic (views, models, urls).
- `teacherdirectory/`: Project settings and configuration.
- `static/`: CSS and JavaScript files.
- `templates/`: HTML templates for the UI.
- `media/`: User-uploaded content (profile images).

troubleshooting
---------------
- **Static Files**: If styles look broken, ensure `STATICFILES_DIRS` is correctly set in `settings.py`.
- **Images**: Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured to handle profile pictures.
