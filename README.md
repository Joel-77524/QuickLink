//QuickLink - URL Shortener

QuickLink is a full-stack URL shortening web application built with Flask and MySQL. It allows users to create custom short URLs, generate QR codes, set link expiration dates, protect links with passwords, and track click analytics through a dedicated dashboard.

🚀 Features
🔗 Shorten long URLs instantly
✨ Custom short aliases
🔒 Password-protected links
⏳ Link expiration dates
📊 Analytics dashboard with click tracking
📱 QR code generation for each shortened URL
🔄 Automatic redirection to original URLs
🗄️ MySQL database integration
🎨 Responsive and modern user interface
🛠️ Tech Stack
Frontend
HTML5
CSS3
JavaScript
Font Awesome
Backend
Python
Flask
SQLAlchemy
Database
MySQL
Additional Libraries
PyMySQL
qrcode
Pillow
📂 Project Structure
QuickLink/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── analytics.html
│   ├── qr.html
│   └── password.html
│
├── static/
│
├── requirements.txt
│
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/Joel-77524/QuickLink.git
cd QuickLink
2. Create Virtual Environment
python -m venv venv
3. Activate Virtual Environment
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
4. Install Dependencies
pip install flask
pip install flask_sqlalchemy
pip install pymysql
pip install qrcode[pil]

Or:

pip install -r requirements.txt
🗄️ Database Setup

Create a MySQL database:

CREATE DATABASE url_shortener;

Update the database configuration in app.py:

app.config["SQLALCHEMY_DATABASE_URI"] = \
"mysql+pymysql://root:YOUR_PASSWORD@localhost/url_shortener"
▶️ Running the Application

Start the Flask server:

python app.py

Open your browser:

http://127.0.0.1:5000
📊 Analytics Dashboard

The analytics dashboard displays:

Original URL
Shortened URL
Click count
Expiry date
QR code access

Visit:

http://127.0.0.1:5000/analytics
🔒 Password Protected Links

Users can optionally secure shortened URLs using a password.

When accessing a protected link:

User enters password.
Password is verified.
Successful verification redirects to the original URL.
📱 QR Code Generation

Each shortened URL has an automatically generated QR code that can be:

Viewed from the analytics dashboard
Scanned directly using any QR scanner
Shared across devices
🎯 Future Enhancements
User authentication and accounts
Link management dashboard
Link deletion and editing
Download QR code functionality
Geo-location analytics
Device and browser analytics
REST API support
Custom branded domains
Dark mode support
📸 Screenshots
Home Page
URL shortening form
Custom aliases
Password protection
Expiry date selection
Analytics Dashboard
Link statistics
Click tracking
QR code access
QR Code Page
Dedicated QR view
Easy sharing and scanning
👨‍💻 Author

Joel Biju

GitHub:
QuickLink Repository

📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational and personal purposes//
