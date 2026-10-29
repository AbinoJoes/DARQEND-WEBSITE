
import os
import re
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from flask import render_template

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024  # 32 KB maximum request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Local development only.
# In production, allow only your actual website origin.
CORS(
    app,
    resources={
        r"/api/contact": {
            "origins": [
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


def get_db_connection():
    """Create a connection to the MySQL database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "darqend_app"),
        password=os.getenv("DB_PASSWORD","abino123"),
        database=os.getenv("DB_NAME", "darqend_db"),
         connection_timeout=10,
        autocommit=False
    )


@app.get("/api/health")
def health():
    """Check whether the backend and database are available."""
    connection = None
    cursor = None
    

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if not connection.is_connected():
            raise RuntimeError("Database connection is unavailable")

        return jsonify({
            "success": True,
            "message": "Backend and database are connected."
        }), 200

    except (Error, RuntimeError, ValueError):
        logger.exception("Health check failed")

        return jsonify({
            "success": False,
            "message": "Backend or database is unavailable."
        }), 503

    finally:
        if connection and connection.is_connected():
            connection.close()


@app.post("/api/contact")
def submit_contact():
    """Validate and save a contact form submission."""

    # Accept JSON requests from the frontend.
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

    if not all(
        isinstance(v, str) for v in (phone, budget)
    ):
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

    if len(email) > 254 or not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
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

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO contact_messages
            (
                full_name,
                email,
                phone,
                service,
                subject,
                budget,
                message,
                consent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            full_name,
            email,
            phone or None,
            service,
            subject,
            budget or None,
            message,
            1,
        )

        cursor.execute(sql, values)
        connection.commit()

        return jsonify({
            "success": True,
            "message": (
                "Thank you! Your enquiry has been submitted "
                "successfully."
            ),
            "id": cursor.lastrowid,
        }), 201

    except Error:
        if connection and connection.is_connected():
            connection.rollback()

        # Keep database details out of the public response.
        logger.exception("Failed to save contact enquiry")

        return jsonify({
            "success": False,
            "message": (
                "We could not save your enquiry. "
                "Please try again later."
            )
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

        connection.commit()

    # Send the saved contact data to Google Sheets
        try:
            save_to_google_sheet({
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "service": service,
                "subject": subject,
                "budget": budget,
                "message": message,
            })
        except Exception:
            app.logger.exception("Google Sheets sync failed")

        return jsonify({
            "success": True,
            "message": "Contact enquiry saved successfully."
        }), 201

@app.errorhandler(413)
def request_too_large(error):
    return jsonify({
                "success": False,
                "message": "The submitted request is too large."
            }), 413


if __name__ == "__main__":
                # Debug mode is for local development only.
    app.run(host="127.0.0.1", port=5000, debug=True)







import requests

def save_to_google_sheet(contact):
    payload = {
        "secret": os.environ["GOOGLE_SHEETS_SECRET"],
        "full_name": contact["full_name"],
        "email": contact["email"],
        "phone": contact.get("phone", ""),
        "service": contact["service"],
        "subject": contact["subject"],
        "budget": contact.get("budget", ""),
        "message": contact["message"],
    }

    response = requests.post(
        os.environ["GOOGLE_SHEETS_WEBHOOK_URL"],
        json=payload,
        timeout=15
    )

    response.raise_for_status()

    if not response.json().get("success"):
        raise RuntimeError("Google Sheets save failed")



