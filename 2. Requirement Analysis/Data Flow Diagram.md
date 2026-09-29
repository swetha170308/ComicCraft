# Phase 2: Requirement Analysis
## Data Flow Diagram (DFD)

### 1. DFD Level 0: Context Diagram
The Level 0 Context Diagram depicts ComicCraft as a single central process interacting with external entities (Users, Google Gemini AI API, Image Generation Engine, and Local File System).

```mermaid
graph TD
    User([User / Browser Client]) -->|1. Story Prompt, Character, Setting, Tone, Style| System[ComicCraft System - FastAPI]
    System -->|2. Formatted Prompt Envelope| GeminiAPI[Google Gemini AI Models]
    GeminiAPI -->|3. JSON Outline & Story Text| System
    System -->|4. Visual Scene Prompts| ImageGen[Stable Diffusion / Image Generator]
    ImageGen -->|5. Rendered Panel PNGs| System
    System -->|6. Panel Layout & Assets| PDFEngine[FPDF Export Engine]
    PDFEngine -->|7. Compiled Multi-Page PDF| FileStore[(Static File Storage)]
    System -->|8. Rendered Comic Preview HTML| User
    System -->|9. Downloadable PDF Document| User
```

---

### 2. DFD Level 1: Subsystem Decomposition

The Level 1 DFD decomposes the system into its primary operational sub-processes:
1. **Input Ingestion & Validation** (`routes.py`)
2. **5-Panel Outline Generation** (`gemini_flash.py`)
3. **Dialogue & Narration Expansion** (`gemini_pro.py`)
4. **Concurrent Panel Inking** (`image_generator.py`)
5. **Layout Assembly & Binding** (`layout_builder.py`)
6. **PDF Compilation & Storage** (`exporters.py`)
7. **Client Presentation & Download** (`comic_preview.html`, `export_success.html`)

```mermaid
graph LR
    subgraph Frontend
        A[HTML Form / JSON API] -->|Raw Inputs| P1[1.0 Request Handler]
    end

    subgraph Backend_Pipeline
        P1 -->|Full Prompt String| P2[2.0 Gemini Flash Outliner]
        P2 -->|Structured JSON 5-Panel Outline| P3[3.0 Gemini Pro Storyteller]
        P2 -->|Image Prompts| P4[4.0 Image Generator Engine]
        
        P3 -->|Full Narration & Dialogues| P5[5.0 Layout Builder]
        P4 -->|Generated PNG Paths| P5
        P2 -->|Panel Metadata| P5

        P5 -->|Structured Layout Dict| P6[6.0 PDF Exporter]
    end

    subgraph Storage
        P4 -->|Save PNGs| D1[(static/panels/)]
        P6 -->|Save PDF| D2[(static/exports/)]
    end

    subgraph Output_Delivery
        P5 -->|Layout Context| P7[7.0 Preview Renderer]
        P6 -->|PDF Web Path| P7
        P7 -->|HTML Response| Client[User Browser]
        D2 -->|File Stream| Client
    end
```

---

### 3. Data Dictionary

| Data Element | Type | Source | Destination | Description |
| :--- | :--- | :--- | :--- | :--- |
| `prompt` | String | User Form / JSON | `generate_outline()` | The core story premise or narrative spark. |
| `character_name` | String | User Form / JSON | `generate_outline()` | Name of the primary character. |
| `setting` | String | User Form / JSON | `generate_outline()` | Environmental context (e.g. Forest, Space). |
| `tone` | String | User Form / JSON | `generate_outline()`, `generate_story()` | Narrative mood (e.g. Dramatic, Funny). |
| `style` | String | User Form / JSON | `image_generator.py` | Visual aesthetic (e.g. Anime, Realistic). |
| `outline` | List[Dict] | `gemini_flash.py` | `gemini_pro.py`, `image_generator.py` | 5 items containing `panel`, `title`, `scene_description`, `image_prompt`. |
| `full_story` | String | `gemini_pro.py` | `layout_builder.py` | Formatted story containing panel titles, dialogues, and captions. |
| `images` | List[Str] | `image_generator.py` | `layout_builder.py`, `static/panels/` | File paths to the saved 5 panel illustrations. |
| `layout` | List[Dict] | `layout_builder.py` | `save_pdf()`, `comic_preview.html` | Unified collection of panels binding images, titles, descriptions, and story text. |
| `pdf_path` | String | `exporters.py` | `comic_preview.html`, `export_success.html` | Absolute and relative path to the generated comic PDF file. |
