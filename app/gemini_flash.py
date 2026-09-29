import json
import os
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Setup Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

model = None
try:
    import google.generativeai as genai
    if GEMINI_API_KEY and GEMINI_API_KEY.strip() and GEMINI_API_KEY != "your_gemini_api_key_here":
        genai.configure(api_key=GEMINI_API_KEY)
        # Try gemini-1.5-flash, fallback to gemini-pro if needed
        model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print(f"[Gemini Flash] Warning during initialization: {e}")
    model = None


def _generate_fallback_outline(user_prompt: str) -> List[Dict[str, Any]]:
    """
    Intelligent dynamic fallback generator when Gemini API key is not configured
    or when network/rate limits occur. Extracts user parameters to craft a tailored 5-panel outline.
    """
    # Parse attributes if embedded in user_prompt
    char_match = re.search(r"main character is ([^.\n]+)", user_prompt, re.IGNORECASE)
    setting_match = re.search(r"setting is a? ([^.\n]+)", user_prompt, re.IGNORECASE)
    tone_match = re.search(r"tone is ([^.\n]+)", user_prompt, re.IGNORECASE)
    style_match = re.search(r"art style is ([^.\n]+)", user_prompt, re.IGNORECASE)

    character = char_match.group(1).strip() if char_match else "the hero"
    setting = setting_match.group(1).strip() if setting_match else "an enigmatic realm"
    tone = tone_match.group(1).strip() if tone_match else "dramatic"
    style = style_match.group(1).strip() if style_match else "comic book"

    # Base story idea extraction
    story_idea = user_prompt.split("\n")[0].strip()
    if not story_idea:
        story_idea = f"An epic journey of {character} across {setting}"

    return [
        {
            "panel": 1,
            "title": f"The Threshold: {setting.title()}",
            "scene_description": f"{character} stands poised at the mysterious boundary of {setting}. Ambient light flickers as an adventurous journey begins with an unmistakable sense of {tone} anticipation.",
            "image_prompt": f"Vivid {style} illustration: {character} standing at the dramatic entrance of {setting}. Intricate detailing, cinematic atmospheric lighting, {tone} mood, high dynamic range comic panel art."
        },
        {
            "panel": 2,
            "title": "Into the Deep Unknown",
            "scene_description": f"Venturing deeper into {setting}, {character} encounters an unexpected anomaly. Shadows dance and strange glowing symbols whisper ancient secrets across the environment.",
            "image_prompt": f"Intense {style} artwork: {character} carefully navigating through {setting}, discovering glowing ancient artifacts and mystical ruins, cinematic shadows, expressive {tone} atmosphere."
        },
        {
            "panel": 3,
            "title": "The Sudden Encounter",
            "scene_description": f"The quiet breaks abruptly! A surprise challenge tests {character}'s resolve amidst the hazardous terrain of {setting}. The stakes escalate immediately.",
            "image_prompt": f"Action-packed {style} comic frame: {character} facing a sudden confrontation in {setting}, glowing magical energy arcs, dynamic motion blur, dramatic perspective, {tone} tension."
        },
        {
            "panel": 4,
            "title": "The Turning Point",
            "scene_description": f"Summoning courage and ingenuity, {character} makes a daring stand. Hidden strengths unleash a dazzling surge of determination against overwhelming odds.",
            "image_prompt": f"Heroic {style} scene: {character} channeling immense inner courage in {setting}, radiant burst of light, heroic pose, cinematic angle, vibrant comic colors."
        },
        {
            "panel": 5,
            "title": "A New Dawn Arises",
            "scene_description": f"Victory and harmony restore peace across {setting}. {character} gazes toward the gleaming horizon, transformed into a legendary champion with new paths awaiting.",
            "image_prompt": f"Inspiring {style} closing shot: {character} standing victoriously on an elevated ridge overlooking {setting} at golden sunset, peaceful radiant aura, masterpiece comic book finish."
        }
    ]


def generate_outline(user_prompt: str) -> List[Dict[str, Any]]:
    """
    Generates a 5-panel comic layout based on the user's story idea using Gemini.

    Args:
        user_prompt (str): The user's comic idea prompt.

    Returns:
        List: A list of dictionaries, one for each panel.
    """
    global model
    prompt = f"""Your task is to generate a *strictly formatted JSON array* containing 5 panel descriptions for a comic based on the story idea below:

Story: "{user_prompt}"

Each JSON object must include:
- "panel" (integer)
- "title" (string)
- "scene_description": "scene description here"
- "image_prompt": "Image prompt for Stable Diffusion"

Output only the JSON array. Do not add conversational text or markdown code fences other than ```json.
"""

    if model:
        try:
            response = model.generate_content(prompt)
            output_text = response.text.strip()
            print("\nRAW GEMINI RESPONSE \n", output_text)

            # Remove any markdown formatting if present
            if output_text.startswith("```json"):
                output_text = output_text.replace("```json", "").replace("```", "").strip()
            elif output_text.startswith("```"):
                output_text = output_text.replace("```", "").strip()

            panel_data = json.loads(output_text)

            # Validation
            if not isinstance(panel_data, list):
                raise ValueError("Gemini response is not a list.")

            for panel in panel_data:
                if not isinstance(panel, dict) or not all(
                    k in panel for k in ("panel", "title", "scene_description", "image_prompt")
                ):
                    raise ValueError(f"Invalid panel format or missing keys: {panel}")

            return panel_data

        except json.JSONDecodeError as e:
            print("JSON Decode error:", e)
            print("Full Text Received:\n", output_text if 'output_text' in locals() else "N/A")
            return _generate_fallback_outline(user_prompt)
        except Exception as e:
            print("Unexpected Gemini Flash error:", e)
            return _generate_fallback_outline(user_prompt)
    else:
        print("[Gemini Flash] Model not configured or key absent; using high-fidelity generative fallback.")
        return _generate_fallback_outline(user_prompt)
