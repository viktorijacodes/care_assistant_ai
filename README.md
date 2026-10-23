# Care Assistant AI 🩺

**Health Memory Activity Planner for Nursing & Care Staff**

Care Assistant AI is an intelligent healthcare web application designed to help nursing home staff, caregivers, and care teams plan personalized, meaningful health memory activities for residents with cognitive impairments or dementia.

---

## 🌟 Key Features

- **Personalized Resident Selection**: Interactive resident grid featuring tailored patient profiles (Astrid, Erik, Ingrid, Lars, Birgitta, Sven, Margareta, Nils, Eva) with mobility status, cognitive condition, and personal preferences/memories.
- **Duration Presets**: Quick selection for activity durations (`5 minutes or less`, `5–15 minutes`, `15–30 minutes`, `30+ minutes`).
- **3-Section Visual Activity Card**:
  1. **Suggested Activity**: Clear 1–2 sentence activity description customized to the resident's interests.
  2. **Conversation Starters**: Exactly 3 open-ended, natural questions for caregivers to engage the resident.
  3. **Why This Activity Fits**: Contextual rationale explaining why the activity suits the resident's preferences and cognitive profile.
- **Responsive Healthcare Interface**: Clean, calming green UI designed for ease of use in care home environments across desktop, tablet, and mobile screens.

---

## 🛠️ Architecture & Technologies

- **Frontend**: HTML5, Modern CSS3 (Grid/Flexbox), Vanilla JavaScript (ES6+), FastAPI static file server.
- **AI Agent Backend**: Built with [Google ADK (Agent Development Kit)](https://github.com/google/adk) and Gemini models.
- **Protocol**: A2A / Structured JSON normalization for agent UI responses.
- **Deployment**: Google Cloud Run / Agent Engine.

---

## 🚀 Quick Start

### Prerequisites

- [Python 3.11+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) Python package manager
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (for GCP deployment)

### 1. Installation

Clone the repository and install dependencies using `uv`:

```bash
git clone https://github.com/viktorijacodes/care_assistant_ai.git
cd care_assistant_ai
uv sync
```

### 2. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Ensure `GOOGLE_CLOUD_PROJECT` is set to your active GCP project ID.

### 3. Run Locally

Start the FastAPI frontend server:

```bash
uv run python frontend/main.py
```

Open your browser and navigate to `http://localhost:8080` (or `http://localhost:8000`).

---

## ☁️ Deployment

Deploy the web frontend directly to Google Cloud Run:

```bash
gcloud run deploy care-assistant-frontend --source=frontend --region=us-central1
```

---

## 📄 License

This project is open-source and available under the MIT License.
