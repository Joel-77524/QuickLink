from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string, random
import qrcode
from io import BytesIO
from flask import send_file

app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Root12345@localhost/url_shortener"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# DATABASE MODEL
# =========================
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# CREATE TABLES
# =========================
with app.app_context():
    db.create_all()

# =========================
# UTILITY FUNCTION
# =========================
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

# =========================
# HOME PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        long_url = request.form.get("long_url")
        custom_alias = request.form.get("custom_alias")
        password = request.form.get("password")
        expires_at = request.form.get("expires_at")

        if not long_url:
            error = "Long URL is required"
        else:
            if custom_alias:
                if URL.query.filter_by(short_code=custom_alias).first():
                    error = "Custom alias already exists"
                short_code = custom_alias
            else:
                short_code = generate_short_code()

            expiry_date = None
            if expires_at:
                expiry_date = datetime.strptime(expires_at, "%Y-%m-%d")

            if not error:
                new_url = URL(
                    long_url=long_url,
                    short_code=short_code,
                    password=password if password else None,
                    expires_at=expiry_date
                )
                db.session.add(new_url)
                db.session.commit()

                short_url = request.url_root + short_code

    return render_template(
        "index.html",
        short_url=short_url,
        error=error
    )

# =========================
# ANALYTICS PAGE
# =========================
@app.route("/analytics")
def analytics():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template("analytics.html", urls=urls)

# =========================
# REDIRECT SHORT URL
# =========================
@app.route("/<short_code>", methods=["GET", "POST"])
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        abort(404)

    # Expiry check
    if url.expires_at and datetime.utcnow() > url.expires_at:
        return "This link has expired", 410

    # Password protection
    if url.password:
        if request.method == "POST":
            entered = request.form.get("password")
            if entered != url.password:
                return render_template(
                    "password.html",
                    error="Incorrect password",
                    short_code=short_code
                )
        else:
            return render_template(
                "password.html",
                short_code=short_code
            )

    # Increase clicks
    url.clicks += 1
    db.session.commit()

    return redirect(url.long_url)

@app.route("/qr/<short_code>")
def generate_qr(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()

    short_url = request.url_root + short_code

    qr = qrcode.make(short_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")

@app.route("/qr-page/<short_code>")
def qr_page(short_code):
    short_url = request.url_root + short_code
    return render_template(
        "qr.html",
        short_code=short_code,
        short_url=short_url
    )

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
