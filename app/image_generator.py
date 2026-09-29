import os
import re
import math
import hashlib
import urllib.parse
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Attempt to import optional AI libraries
torch_available = False
diffusers_available = False
pipe = None

HF_API_KEY = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")

try:
    import torch
    from diffusers import StableDiffusionPipeline
    # We do not block startup downloading 5GB unless requested or GPU enabled
    if torch.cuda.is_available() or getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        torch_available = True
except Exception:
    pass


def sanitize_filename(prompt: str) -> str:
    """Sanitize prompt into a safe, deterministic filename."""
    clean_sub = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:35]).strip('_')
    hash_str = hashlib.md5(prompt.encode('utf-8')).hexdigest()[:8]
    return f"{clean_sub}_{hash_str}.png"


def _create_procedural_comic_art(prompt: str, output_path: str):
    """
    Creates an evocative, high-aesthetic comic book illustration using Pillow.
    Uses dynamic color harmony, halftone patterns, atmospheric gradients,
    silhouette elements, and comic-book panel borders.
    """
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    width, height = 768, 512
    img = Image.new("RGB", (width, height), "#10131a")
    draw = ImageDraw.Draw(img)

    lower_prompt = prompt.lower()

    # Determine theme palette
    if any(w in lower_prompt for w in ["forest", "nature", "tree", "fox", "wood"]):
        c_top = (18, 48, 38)
        c_mid = (40, 95, 60)
        c_bot = (12, 28, 20)
        accent = (255, 175, 65)
        theme = "NATURE & MYSTERY"
    elif any(w in lower_prompt for w in ["city", "cyber", "future", "neon", "tech"]):
        c_top = (15, 10, 35)
        c_mid = (30, 80, 140)
        c_bot = (200, 30, 110)
        accent = (0, 240, 255)
        theme = "CYBER REALM"
    elif any(w in lower_prompt for w in ["space", "cosmic", "star", "galaxy"]):
        c_top = (5, 5, 20)
        c_mid = (45, 20, 80)
        c_bot = (10, 15, 40)
        accent = (160, 210, 255)
        theme = "COSMIC ODYSSEY"
    elif any(w in lower_prompt for w in ["sunset", "dawn", "desert", "dramatic"]):
        c_top = (60, 20, 45)
        c_mid = (180, 70, 45)
        c_bot = (250, 170, 70)
        accent = (255, 240, 180)
        theme = "DRAMATIC HORIZON"
    else:
        c_top = (25, 25, 45)
        c_mid = (65, 80, 120)
        c_bot = (15, 20, 30)
        accent = (255, 200, 80)
        theme = "EPIC TALE"

    # Draw gradient sky
    for y in range(height):
        t = y / float(height)
        if t < 0.6:
            st = t / 0.6
            r = int(c_top[0] * (1 - st) + c_mid[0] * st)
            g = int(c_top[1] * (1 - st) + c_mid[1] * st)
            b = int(c_top[2] * (1 - st) + c_mid[2] * st)
        else:
            st = (t - 0.6) / 0.4
            r = int(c_mid[0] * (1 - st) + c_bot[0] * st)
            g = int(c_mid[1] * (1 - st) + c_bot[1] * st)
            b = int(c_mid[2] * (1 - st) + c_bot[2] * st)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Comic Halftone effect on upper atmosphere
    halftone_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(halftone_overlay)
    step = 16
    for gx in range(0, width, step):
        for gy in range(0, int(height * 0.55), step):
            dot_radius = int(2.5 * (1.0 - gy / (height * 0.55)))
            if dot_radius > 0:
                h_draw.ellipse(
                    [gx - dot_radius, gy - dot_radius, gx + dot_radius, gy + dot_radius],
                    fill=(255, 255, 255, 30)
                )
    img.paste(Image.alpha_composite(img.convert("RGBA"), halftone_overlay).convert("RGB"), (0, 0))

    # Sun / Moon / Energy Orb
    orb_x, orb_y = int(width * 0.75), int(height * 0.35)
    orb_radius = 65
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    for r in range(orb_radius + 60, orb_radius, -4):
        alpha = int(45 * (1 - (r - orb_radius) / 60))
        g_draw.ellipse([orb_x - r, orb_y - r, orb_x + r, orb_y + r], fill=(accent[0], accent[1], accent[2], alpha))
    g_draw.ellipse([orb_x - orb_radius, orb_y - orb_radius, orb_x + orb_radius, orb_y + orb_radius], fill=(255, 255, 240, 220))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow_layer).convert("RGB"), (0, 0))

    # Distant Silhouette Mountains / Ruins
    mountains = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    m_draw = ImageDraw.Draw(mountains)
    pts = [(0, height)]
    for sx in range(0, width + 50, 40):
        sy = int(height * 0.55 + 40 * math.sin(sx * 0.015) + 20 * math.cos(sx * 0.03))
        pts.append((sx, sy))
    pts.append((width, height))
    m_draw.polygon(pts, fill=(c_top[0] // 2, c_top[1] // 2, c_top[2] // 2, 210))

    # Foreground Silhouette Terrain & Hero Pose
    fore = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(fore)
    fore_pts = [(0, height), (0, int(height * 0.72))]
    for fx in range(0, width + 40, 30):
        fy = int(height * 0.72 + 25 * math.sin(fx * 0.02) + 10 * math.cos(fx * 0.04))
        fore_pts.append((fx, fy))
    fore_pts.append((width, height))
    f_draw.polygon(fore_pts, fill=(10, 12, 18, 255))

    # Silhouette Character (Heroic Stance)
    cx = int(width * 0.32)
    cy = int(height * 0.67)
    # Cape / Aura
    f_draw.polygon([(cx - 8, cy - 25), (cx - 30, cy + 20), (cx + 5, cy + 10)], fill=(accent[0], accent[1], accent[2], 190))
    # Head
    f_draw.ellipse([cx - 8, cy - 40, cx + 8, cy - 24], fill=(12, 14, 20, 255))
    # Torso & Legs
    f_draw.polygon([(cx - 10, cy - 24), (cx + 10, cy - 24), (cx + 12, cy + 12), (cx - 12, cy + 12)], fill=(12, 14, 20, 255))
    f_draw.line([(cx - 6, cy + 12), (cx - 12, cy + 42)], fill=(12, 14, 20, 255), width=6)
    f_draw.line([(cx + 6, cy + 12), (cx + 14, cy + 42)], fill=(12, 14, 20, 255), width=6)

    # Composite layers
    img = Image.alpha_composite(img.convert("RGBA"), mountains)
    img = Image.alpha_composite(img, fore).convert("RGB")

    # Comic Book Border & Frame
    final_draw = ImageDraw.Draw(img)
    # Heavy outer comic border
    final_draw.rectangle([0, 0, width - 1, height - 1], outline=(15, 18, 24), width=8)
    final_draw.rectangle([8, 8, width - 9, height - 9], outline=(255, 255, 255), width=2)

    # Comic Header Stamp
    stamp_w, stamp_h = 240, 30
    final_draw.rectangle([14, 14, 14 + stamp_w, 14 + stamp_h], fill=(20, 22, 30))
    final_draw.rectangle([14, 14, 14 + stamp_w, 14 + stamp_h], outline=accent, width=2)
    final_draw.text((24, 20), f"COMICCRAFT // {theme}", fill=accent)

    # Prompt Synopsis Banner at bottom
    prompt_snip = prompt if len(prompt) < 70 else prompt[:67] + "..."
    bar_y = height - 42
    final_draw.rectangle([14, bar_y, width - 14, bar_y + 26], fill=(15, 18, 25))
    final_draw.rectangle([14, bar_y, width - 14, bar_y + 26], outline=(70, 80, 100), width=1)
    final_draw.text((24, bar_y + 6), f"SCENE: {prompt_snip}", fill=(225, 230, 240))

    img.save(output_path, "PNG", quality=95)


def generate_image(prompt: str, filename: Optional[str] = None) -> str:
    """
    This function creates a comic-style image based on the provided image prompt.
    It sanitizes the prompt for safe filenames, tries high-quality generation,
    and saves the generated image to the static/panels directory.

    Returns the file path to the saved image.
    """
    if not filename:
        filename = sanitize_filename(prompt)

    path = f"static/panels/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Return cached image if already present
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return path

    # 1. Attempt AI Image Generation via Pollinations AI (free, no token needed)
    try:
        import requests
        clean_encoded = urllib.parse.quote(f"comic book panel illustration, {prompt}, masterpiece, 8k")
        pollinations_url = f"https://image.pollinations.ai/prompt/{clean_encoded}?width=768&height=512&seed={abs(hash(prompt)) % 100000}&nologo=true"
        resp = requests.get(pollinations_url, timeout=7)
        if resp.status_code == 200 and len(resp.content) > 10000:
            with open(path, "wb") as f:
                f.write(resp.content)
            return path
    except Exception as e:
        print(f"[Image Gen] External generation skipped/unavailable: {e}")

    # 2. High-fidelity artistic fallback using Pillow
    try:
        _create_procedural_comic_art(prompt, path)
        return path
    except Exception as err:
        print(f"[Image Gen] Procedural generation error: {err}")
        # Absolute minimal image creation so it never crashes
        from PIL import Image
        fallback_img = Image.new("RGB", (768, 512), color=(40, 44, 52))
        fallback_img.save(path)
        return path
