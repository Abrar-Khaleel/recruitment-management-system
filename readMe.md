```markdown
# Recruitment Management System (RMS) 👔

A modern, responsive, and full-stack web application designed for HR departments to manage recruitment pipelines, track job postings, and handle candidate applications. Built with a focus on clean Enterprise UI/UX and a robust Django backend.

## 🚀 Key Features

### 📊 Analytics & Reporting
* **Interactive Dashboard:** Live counters for "Total Candidates" and "Open Positions," plus a "Recent Applications" table.
* **Visual Analytics:** Integrated Chart.js visualization showing candidate distribution across different job roles.
* **Data Export:** One-click CSV export functionality to download candidate data for offline analysis in Excel.

### 🎨 Frontend & Design
* **Zero-JS Dropdowns:** Innovative pure CSS implementation for interactive profile menus, ensuring high performance.
* **Modern "Glassmorphism" UI:** Uses a card-glass aesthetic with translucent backgrounds and soft shadows for a premium, clean look.
* **Responsive Sidebar:** A fixed, intuitive navigation bar that adapts to different screen sizes.

### ⚙️ Backend (Django)
* **Full CRUD Operations:**
    * **Create:** Post new Job Roles and Add Candidate profiles via secure forms.
    * **Read:** Dynamic searchable lists for Candidates and Jobs with pagination.
    * **Update:** Pre-filled forms to edit existing job posts or candidate details.
    * **Delete:** Secure confirmation pages with POST request protection to prevent accidental data loss.
* **Relational Database:** Implements `ForeignKey` relationships between Candidates and Job Roles (One-to-Many).
* **Authentication Flow:** Secure Login, Register, and Forgot Password UI routed through Django's auth system.

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons.
* **Backend:** Python 3.12.5, Django 5.0+.
* **Database:** MySQL (Production ready).
* **Architecture:** Django MVT (Model-View-Template).

## 📂 Project Structure

```text
RECRUITMENT-MANAGEMENT-SYSTEM/
├── manage.py              # Django Task Manager
├── sms/                   # Project Configuration
│   ├── settings.py        # Database & App Config
│   └── urls.py            # Main Router
├── students/              # Main Logic (Internal App Name)
│   ├── models.py          # Schema (Candidate, JobRole)
│   ├── views.py           # Controller Logic & Analytics
│   └── urls.py            # App-specific Routes
├── static/                # Static Assets
│   └── css/
│       └── style.css
└── templates/             # HTML Views
    ├── dashboard.html     # Analytics Dashboard
    ├── students.html      # Candidate Directory
    ├── courses.html       # Job Postings
    └── ... (other pages)

```

## 🔧 Installation & Setup

Follow these steps to run the project locally on your machine.

**1. Clone the Repository**

```bash
git clone https://github.com/Abrar-Khaleel/recruitment-management-system.git
cd recruitment-management-system

```

**2. Create a Virtual Environment**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

```

**3. Install Dependencies**

```bash
pip install django mysqlclient

```

**4. Configure Database**

* Ensure you have a MySQL database named `sms_db` created.
* Update `sms/settings.py` with your MySQL credentials if necessary.

**5. Apply Database Migrations**

```bash
python manage.py makemigrations
python manage.py migrate

```

**6. Create Admin User**

```bash
python manage.py createsuperuser

```

**7. Run the Development Server**

```bash
python manage.py runserver

```

Open your browser and navigate to: `http://127.0.0.1:8000/`



