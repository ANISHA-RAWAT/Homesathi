# 🏠 HomeSathi – Online Property Renting System

A full-stack web application built with **Django** and **MySQL** that allows users to search, list, and rent properties online. The platform features secure authentication, internal messaging, and a clean responsive UI.

---

## 🚀 Features

- 🔍 **Property Search** – Search and filter available properties
- 📋 **Property Listings** – Owners can list, manage and update their properties with images
- 👤 **User Authentication** – Secure signup/login with **email verification**
- 📬 **Internal Messaging System** – Buyers and owners can communicate directly within the platform (like an in-app inbox)
- 🗂️ **My Listings** – Owners can manage all their listed properties
- 📄 **Property Detail Page** – Full details view for each property
- ❓ **FAQ & About Us Pages** – Informational pages for users
- 📞 **Contact Us** – Users can reach out for support

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| Auth | Django Authentication + Email Verification |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
Homesathi/
├── homesathi/        # Project settings and URLs
├── properties/       # Property listing app (views, models, urls)
├── users/            # User auth app (signup, login, email verification)
├── templates/        # HTML templates for all pages
├── static/           # CSS, JS, images
├── media/            # Uploaded property images
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.x
- MySQL
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ANISHA-RAWAT/Homesathi.git
cd Homesathi

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure MySQL database in homesathi/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homesathi_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 4. Configure email settings in settings.py for email verification
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📸 Pages

| Page | Description |
|------|-------------|
| Homepage | Landing page with featured properties |
| Search | Filter and browse available properties |
| Product Detail | Full property info with images |
| My Listings | Owner dashboard to manage listings |
| Inbox | Internal messaging between users |
| Login / Signup | Auth with email verification |
| Contact Us | Support form |
| FAQ | Frequently asked questions |
| About Us | About the platform |

---

## 👩‍💻 Author

**Anisha Rawat**
- GitHub: [@ANISHA-RAWAT](https://github.com/ANISHA-RAWAT)
- LinkedIn: [anisha-rawat-59bb92343](https://linkedin.com/in/anisha-rawat-59bb92343)
