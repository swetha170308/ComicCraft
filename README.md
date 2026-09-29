# ComicCraft - AI Comic Story Creator using Gemini Models

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![AI Models](https://img.shields.io/badge/Models-Gemini%201.5%20Flash%20%7C%20Pro%20%7C%20Diffusion-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Academic Track](https://img.shields.io/badge/TN%20Skills-AI%2FML%20%26%20GenAI%20Track-purple.svg)](https://smartbridge.com/)

**ComicCraft** is an end-to-end generative AI web application that automatically transforms user prompts into rich, panel-by-panel comic book adventures. Combining **Google Gemini Flash** (structured narrative outlining), **Google Gemini Pro** (character dialogues and story expansion), **Diffusion Inking Models** (scene illustrations), and **FPDF2** (document compilation), ComicCraft enables anyone to create and publish print-ready comic books in seconds.

---

## 🌟 Key Features

1. **Multi-Attribute Story Form**: Custom inputs for Story Prompt, Character Name, Setting, Tone (Dramatic, Funny, Poetic, Action-packed), and Art Style (Anime, Comic Book, Realistic, Pixel Art, Cyberpunk).
2. **1-Click Story Presets**: Instant auto-fill for 4 curated story concepts (*The Brave Fox*, *Cyberpunk Detective*, *Cosmic Odyssey*, *Magic Academy*).
3. **5-Panel Narrative Outlining**: Gemini 1.5 Flash plans a structured narrative arc (Threshold, Rising Action, Confrontation, Climax, Resolution).
4. **Cinematic Dialogue & Narration**: Gemini 1.5 Pro synthesizes authentic character dialogues, narrator blocks, and ambient environmental captions (`**CAPTION:**`).
5. **Concurrent Visual Inking**: Multi-threaded image generation (`ThreadPoolExecutor`) inking all 5 panels in parallel.
6. **Dynamic Web Preview**: Interactive sequential comic strip featuring custom speech bubbles, yellow caption boxes, and illustration frames.
7. **Publication-Ready PDF Export**: Generates a standardized 5-page A4 PDF (exactly 1 panel per page) using embedded TrueType fonts (`DejaVuSans.ttf`).
8. **Export Confirmation & Sharing**: Celebratory export success page with re-download capabilities and a call-to-action to create another comic.
9. **Headless JSON REST API**: Complete API endpoint (`/generate-comic/json`) for programmatic integrations.
10. **Intelligent Fallback Engine**: Guaranteed 100% uptime with built-in parametric generation when API keys are unconfigured or offline.

---

## 🏗️ Technical Architecture

```
User (Browser Client / JSON API)
             │
             ▼
   [FastAPI Server: app/main.py]
             │
             ├──► [routes.py: /generate & /generate-comic/json]
             │          │
             │          ├─► 1. [gemini_flash.py] ──► 5-Panel JSON Outline
             │          │
             │          ├─► 2. [gemini_pro.py]   ──► Dialogues, Narration & Captions
             │          │
             │          ├─► 3. [image_generator.py] (Concurrent Inking Pipeline)
             │          │          │
             │          │          ▼
             │          │     static/panels/*.png
             │          │
             │          ├─► 4. [layout_builder.py] ──► Structured Comic Layout
             │          │
             │          └─► 5. [exporters.py] ──► FPDF2 Unicode PDF Compiler
             │                                         │
             │                                         ▼
             │                                    static/exports/*.pdf
             │
             ├─► [comic_preview.html] (Interactive Sequential Strip)
             │
             └─► [export_success.html] (Download Confirmation & CTA)
```

---

## 📂 Project Repository Structure (Phase-Wise Submission)

```
magesh/
├── 1. Brainstorming & Ideation/
│   ├── Brainstorming & Idea Prioritization.md (and .pdf)
│   ├── Define Problem Statements .md (and .pdf)
│   └── Empathy Map.md (and .pdf)
├── 2. Requirement Analysis/
│   ├── Customer Journey Map.md (and .pdf)
│   ├── Data Flow Diagram.md (and .pdf)
│   ├── Solution Requirements.md (and .pdf)
│   └── Technology Stack.md (and .pdf)
├── 3. Project Design Phase/
│   ├── Problem-Solution Fit.md (and .pdf)
│   ├── Proposed Solution.md (and .pdf)
│   └── Solution Architecture.md (and .pdf)
├── 4. Project Planning Phase/
│   └── Project Planning.md (and .pdf)
├── 5. Project Development Phase/
│   ├── Code-Layout, Readability and Reusability.md (and .pdf)
│   ├── Coding & Solution.md (and .pdf)
│   └── No. of Functional Features Included in the Solution.md (and .pdf)
├── 6.Project Testing/
│   └── Performance Testing.md (and .pdf)
├── 7.Project Documentation/
│   ├── Project Executable Files.md (and .pdf)
│   └── Sample Project Documentation.md (and .pdf)
├── 8.Project Demonstration/
│   ├── Communication.md (and .pdf)
│   ├── Demonstration of Proposed Features.md (and .pdf)
│   ├── Project Demo Planning.md (and .pdf)
│   ├── Scalability & Future Plan.md (and .pdf)
│   └── Team Involvement in Demonstration.md (and .pdf)
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── panels/
│   ├── exports/
│   └── fonts/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start & Installation

### 1. Clone & Enter Project Directory
```bash
git clone <repository-url>
cd magesh
```

### 2. Set Up Virtual Environment
```bash
# macOS / Linux
python3 -m venv env
source env/bin/activate

# Windows
python -m venv env
env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Secrets
```bash
cp .env.example .env
```
Add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_KEY=your_huggingface_api_key_here
HOST=127.0.0.1
PORT=8000
```
*(Note: If no API key is provided, ComicCraft runs in full offline fallback mode with dynamic personalized story and image generation!)*

### 5. Launch the Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Visit the application in your browser:
- **Web App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc API Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testing & Verification

Run the automated integration test suite:
```bash
python3 -c "
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)
assert client.get('/').status_code == 200
assert client.get('/test-image').status_code == 200
res = client.post('/generate-comic/json', json={'prompt': 'The brave fox', 'character_name': 'Free', 'setting': 'Forest', 'tone': 'Dramatic', 'style': 'Comic Book'})
assert res.status_code == 200
print('✅ All System Endpoints & Comic Generation Tests Passed!')
"
```

---

## 📝 Student Project Submission Checklist

- [x] **Phase 1: Brainstorming & Ideation** completed with Brainstorming, Problem Statements, and Empathy Map.
- [x] **Phase 2: Requirement Analysis** completed with Journey Map, DFD, Requirements, and Tech Stack.
- [x] **Phase 3: Project Design Phase** completed with Problem-Solution Fit, Proposed Solution, and Architecture.
- [x] **Phase 4: Project Planning Phase** completed with WBS, Timeline, and Resource Allocation.
- [x] **Phase 5: Project Development Phase** completed with Code Layout, Solutions, and Feature List.
- [x] **Phase 6: Project Testing** completed with Unit Tests, Latency Benchmarks, and Concurrency Verification.
- [x] **Phase 7: Project Documentation** completed with Executable Guide and Comprehensive Technical Report.
- [x] **Phase 8: Project Demonstration** completed with Video Demo Script, Feature Walkthrough, and Future Roadmap.
- [x] **Deliverables**: Both `.md` and `.pdf` files compiled in each phase directory.
- [x] **Application**: Fully operational end-to-end prototype on FastAPI.

---

## 📜 License
This project is developed for the **TN Skills / SmartBridge AI-ML and GenAI Track**. Released under the MIT License.
