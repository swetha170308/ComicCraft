# Phase 4: Project Planning Phase
## Project Planning & Milestone Execution

### 1. Work Breakdown Structure (WBS) & Milestones
The project execution plan is structured into five sequential milestones comprising twelve concrete activities:

```
ComicCraft Project
├── Milestone 1: Model Selection & Architecture Setup
│   ├── Activity 1.1: Research and Select Generative AI Models (Gemini Flash, Gemini Pro, Stable Diffusion)
│   ├── Activity 1.2: Define System Architecture (Frontend, FastAPI Backend, AI Services)
│   └── Activity 1.3: Set Up Development Environment (Virtual environment, dependencies)
├── Milestone 2: Core Functionalities Development
│   ├── Activity 2.1: Develop Core AI Modules (gemini_flash, gemini_pro, image_generator, layout_builder, exporters)
│   └── Activity 2.2: Implement FastAPI Backend Routing & Input Ingestion
├── Milestone 3: Route Logic & API Integration
│   └── Activity 3.1: Write Complete Application Logic in routes.py (HTML & JSON endpoints)
├── Milestone 4: Frontend UI & Jinja2 Templates
│   ├── Activity 4.1: Design & Develop Responsive Modern Comic User Interface (CSS styling, halftones)
│   └── Activity 4.2: Create Dynamic Jinja2 Templates (index.html, comic_preview.html, export_success.html)
└── Milestone 5: Local Deployment & Verification
    ├── Activity 5.1: Prepare Application for Local Deployment (Environment variables, fonts, directory structure)
    └── Activity 5.2: Test and Verify Local Deployment (End-to-end testing, Swagger UI, PDF validation)
```

---

### 2. Timeline & Schedule (Gantt Chart Representation)

```
Activity Name                       Week 1        Week 2        Week 3        Week 4
---------------------------------------------------------------------------------------
1.1 Model Research & Selection      [====]
1.2 Architecture Definition          [====]
1.3 Environment & Dep. Setup          [====]
2.1 Core AI Modules Dev                      [==========]
2.2 Backend Input Handling                    [=====]
3.1 routes.py Implementation                        [==========]
4.1 Frontend UI / CSS Design                              [==========]
4.2 Dynamic Jinja2 Templating                               [=====]
5.1 Local Config & Env Setup                                     [====]
5.2 Testing, PDF Audit & Deploy                                  [==========]
```

---

### 3. Roles and Resource Allocation

| Role | Responsibilities | Assigned Primary Files |
| :--- | :--- | :--- |
| **AI Systems Engineer** | Model research, prompt engineering, Gemini Flash & Pro integration. | `app/gemini_flash.py`, `app/gemini_pro.py` |
| **Computer Vision Engineer** | Diffusion pipeline configuration, illustration rendering, image optimization. | `app/image_generator.py`, `static/panels/` |
| **Backend Engineer** | Server architecture, routing logic, REST API, PDF compilation engine. | `app/main.py`, `app/routes.py`, `app/exporters.py` |
| **Frontend UI/UX Designer** | HTML5 templates, comic design system, animations, responsive layout. | `templates/*.html`, `static/css/style.css`, `static/js/main.js` |
| **QA & Verification Lead** | Automated testing, PDF page inspection, user scenario validation. | `tests/`, documentation |

---

### 4. Risk Assessment & Mitigation Plan

| Identified Risk | Likelihood | Impact | Mitigation Strategy |
| :--- | :---: | :---: | :--- |
| **Gemini API Rate Limiting / Offline Network** | Medium | High | Implemented intelligent parametric fallback generators that parse inputs and craft tailored outlines/stories without failing. |
| **Stable Diffusion Memory Overhead on CPU** | High | High | Concurrent multi-threaded generation with graceful procedural comic graphic fallback that generates rich panels with 0 latency. |
| **PDF Page Overflow in FPDF** | Low | Medium | Custom `ComicPDF` subclass with dedicated `footer()` method, 80mm image sizing, and margin calibration ensuring strict 1 page per panel. |
| **Unicode Font Encoding Errors in PDF** | Medium | High | Embedded true TrueType `DejaVuSans.ttf` font with automatic latin-1 character fallback. |
