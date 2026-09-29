# Phase 2: Requirement Analysis
## Customer Journey Map

### 1. Journey Overview
The Customer Journey Map tracks the end-to-end user experience within ComicCraft across five distinct phases: **Discovery & Prompting**, **Configuration & Preference Setting**, **AI Multi-Model Processing**, **Sequential Review**, and **Publication & Export**.

---

### 2. Multi-Stage Journey Table

| Journey Stage | User Goals & Actions | Touchpoint | User Thoughts & Emotions | System Response / Feature | Potential Friction & Mitigations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Discovery & Prompting** | User visits ComicCraft to create an AI comic. Reads hero tagline and explores story presets. | Homepage (`/`) | *"Can I really make a comic without drawing?"* - Curious, hopeful. | Renders atmospheric comic header, clear value proposition, and quick-picker preset chips. | Blank page syndrome. Mitigation: 4 pre-engineered story presets with 1-click auto-fill. |
| **2. Configuration** | Fills in Story Prompt, Character Name, Setting, Tone, and Art Style. | Creation Form Card (`index.html`) | *"I want this to feel like a classic comic book."* - Creative, engaged. | Form validation highlights required fields and provides responsive select dropdowns. | Complex forms discourage users. Mitigation: Streamlined 5-field form with sensible defaults. |
| **3. Processing** | Clicks "GENERATE COMIC STRIP" and waits for AI orchestration. | Loading Overlay | *"I hope the story is exciting!"* - Anticipatory. | Displays dynamic comic loading overlay with rotating sound effects (*POW!*, *ZAP!*, *KABOOM!*) and progress labels. | Perceived waiting time. Mitigation: Multi-threaded concurrent image generation reduces wait by 5x. |
| **4. Sequential Review** | Reviews 5-panel comic sequentially: images, scene description, dialogue, captions, prompt references. | Comic Preview Page (`/generate`) | *"Wow, this looks like an actual comic page!"* - Delighted, impressed. | Renders panel cards with speech bubbles, yellow caption boxes, dark narrator blocks, and scene frames. | Disconnected story panels. Mitigation: Sequential prompt binding maintains storyline continuity. |
| **5. Publication & Export** | Clicks "Download Your Comic as PDF". Saves the PDF to their local computer. | Download & Export Success Page (`/export-success`) | *"I can print this out and share it with my friends!"* - Proud, satisfied. | Downloads timestamped PDF (`comic_YYYYMMDD_HHMMSS.pdf`) and redirects to celebratory confirmation page. | Broken download links. Mitigation: Native FastAPI `FileResponse` attachment stream with fallback links. |

---

### 3. Key Moments of Truth (MoT)
- **Zero-Friction Prompting**: Enabling the user to test the platform in under 5 seconds using quick presets.
- **The Visual Reveal**: First impression of the 5-panel strip with authentic comic speech bubbles and illustrations.
- **Offline Artifact Delivery**: Holding the completed multi-page PDF document confirms genuine product utility.
