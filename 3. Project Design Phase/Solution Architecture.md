# Phase 3: Project Design Phase
## Solution Architecture

### 1. Architectural Diagram
ComicCraft follows a clean, three-tier modular architecture separating presentation, business logic orchestration, and AI model services:

```mermaid
graph TB
    subgraph Presentation_Layer["1. Presentation Tier (Frontend)"]
        UI_Home["index.html<br/>• Story Prompt Form<br/>• Style & Tone Selectors<br/>• Quick Presets"]
        UI_Preview["comic_preview.html<br/>• 5-Panel Comic Strip<br/>• Speech Bubbles & Narrations<br/>• Download Actions"]
        UI_Success["export_success.html<br/>• Download Confirmation<br/>• Re-download Link<br/>• Create Another CTA"]
        CSS["style.css (Modern Comic Design, Glassmorphism, Halftones)"]
        JS["main.js (Dynamic Presets, Sound Effects, Loading Overlay)"]
    end

    subgraph Controller_Layer["2. Application Tier (FastAPI Backend)"]
        App["main.py (App Initialization & Middleware)"]
        Routes["routes.py<br/>• GET /<br/>• POST /generate<br/>• POST /generate-comic/json<br/>• GET /download/{filename}<br/>• GET /export-success<br/>• GET /test-image"]
    end

    subgraph Service_Layer["3. Core Processing & AI Engine"]
        Mod_Flash["gemini_flash.py<br/>generate_outline()<br/>(Gemini 1.5 Flash)"]
        Mod_Pro["gemini_pro.py<br/>generate_story()<br/>(Gemini 1.5 Pro)"]
        Mod_Img["image_generator.py<br/>generate_image()<br/>(Diffusers & Inking Pipeline)"]
        Mod_Layout["layout_builder.py<br/>build_comic_layout()"]
        Mod_PDF["exporters.py<br/>save_pdf()<br/>(FPDF2 Unicode Compiler)"]
    end

    subgraph Storage_Layer["4. Storage & Static Assets"]
        Panels["static/panels/ (*.png)"]
        Exports["static/exports/ (*.pdf)"]
        Fonts["static/fonts/ (DejaVuSans.ttf)"]
    end

    UI_Home -->|POST Form Data| Routes
    Routes -->|Story Idea| Mod_Flash
    Mod_Flash -->|5-Panel JSON Outline| Mod_Pro
    Mod_Flash -->|Scene Image Prompts| Mod_Img
    Mod_Img -->|Write PNG Files| Panels
    Mod_Img -->|PNG File Paths| Mod_Layout
    Mod_Pro -->|Narration & Dialogue| Mod_Layout
    Mod_Layout -->|Structured Layout Dict| Mod_PDF
    Mod_Layout -->|Layout Object| UI_Preview
    Mod_PDF -->|Compile PDF File| Exports
    Exports -->|Download Attachment| UI_Success
```

---

### 2. Component Responsibilities

| Component | File Path | Primary Responsibility |
| :--- | :--- | :--- |
| **Server Entrypoint** | `app/main.py` | Instantiates FastAPI, configures CORS middleware, mounts `/static` file directories, and registers route controllers. |
| **API Router** | `app/routes.py` | Handles incoming HTTP requests, performs input validation via Pydantic, coordinates the AI pipeline, and renders templates. |
| **Panel Outliner** | `app/gemini_flash.py` | Queries Gemini 1.5 Flash with structured system instructions to produce a valid 5-panel JSON storyline array. |
| **Dialogue Expander**| `app/gemini_pro.py` | Queries Gemini 1.5 Pro to expand the outline into comic book narration, environmental captions, and character dialogue. |
| **Image Generator** | `app/image_generator.py`| Inks panel scenes using generative diffusion or artistic illustration pipelines, outputting optimized PNG assets. |
| **Layout Builder** | `app/layout_builder.py` | Extracts title, speech bubble, caption, and narration metadata, mapping them to corresponding panel imagery. |
| **PDF Exporter** | `app/exporters.py` | Formats each panel into a dedicated A4 page with TrueType Unicode fonts and compiles the downloadable PDF document. |

---

### 3. Fault-Tolerance & Resilience Strategy
- **Decoupled Fallback Engine**: If the Gemini API is unreachable or environment keys are absent, both `gemini_flash.py` and `gemini_pro.py` switch to semantic fallback generators that tailor outlines and stories based on user parameters, preventing 500 errors.
- **Concurrent Inking with Cache Check**: In `image_generator.py`, prompt strings are hashed to check for existing panel assets before initiating redundant generation.
- **Unicode Font Handling**: TrueType fonts are loaded with error-handling to prevent character set encoding exceptions in multi-language environments.
