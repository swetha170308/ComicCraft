import os
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class PromptRequest(BaseModel):
    prompt: str = Field(..., description="Main storyline idea for the comic")
    character_name: str = Field("Hero", description="Hero of the comic")
    setting: str = Field("Enchanted Forest", description="Location/Setting")
    tone: str = Field("Dramatic", description="Mood of the story")
    style: str = Field("Comic Book", description="Visual art style preference")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Loads the homepage where users can submit their story details."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/generate")
async def generate_redirect():
    """Redirects direct GET visits to the creation homepage."""
    return RedirectResponse(url="/", status_code=303)


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    """
    Handles form submission, processes the input using AI models,
    generates the comic panels, builds the layout, compiles the PDF,
    and returns the comic preview page.
    """
    try:
        # Combine user input into a single full prompt
        full_prompt = (
            f"{prompt}\n"
            f"The main character is {character_name}. "
            f"The setting is a {setting}. "
            f"The tone is {tone}. The art style is {style}."
        )

        # Step 1: Generate panel outline
        outline = generate_outline(full_prompt)
        if not isinstance(outline, list) or not all("image_prompt" in panel for panel in outline):
            raise ValueError("Invalid outline structure from Gemini response.")

        # Step 2: Generate story narration and dialogue
        full_story = generate_story(outline)

        # Step 3: Generate images for each panel concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            images = list(executor.map(lambda p: generate_image(p["image_prompt"]), outline))

        # Step 4: Build Layout
        layout = build_comic_layout(images, full_story, outline)

        # Step 5: Export to PDF
        pdf_path = save_pdf(layout)
        web_pdf_path = pdf_path.replace("\\", "/")

        return templates.TemplateResponse("comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_path": web_pdf_path,
            "prompt": prompt,
            "character_name": character_name,
            "setting": setting,
            "tone": tone,
            "style": style
        })

    except Exception as e:
        print(f"[Generate Route Error] {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error_message": f"Unable to generate comic: {str(e)}"
        }, status_code=500)


@router.post("/generate-comic/json")
async def generate_comic_json(req: PromptRequest):
    """
    An API route that accepts JSON payloads, triggers comic generation,
    and returns comic layout data and the generated PDF path.
    """
    try:
        full_prompt = (
            f"{req.prompt}\n"
            f"The main character is {req.character_name}. "
            f"The setting is a {req.setting}. "
            f"The tone is {req.tone}. The art style is {req.style}."
        )

        outline = generate_outline(full_prompt)
        if not isinstance(outline, list) or not all("image_prompt" in panel for panel in outline):
            raise ValueError("Invalid outline structure from Gemini response.")

        full_story = generate_story(outline)

        with ThreadPoolExecutor(max_workers=5) as executor:
            images = list(executor.map(lambda p: generate_image(p["image_prompt"]), outline))

        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)
        web_pdf_path = pdf_path.replace("\\", "/")

        return JSONResponse(content={
            "status": "success",
            "message": "Comic generated successfully",
            "layout": layout,
            "pdf_path": web_pdf_path,
            "character_name": req.character_name,
            "setting": req.setting,
            "tone": req.tone,
            "style": req.style
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    """Serves the generated PDF file for direct download."""
    clean_filename = os.path.basename(filename)
    file_path = os.path.join("static/exports", clean_filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=clean_filename,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{clean_filename}"'}
        )
    raise HTTPException(status_code=404, detail="Requested comic PDF file not found.")


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = ""):
    """Displays a success confirmation page after the comic is downloaded."""
    filename = os.path.basename(pdf_path) if pdf_path else ""
    return templates.TemplateResponse("export_success.html", {
        "request": request,
        "pdf_path": pdf_path,
        "filename": filename
    })


@router.get("/test-image")
async def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, artstation"):
    """Developer utility route to test image generation from a direct prompt."""
    try:
        image_path = generate_image(prompt)
        return {
            "message": "Image generated successfully",
            "path": image_path.replace("\\", "/")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
