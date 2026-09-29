# Phase 2: Requirement Analysis
## Technology Stack Justification

### 1. Technology Matrix Overview

| Tier | Technology / Library | Version | Purpose in ComicCraft | Rationale & Justification |
| :--- | :--- | :--- | :--- | :--- |
| **Backend Framework** | **FastAPI** | `>= 0.109.0` | Server-side routing, request handling, form ingestion, and JSON REST API. | Exceptional async performance, automatic OpenAPI documentation (`/docs`), native Pydantic validation, and minimal boilerplate. |
| **ASGI Server** | **Uvicorn** | `>= 0.27.0` | High-performance asynchronous server running FastAPI. | Industry-standard lightning-fast ASGI server built on `uvloop` and `httptools`. |
| **Template Engine** | **Jinja2** | `>= 3.1.2` | Server-rendered dynamic HTML templates. | Seamless integration with FastAPI, expressive template syntax (`{% for panel in layout %}`), fast compilation. |
| **LLM Orchestration** | **Google Gemini Flash** (`gemini-1.5-flash`) | API / SDK | Generating structured 5-panel comic storyline outlines in JSON. | Extremely low latency, superior adherence to JSON schemas, cost-effective for rapid outlining. |
| **Creative Storyteller** | **Google Gemini Pro** (`gemini-1.5-pro`) | API / SDK | Synthesizing detailed comic narration, character dialogue, and captions. | Deep literary reasoning, nuanced character voice generation, and expressive dialogic pacing. |
| **Visual Inking Engine**| **Stable Diffusion & Inking Pipeline** | SD 1.5 / Diffusers | Generating comic-style illustrations from AI scene prompts. | High-quality visual fidelity, rich artistic styling support (anime, comic book, cyberpunk, realistic). |
| **Document Compiler** | **FPDF2** | `>= 2.8.0` | Compiling panels, illustrations, and text into a downloadable PDF document. | Lightweight pure-Python PDF generation with Unicode font embedding (`DejaVuSans.ttf`), precise millimeter layout control. |
| **Image Processing** | **Pillow (PIL)** | `>= 10.0.0` | Image format conversion, dimension checks, and procedural artistic synthesis. | Rock-solid Python imaging standard, fast raster processing, zero binary external dependencies. |
| **Frontend Styling** | **HTML5 & Vanilla Modern CSS** | CSS3 | Responsive comic book UI, glassmorphism, speech bubbles, and animations. | Maximum control, zero heavy UI frameworks, native CSS variables, instant loading speeds. |
| **Configuration** | **python-dotenv** | `>= 1.0.0` | Managing environment variables (`GEMINI_API_KEY`, `HF_API_KEY`). | Secure secret isolation preventing accidental credential leaks. |

---

### 2. Comparative Analysis: Why FastAPI over Flask?
1. **Asynchronous Throughput**: FastAPI's native `async/await` enables non-blocking handling of long-running generative AI calls.
2. **Schema Validation**: FastAPI leverages Pydantic for strict runtime type enforcement (`PromptRequest`), preventing malformed requests.
3. **Interactive Documentation**: Instant Swagger UI (`/docs`) and ReDoc (`/redoc`) for seamless developer and evaluator testing.
