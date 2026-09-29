import os
from datetime import datetime
from typing import List, Dict, Any
from fpdf import FPDF

EXPORT_FOLDER = "static/exports"
FONT_PATH = "static/fonts/DejaVuSans.ttf"
FONT_BOLD_PATH = "static/fonts/DejaVuSans-Bold.ttf"


class ComicPDF(FPDF):
    def footer(self):
        # Position 12 mm from bottom
        self.set_y(-12)
        font = "DejaVu" if "DejaVu" in self.fonts else "Helvetica"
        self.set_font(font, "", 8.5)
        self.set_text_color(140, 145, 155)
        self.cell(0, 8, f"ComicCraft - AI Comic Book Creator | Page {self.page_no()}", align="C")


def save_pdf(layout: List[Dict[str, Any]]) -> str:
    """
    Compiles the full comic panels, illustrations, and story into a structured multi-page PDF.
    Each panel is carefully positioned onto a single dedicated page.

    Args:
        layout (list): List of dictionaries containing panel number, image path, and text.

    Returns:
        str: File path to the saved PDF.
    """
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    pdf = ComicPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Use DejaVu unicode font if available, fallback to built-in Helvetica
    use_dejavu = False
    if os.path.exists(FONT_PATH):
        try:
            pdf.add_font("DejaVu", "", FONT_PATH)
            if os.path.exists(FONT_BOLD_PATH):
                pdf.add_font("DejaVu", "B", FONT_BOLD_PATH)
            use_dejavu = True
        except Exception as e:
            print(f"[PDF Export] Warning loading DejaVu font: {e}")

    main_font = "DejaVu" if use_dejavu else "Helvetica"

    for panel in layout:
        pdf.add_page()

        # 1. Header / Panel Title
        pdf.set_font(main_font, "B" if use_dejavu else "", 15)
        pdf.set_text_color(20, 20, 20)
        title_text = panel.get("title", f"Panel {panel.get('panel', 1)}")
        if not use_dejavu:
            title_text = title_text.encode("latin-1", "replace").decode("latin-1")
        pdf.cell(0, 8, title_text, ln=True, align="C")

        # Decorative line
        pdf.set_draw_color(239, 68, 68)
        pdf.set_line_width(0.6)
        pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
        pdf.ln(4)

        # 2. Image placement (80mm height to ensure 1 page per panel)
        image_path = panel.get("image_path", "")
        y_image = pdf.get_y()
        image_height = 80
        spacing_after_image = 6

        if os.path.exists(image_path):
            img_x = 20
            img_w = pdf.w - 40
            # Border frame around image
            pdf.set_draw_color(30, 41, 59)
            pdf.set_line_width(0.5)
            pdf.rect(img_x - 1, y_image - 1, img_w + 2, image_height + 2)
            pdf.image(image_path, x=img_x, y=y_image, w=img_w, h=image_height)
            pdf.set_y(y_image + image_height + spacing_after_image)
        else:
            pdf.set_y(y_image + 5)
            pdf.set_font(main_font, "", 10)
            pdf.multi_cell(0, 8, f"[Illustration reference: {image_path}]")
            pdf.set_y(y_image + 20)

        # 3. Scene context (subtle italic / gray)
        scene_desc = panel.get("scene_description", "")
        if scene_desc:
            pdf.set_font(main_font, "", 9)
            pdf.set_text_color(90, 100, 115)
            desc_text = f"Scene Context: {scene_desc}"
            if not use_dejavu:
                desc_text = desc_text.encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 5, desc_text)
            pdf.ln(3)

        # 4. Narrative Story Text
        pdf.set_text_color(25, 30, 40)
        pdf.set_font(main_font, "", 10.5)

        story_text = panel.get("text", "")
        story_lines = story_text.strip().splitlines()

        # Remove duplicate title line if present
        if story_lines and story_lines[0].strip().lower().startswith("**panel"):
            story_lines = story_lines[1:]

        cleaned_text = "\n".join(story_lines).strip()
        if not use_dejavu:
            cleaned_text = cleaned_text.encode("latin-1", "replace").decode("latin-1")

        pdf.multi_cell(0, 6, cleaned_text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)

    return pdf_path
