# Phase 8: Project Demonstration
## Project Demonstration Planning & Video Recording Script

### 1. Demonstration Purpose & Scope
This plan guides the recording of a professional 3 to 5-minute video demonstration required for project submission to SmartBridge and TN Skills portal evaluators.

---

### 2. Video Demonstration Script & Timeline (Total Duration: 4 Minutes)

| Time Stamp | Section | Visual on Screen | Spoken Script / Narration Points |
| :---: | :--- | :--- | :--- |
| **0:00 - 0:30** | **Project Introduction** | Title slide / Homepage at `http://127.0.0.1:8000/` | *"Hello everyone! Today we present ComicCraft, an AI-powered comic book story creator built with FastAPI, Google Gemini 1.5 models, and Stable Diffusion. Our goal is to empower non-artists and writers to turn simple prompts into complete 5-panel comic strips with illustrations, dialogues, and downloadable PDFs."* |
| **0:30 - 1:15** | **Architecture & Tech Stack** | Solution Architecture Diagram & Swagger Docs at `/docs` | *"ComicCraft utilizes a multi-model pipeline: Gemini 1.5 Flash plans a structured 5-panel outline, Gemini 1.5 Pro generates character dialogues and captions, while our inking engine renders panel art concurrently. The layout is assembled in FastAPI and compiled using FPDF2."* |
| **1:15 - 2:30** | **Live Creation Demo (Scenario 1)** | Homepage form: Fill "The Brave Fox", click Generate | *"Let's test Scenario 1 using our Brave Fox preset. We specify the character name 'Free', forest setting, dramatic tone, and realistic art style. Clicking Generate brings up our dynamic comic loading overlay. Within seconds, all 5 panels are created!"* |
| **2:30 - 3:15** | **Reviewing Comic Panels** | Scrolling through panels on `/generate` | *"Notice the sequential consistency: Panel 1 introduces the forest threshold, followed by rising tension, climax, and triumph. Each panel includes scene descriptions, yellow comic caption boxes, narrator text, and speech bubbles."* |
| **3:15 - 3:45** | **PDF Download & Export Success** | Click "Download Your Comic as PDF" | *"Now let's click 'Download Your Comic as PDF'. The file downloads instantly, and we are automatically redirected to our celebratory Export Success page. Opening the PDF, we see a clean, professional 5-page document with exactly one panel per page."* |
| **3:45 - 4:00** | **Conclusion & Future Scope** | GitHub repo & project summary | *"ComicCraft successfully solves the barrier to visual storytelling. Thank you to our mentors and SmartBridge!"* |

---

### 3. Screen Recording Guidelines for Submission
1. **Audio**: Use a quiet room and clear microphone. Speak with steady pacing.
2. **Resolution**: Record full desktop at 1080p (1920x1080) with browser tabs clearly visible.
3. **Sharing Permissions**: When uploading the video to Google Drive:
   - Click **Share**.
   - Change General Access to **"Anyone with the link can view"**.
   - Copy and paste the link into the Google Form submission.
