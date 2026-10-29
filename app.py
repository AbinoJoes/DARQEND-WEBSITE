import os
import re
import logging
import requests

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024  # 32 KB maximum request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Local development and frontend origins
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://127.0.0.1:5000",
                "http://localhost:5000",
                "http://127.0.0.1:5500",
                "http://localhost:5500",
            ]
        }
    },
)

ALLOWED_SERVICES = {
    "Web Development",
    "Software Solutions",
    "AI and Data Solutions",
    "UI UX Design",
    "Cloud and Integration",
    "IT Consulting",
    "Other",
}

ALLOWED_BUDGETS = {
    "",
    "Under ₹25,000",
    "₹25,000 - ₹50,000",
    "₹50,000 - ₹1,00,000",
    "Above ₹1,00,000",
    "Not decided",
}


def save_to_google_sheet(contact):
    """Sync contact enquiry directly to Google Sheets webhook."""
    webhook_url = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL")
    secret = os.getenv("GOOGLE_SHEETS_SECRET")

    if not webhook_url or not secret:
        logger.error("Google Sheets webhook URL or secret not configured in .env.")
        return False, "Google Sheets webhook URL or secret is not configured in .env."

    payload = {
        "secret": secret,
        "full_name": contact["full_name"],
        "email": contact["email"],
        "phone": contact.get("phone", ""),
        "service": contact["service"],
        "subject": contact["subject"],
        "budget": contact.get("budget", ""),
        "message": contact["message"],
    }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            allow_redirects=True,
            timeout=20,
        )

        if response.status_code == 401:
            logger.error("Google Apps Script returned 401 Unauthorized. Access must be set to 'Anyone'.")
            return (
                False,
                "Google Apps Script returned 401 Unauthorized. Please ensure 'Who has access' is set to 'Anyone' in your deployment settings."
            )

        response.raise_for_status()

        try:
            res_json = response.json()
            if res_json.get("success"):
                logger.info("Enquiry successfully recorded in Google Sheets.")
                return True, "Enquiry saved successfully."
            else:
                logger.warning("Google Sheets script returned error: %s", res_json)
                return False, res_json.get("message", "Google Sheet rejected the submission.")
        except Exception:
            if "success" in response.text.lower() or response.status_code == 200:
                return True, "Enquiry saved successfully."
            return False, f"Unexpected response from Google: {response.text[:120]}"

    except requests.exceptions.RequestException as exc:
        logger.exception("Google Sheets connection error: %s", exc)
        return False, f"Failed to connect to Google Sheets: {str(exc)}"


# ---------------------------------------------------------------------------
# Frontend Page Routes
# ---------------------------------------------------------------------------

@app.route("/")
@app.route("/index.html")
def index():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/about")
@app.route("/about.html")
def about():
    """Render the About Us page."""
    return render_template("about.html")


@app.route("/services")
@app.route("/services.html")
def services():
    """Render the Services page."""
    return render_template("services.html")


@app.route("/projects")
@app.route("/projects.html")
def projects():
    """Render the Projects portfolio page."""
    return render_template("projects.html")


@app.route("/contact")
@app.route("/contact.html")
def contact():
    """Render the Contact page."""
    return render_template("contact.html")


@app.route("/favicon.ico")
def favicon():
    """Serve the brand icon as the favicon."""
    return send_from_directory(
        os.path.join(app.root_path, "static", "assets"),
        "WhatsApp_Image_2026-10-27_at_9.11.29_PM-removebg-preview.png",
        mimetype="image/png",
    )


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    """Check whether the backend and Google Sheets configuration are available."""
    has_webhook = bool(os.getenv("GOOGLE_SHEETS_WEBHOOK_URL"))
    has_secret = bool(os.getenv("GOOGLE_SHEETS_SECRET"))

    if has_webhook and has_secret:
        return jsonify({
            "success": True,
            "message": "Backend is running and Google Sheets integration is configured."
        }), 200

    return jsonify({
        "success": False,
        "message": "Backend is running, but GOOGLE_SHEETS_WEBHOOK_URL or GOOGLE_SHEETS_SECRET is missing."
    }), 503


@app.post("/api/contact")
def submit_contact():
    """Validate and forward contact enquiry directly to Google Sheets."""
    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Please submit the form as JSON."
        }), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    # Read fields and trim unnecessary whitespace.
    full_name = data.get("fullName", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    service = data.get("service", "")
    subject = data.get("subject", "")
    budget = data.get("budget", "")
    message = data.get("message", "")
    consent = data.get("consent")

    # Reject unexpected data types.
    required_fields = {
        "fullName": full_name,
        "email": email,
        "service": service,
        "subject": subject,
        "message": message,
    }

    if any(not isinstance(v, str) for v in required_fields.values()):
        return jsonify({
            "success": False,
            "message": "Please check your form fields."
        }), 400

    if not all(isinstance(v, str) for v in (phone, budget)):
        return jsonify({
            "success": False,
            "message": "Please check your optional fields."
        }), 400

    full_name = full_name.strip()
    email = email.strip()
    phone = phone.strip()
    service = service.strip()
    subject = subject.strip()
    budget = budget.strip()
    message = message.strip()

    # Validate required fields and lengths.
    if not all([full_name, email, service, subject, message]):
        return jsonify({
            "success": False,
            "message": "Please fill in all required fields."
        }), 400

    if len(full_name) > 120:
        return jsonify({
            "success": False,
            "message": "Name must be 120 characters or fewer."
        }), 400

    if len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    if phone and len(phone) > 30:
        return jsonify({
            "success": False,
            "message": "Phone number is too long."
        }), 400

    if service not in ALLOWED_SERVICES:
        return jsonify({
            "success": False,
            "message": "Please select a valid service."
        }), 400

    if len(subject) > 200:
        return jsonify({
            "success": False,
            "message": "Subject must be 200 characters or fewer."
        }), 400

    if budget not in ALLOWED_BUDGETS:
        return jsonify({
            "success": False,
            "message": "Please select a valid budget."
        }), 400

    if not message or len(message) > 5000:
        return jsonify({
            "success": False,
            "message": "Message must contain 1 to 5000 characters."
        }), 400

    if consent is not True:
        return jsonify({
            "success": False,
            "message": "Please agree to be contacted."
        }), 400

    # Forward directly to Google Sheets
    success, reason = save_to_google_sheet({
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "service": service,
        "subject": subject,
        "budget": budget,
        "message": message,
    })

    if success:
        return jsonify({
            "success": True,
            "message": "Thank you! Your enquiry has been submitted successfully."
        }), 201

    return jsonify({
        "success": False,
        "message": reason
    }), 502


@app.errorhandler(413)
def request_too_large(error):
    return jsonify({
        "success": False,
        "message": "The submitted request is too large."
    }), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
