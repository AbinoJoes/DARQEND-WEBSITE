# 🌌 Darqend Technologies — Official Website & Lead Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-API-34A853.svg?logo=googlesheets&logoColor=white)](https://sheets.new)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26.svg?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6.svg?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E.svg?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](#license)

> **"We turn bold ideas into digital possibilities."**  
> Darqend Technologies is a full-service digital and software engineering agency crafting high-performance web applications, intelligent data solutions, and bespoke software architectures.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Directory Structure](#-directory-structure)
- [Installation & Setup](#-installation--setup)
  - [Prerequisites](#prerequisites)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Virtual Environment Setup](#2-virtual-environment-setup)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Environment Variables](#4-environment-variables)
  - [5. Google Sheets Webhook Setup](#5-google-sheets-webhook-setup)
  - [6. Running the Application](#6-running-the-application)
- [API Documentation](#-api-documentation)
  - [Health Check (`GET /api/health`)](#1-health-check)
  - [Submit Contact Inquiry (`POST /api/contact`)](#2-submit-contact-inquiry)
- [Validation & Security](#-validation--security)
- [Google Sheets Automation Script](#-google-sheets-automation-script)
- [Production Deployment](#-production-deployment)
- [License](#-license)

---

## 🔭 Overview

The **Darqend Technologies Website** is a modern, high-conversion agency platform paired with a lightweight Python Flask backend. It serves as the primary marketing showcase and client inquiry engine for Darqend Technologies. All customer enquiries are validated on the backend and forwarded directly into a **Google Spreadsheet** in real time via an Apps Script webhook, eliminating the need for a local database server.

---

## ✨ Key Features

### 🖥️ Frontend (Client Experience)
- **Aesthetic Dark Theme & Modern Visuals:** Built with subtle glow orbs, ambient radial gradients, grid overlays, glassmorphic cards, and sleek typography.
- **Multi-Page Site Structure:**
  - `index.html` — Dynamic hero banner, agency narrative, service highlights, and call-to-actions.
  - `about.html` — Agency origin, mission, core values, engineering philosophy, and milestones.
  - `services.html` — Deep-dive service catalog with delivery roadmaps.
  - `projects.html` — Dynamic portfolio gallery equipped with client-side interactive tag/category filtering.
  - `contact.html` — Comprehensive inquiry form with real-time feedback and validation.
- **Responsive Navigation:** Accessible mobile drawer menu with ARIA landmarks, `Escape` key handling, and auto-dismiss on route clicks.
- **Scroll Interactions & Performance:** Scroll-triggered element reveals powered by `IntersectionObserver` with zero external frontend framework dependencies.

### ⚙️ Backend (Google Sheets Lead Engine)
- **Direct-to-Sheets Integration:** Customer leads are automatically validated and written into Google Sheets in real-time.
- **Zero Database Maintenance:** No MySQL or relational database required—simple, robust, and cost-effective.
- **Health Check Endpoint:** Real-time service readiness monitoring at `/api/health`.
- **CORS Protection:** Configured with domain restriction for cross-origin frontend requests.
- **DoS Mitigation:** Hard 32 KB request size ceiling enforced via Flask configuration.
- **Strict Data Validation:** Comprehensive server-side checks for data types, email formatting, string lengths, and whitelisted fields.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Vanilla HTML5, Modern CSS3 (Grid/Flexbox/CSS Variables), Vanilla JavaScript (ES6+) |
| **Backend API** | Python 3.8+, Flask 2.3+, Flask-CORS, python-dotenv, Requests |
| **Data Storage** | Google Sheets (via Google Apps Script Web App) |
| **Assets & Fonts** | Google Fonts (*Inter*), Custom SVG & PNG Brand Assets |

---

## 📐 Project Architecture

```
┌─────────────────────────────────────────┐
│   Frontend Client (Browser / Port 5000) │
│    HTML5 / Modern CSS / Vanilla JS      │
└──────────────────┬──────────────────────┘
                   │
          JSON POST /api/contact
                   │
                   ▼
┌─────────────────────────────────────────┐
│       Flask API Service (Port 5000)     │
│         - 32 KB Payload Limit           │
│         - Strict Field Validation       │
│         - CORS Middleware               │
└──────────────────┬──────────────────────┘
                   │
          Direct Webhook POST
          (JSON with secret)
                   │
                   ▼
┌─────────────────────────────────────────┐
│        Google Apps Script Web App       │
│       Appends row to Google Sheet       │
└─────────────────────────────────────────┘
```

---

## 📂 Directory Structure

```plaintext
DARQEND-WEBSITE/
├── .env.example                     # Sample environment variables template
├── .gitignore                       # Git exclusion rules (venv, .env, __pycache__)
├── app.py                           # Flask backend entrypoint & API routes
├── README.md                        # Project documentation (this file)
├── requirements.txt                 # Python package dependencies
│
├── static/                          # Static web assets
│   ├── assets/                      # Brand logos, icons, and graphic assets
│   │   └── WhatsApp_Image_...png    # Darqend logo
│   ├── css/                         # Modular stylesheets
│   │   ├── about.css                # About page styles & animations
│   │   ├── contact.css              # Contact page & form styling
│   │   ├── projects.css             # Project grid & filter tags
│   │   ├── services.css             # Services layout & detail cards
│   │   └── style.css                # Global theme variables, reset, nav, & footer
│   └── js/                          # Client-side JavaScript
│       ├── form.js                  # AJAX contact form submitter & validation
│       └── script.js                # Mobile nav, scroll reveals, & project filters
│
└── templates/                       # Website HTML pages
    ├── about.html                   # About Darqend Technologies
    ├── contact.html                 # Contact & project inquiry page
    ├── index.html                   # Homepage
    ├── projects.html                # Project showcases & portfolio
    └── services.html                # IT & software services catalog
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/))
- A Google Account for **Google Sheets**

---

### 1. Clone Repository

```bash
git clone https://github.com/your-username/DARQEND-WEBSITE.git
cd DARQEND-WEBSITE
```

---

### 2. Virtual Environment Setup

Create and activate an isolated Python environment:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment Variables

Create your `.env` file from the template:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

Open `.env` and set your webhook URL and secret:

```env
GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/your_script_id/exec
GOOGLE_SHEETS_SECRET=Darqend_Secret_Key_2026_xyz!
```

---

### 5. Google Sheets Webhook Setup

Follow the [Google Sheets Automation Script](#-google-sheets-automation-script) instructions below to generate your Webhook URL.

---

### 6. Running the Application

Launch the Flask server:

```bash
python app.py
```

The application will start at `http://127.0.0.1:5000/`. You can immediately open:
- **Homepage:** `http://127.0.0.1:5000/`
- **About:** `http://127.0.0.1:5000/about.html`
- **Services:** `http://127.0.0.1:5000/services.html`
- **Projects:** `http://127.0.0.1:5000/projects.html`
- **Contact:** `http://127.0.0.1:5000/contact.html`
- **API Health:** `http://127.0.0.1:5000/api/health`

---

## 📡 API Documentation

### 1. Health Check

Verifies backend runtime and Google Sheets configuration status.

- **URL:** `/api/health`
- **Method:** `GET`
- **Response Headers:** `Content-Type: application/json`

#### Success Response (`200 OK`)
```json
{
  "success": true,
  "message": "Backend is running and Google Sheets integration is configured."
}
```

---

### 2. Submit Contact Inquiry

Validates the form and sends the inquiry directly to Google Sheets.

- **URL:** `/api/contact`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`

#### Request Payload Specification

| Field | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `fullName` | `string` | **Yes** | Max 120 characters |
| `email` | `string` | **Yes** | Valid email, max 254 characters |
| `phone` | `string` | No | Max 30 characters |
| `service` | `string` | **Yes** | Must match one of [Allowed Services](#allowed-services) |
| `subject` | `string` | **Yes** | Max 200 characters |
| `budget` | `string` | No | Must match one of [Allowed Budgets](#allowed-budgets) |
| `message` | `string` | **Yes** | 1 to 5,000 characters |
| `consent` | `boolean`| **Yes** | Must be strictly `true` |

#### Allowed Services:
- `Web Development`
- `Software Solutions`
- `AI and Data Solutions`
- `UI UX Design`
- `Cloud and Integration`
- `IT Consulting`
- `Other`

#### Allowed Budgets:
- `Under ₹25,000`
- `₹25,000 - ₹50,000`
- `₹50,000 - ₹1,00,000`
- `Above ₹1,00,000`
- `Not decided`
- `""` *(empty string)*

#### Success Response (`201 Created`)
```json
{
  "success": true,
  "message": "Thank you! Your enquiry has been submitted successfully."
}
```

---

## 📊 Google Sheets Automation Script

1. Open your Google Sheet &rarr; **Extensions** &rarr; **Apps Script**.
2. Paste this code:

```javascript
const SHARED_SECRET = "Darqend_Secret_Key_2026_xyz!"; 

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    // Verify secret token
    if (!data.secret || data.secret !== SHARED_SECRET) {
      return ContentService.createTextOutput(
        JSON.stringify({ success: false, message: "Unauthorized: Invalid secret" })
      ).setMimeType(ContentService.MimeType.JSON);
    }

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Auto-create headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Timestamp",
        "Full Name",
        "Email",
        "Phone",
        "Service",
        "Subject",
        "Budget",
        "Message"
      ]);
    }

    // Append the incoming inquiry row
    sheet.appendRow([
      new Date(),
      data.full_name || "",
      data.email || "",
      data.phone || "",
      data.service || "",
      data.subject || "",
      data.budget || "",
      data.message || ""
    ]);

    return ContentService.createTextOutput(
      JSON.stringify({ success: true, message: "Row added successfully" })
    ).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: err.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}
```

3. Click **Deploy** &rarr; **New deployment** &rarr; select **Web app**.
   - **Execute as:** `Me`
   - **Who has access:** `Anyone` *(Crucial!)*
4. Copy the Web app URL and paste it into your `.env` file under `GOOGLE_SHEETS_WEBHOOK_URL`.

---

## 🌐 Production Deployment

For production deployments:

1. **Disable Debug Mode:** Set `debug=False` in `app.run()` or invoke a production WSGI server.
2. **Use a Production WSGI Server:**
   ```bash
   # Linux
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app

   # Windows
   pip install waitress
   waitress-serve --port=5000 app:app
   ```
3. **Configure Reverse Proxy:** Put **Nginx** or **Cloudflare** in front of your WSGI server with HTTPS / SSL termination.

---

## 📄 License

All rights reserved © **Darqend Technologies**.  
This repository contains proprietary source code and assets. Unauthorized copying, distribution, or commercial reuse without explicit written consent is strictly prohibited.
