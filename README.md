# 🏥 Hospital AI System

A modern **Telemedicine & AI Triage Application** powered by **Google Gemini**.
This platform connects patients with doctors, offers intelligent appointment scheduling, and features advanced AI tools for emergency triage and video consultation analysis.

## 🌟 Key Features

### 1. 🤖 AI-Powered Emergency Triage
-   **Chat with AI**: Immediate guidance for symptoms using Gemini 3.0 Flash.
-   **Smart Response**: Differentiates between critical emergencies (directing to 911) and manageable symptoms.

### 2. 🎥 Video Consultation Intelligence
-   **Record & Upload**: Patients can record short consultation videos describing their condition.
-   **AI Analysis**: The system analyzes the video to generate a **Transcript**, identify **Key Symptoms**, and suggest **Next Steps**.

### 3. 📅 Smart Appointment Booking
-   **Role-Based Access**: Separate portals for **Doctors** and **Patients**.
-   **Dynamic Scheduling**: View available doctors and book fixed time slots.
-   **Rescheduling**: Easy management of existing appointments.

### 4. 🎨 Modern UI/UX
-   **Glassmorphism Design**: Premium, deep-space blue aesthetic.
-   **Responsive**: Fully functional on mobile and desktop.
-   **Animations**: Smooth transitions and interactive elements.

---

## 🛠️ Tech Stack

-   **Backend**: Flask (Python)
-   **AI Engine**: Google Gemini API (`gemini-3-flash-preview` & `gemini-2.0-flash`)
-   **Frontend**: HTML5, CSS3 (Custom Design System), JavaScript
-   **Database**: CSV (Lightweight persistence for Demo)
-   **Deployment**: Ready for Render.com (Gunicorn)

---

## 🚀 Installation & Local Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/7abhishe/healthCareSystem.git
    cd healthCareSystem
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the `app/` directory (or root):
    ```ini
    GEMINI_API_KEY=your_gemini_api_key_here
    FLASK_SECRET_KEY=supersecretkey
    ```

5.  **Run the Application**
    ```bash
    python app/main.py
    ```
    Access the app at `http://127.0.0.1:5000`.

---

## 🌐 Deployment (Render.com)

This project is configured for free hosting on Render.

1.  Push your code to **GitHub**.
2.  Go to [Render Dashboard](https://dashboard.render.com).
3.  Create a **New Web Service**.
4.  Connect your GitHub repository.
5.  **Settings**:
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn app.main:app`
6.  **Environment Variables**:
    -   Add `GEMINI_API_KEY`.
7.  Deploy! 🚀

---

## 📂 Project Structure

```
hospital-ai-app/
├── app/
│   ├── genai/          # AI Agents (Video & Emergency)
│   ├── routes/         # Flask Routes (Auth, Record, Appt)
│   ├── static/         # CSS, JS, Videos
│   ├── templates/      # HTML Templates
│   ├── main.py         # App Entry Point
│   └── users.csv       # Data Storage
├── requirements.txt    # Python Dependencies
├── Procfile            # Deployment Config
└── README.md           # Documentation
```

## 🛡️ License

This project is for educational purposes. Medical advice provided by the AI is for demonstration only and should not replace professional medical consultation.