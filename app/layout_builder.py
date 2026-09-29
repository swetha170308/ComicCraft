import re
from typing import List, Dict, Any


def build_comic_layout(
    image_paths: List[str], full_story: str, outline: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Organizes generated images, panel outlines, and story text into a structured layout.

    Args:
        image_paths (list): List of file paths to generated panel images.
        full_story (str): Complete narrative text generated for the comic.
        outline (list): List of panel outline dictionaries.

    Returns:
        List[dict]: Formatted layout dictionaries for template rendering and PDF export.
    """
    # Split the full story into individual panel segments
    story_panels = full_story.split("**Panel")
    story_panels = [f"**Panel{p}" for p in story_panels if p.strip()]

    # Fallback if split didn't find **Panel headers
    if len(story_panels) < len(outline):
        story_panels = [p for p in full_story.split("\n\n") if p.strip()]
        while len(story_panels) < len(outline):
            idx = len(story_panels) + 1
            story_panels.append(
                f"**Panel {idx}**\n*NARRATION:* The journey continues through the mysterious realm."
            )

    layout = []
    for idx, (image, raw_text, panel_info) in enumerate(
        zip(image_paths, story_panels, outline), start=1
    ):
        lines = raw_text.strip().splitlines()
        # Remove title line like "**Panel 1: Title**" if present
        if lines and lines[0].strip().lower().startswith("**panel"):
            body_text = "\n".join(lines[1:]).strip()
        else:
            body_text = raw_text.strip()

        # Parse caption, narration, and dialogue for rich UI display
        caption_match = re.search(r"\*\*CAPTION:\*\*\s*(.+)", body_text, re.IGNORECASE)
        narration_match = re.search(r"\*NARRATION:\*\s*(.+)", body_text, re.IGNORECASE)
        char_dialogue_match = re.search(r"\*([A-Z0-9_\s]+):\*\s*\"?([^\"]+)\"?", body_text)

        caption = caption_match.group(1).strip() if caption_match else ""
        narration = narration_match.group(1).strip() if narration_match else ""
        character_line = ""
        if char_dialogue_match and char_dialogue_match.group(1).upper() not in ["CAPTION", "NARRATION"]:
            character_line = f'{char_dialogue_match.group(1)}: "{char_dialogue_match.group(2)}"'

        title = panel_info.get("title", f"Panel {idx}")
        # Clean title if it already starts with "Panel X:"
        if title.lower().startswith(f"panel {idx}:"):
            display_title = title
        else:
            display_title = f"Panel {idx}: {title}"

        layout.append({
            "panel": idx,
            "title": display_title,
            "raw_title": panel_info.get("title", f"Panel {idx}"),
            "image_path": image,
            "text": body_text,
            "scene_description": panel_info.get("scene_description", ""),
            "image_prompt": panel_info.get("image_prompt", ""),
            "caption": caption,
            "narration": narration,
            "dialogue": character_line,
        })

    return layout
