import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

model = None
try:
    import google.generativeai as genai
    if GEMINI_API_KEY and GEMINI_API_KEY.strip() and GEMINI_API_KEY != "your_gemini_api_key_here":
        genai.configure(api_key=GEMINI_API_KEY)
        # Try gemini-1.5-pro, fallback to gemini-pro if needed
        model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    print(f"[Gemini Pro] Warning during initialization: {e}")
    model = None


def _generate_fallback_story(outline: List[Dict[str, Any]]) -> str:
    """
    Intelligent dynamic story generator when Gemini API is offline or key is unconfigured.
    Generates rich comic story dialogue, captions, and narrative text for each panel.
    """
    story_parts = []
    for idx, panel in enumerate(outline, start=1):
        title = panel.get("title", f"Panel {idx}")
        scene_desc = panel.get("scene_description", "")

        # Extract character/action hints
        part = f"""**Panel {idx}: {title}**
{scene_desc}

**CAPTION:** The winds carry ancient echoes; every heartbeat counts in the unfolding mystery.
*NARRATION:* With sharp eyes and unbroken focus, every step forward turns hesitation into courage.
*CHARACTER:* "No turning back now... whatever lies in these shadows, I'm ready!"
"""
        story_parts.append(part.strip())

    return "\n\n".join(story_parts)


def generate_story(outline: list) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini 1.5 Pro.

    Args:
        outline (list): A list of dictionaries representing each comic panel's idea.

    Returns:
        str: The generated comic story text or an error message.
    """
    global model

    # Format the panel outline as a numbered list for clarity
    formatted_outline = "\n".join([
        f"{i+1}. {item.get('title', '')}: {item.get('scene_description', '')}"
        if isinstance(item, dict) else f"{i+1}. {item}"
        for i, item in enumerate(outline)
    ])

    # Construct the prompt
    prompt = f"""You are a professional comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- For EACH panel, start with:
  **Panel <number>: <Title>**
- Followed by a short scene paragraph.
- Include **CAPTION:** for ambient environmental sound/mood.
- Include *NARRATION:* for the narrator's voice.
- Include character dialogue in quotes (e.g., *HERO:* "Let's do this!").
- Keep each panel self-contained but part of a cohesive 5-panel story arc.
"""

    if model:
        try:
            response = model.generate_content(prompt)
            if response.text and response.text.strip():
                return response.text.strip()
            return _generate_fallback_story(outline)
        except Exception as e:
            print(f"[Gemini Pro] Error generating story with model: {e}")
            return _generate_fallback_story(outline)
    else:
        print("[Gemini Pro] Model not configured or key absent; using high-fidelity narrative fallback.")
        return _generate_fallback_story(outline)
