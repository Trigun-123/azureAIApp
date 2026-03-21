# Azure AI Agent Workshop

This repository contains a Flask application that interfaces with Azure OpenAI Assistants API.

## Prerequisites

- Python 3.8 or higher
- Git

## Prerequisites (Quick Glance Before Session)

Please go through the following resources to understand the basics:

- Copilot Learning Hub (Intro to AI + Copilot tools)
  https://learn.microsoft.com/en-us/shows/copilot-learning-hub?wt.mc_id=studentamb_344953

- Azure AI Foundry (Platform for building AI agents)
  https://learn.microsoft.com/en-us/azure/ai-foundry?wt.mc_id=studentamb_344953

- Microsoft AI Overview (AI ecosystem & concepts)
  https://learn.microsoft.com/en-us/ai/?tabs=business-technical-leader&wt.mc_id=studentamb_344953

- Generative AI Fundamentals (Core AI concepts)
  https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai?wt.mc_id=studentamb_344953

- Azure AI for Developers (Integrating AI into apps)
  https://learn.microsoft.com/en-us/azure/developer/ai?wt.mc_id=studentamb_344953

- Azure Copilot (AI-powered cloud assistance)
  https://learn.microsoft.com/en-us/azure/copilot?wt.mc_id=studentamb_344953

- Agent Academy (Understanding AI agents)
  https://microsoft.github.io/agent-academy?wt.mc_id=studentamb_344953

- Important Setup
  Please ensure you claim your Azure free credits ($100) before the workshop:

- Use your university email (ending with .edu) to sign up
  https://azure.microsoft.com/en-in/pricing/offers/ms-azr-0170p?wt.mc_id=studentamb_344953

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rtarun3606k/Azure-101---Build-and-host-your-1st-app
cd Azure-101---Build-and-host-your-1st-app
```

### 2. Create a virtual environment

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install gunicorn
```

## Configuration

### 1. Create Environment File

Copy the example environment file to a new file named `.env`:

**Linux / macOS:**

```bash
cp .env.example .env
```

**Windows:**

```cmd
copy .env.example .env
```

### 2. Configure Environment Variables

Open the `.env` file in a text editor.

1.  Read the comments in the file.
2.  Uncomment the variable lines (remove the `#` at the beginning of each line).
3.  Replace the placeholder values with your actual Azure OpenAI credentials.

Example variables to set:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `ASSISTANT_ID`
- `FLASK_SECRET_KEY`

## Running the Application

### Development Server

To run the application using the Flask development server:

```bash
python app.py
```

The application will be available at http://127.0.0.1:5000.

### Production Server (Key Recommendation)

To run the application using Gunicorn (production-ready WSGI server):

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

The application will be accessible at http://localhost:8000.
