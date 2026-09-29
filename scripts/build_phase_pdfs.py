import os
import glob
from fpdf import FPDF
from fpdf.enums import XPos, YPos

font_path = "static/fonts/DejaVuSans.ttf"
font_bold_path = "static/fonts/DejaVuSans-Bold.ttf"

phase_dirs = [
    "1. Brainstorming & Ideation",
    "2. Requirement Analysis",
    "3. Project Design Phase",
    "4. Project Planning Phase",
    "5. Project Development Phase",
    "6.Project Testing",
    "7.Project Documentation",
    "8.Project Demonstration"
]

def main():
    count = 0
    for p_dir in phase_dirs:
        if not os.path.exists(p_dir):
            continue
        for md_file in glob.glob(os.path.join(p_dir, "*.md")):
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            pdf_file = os.path.join(p_dir, f"{base_name}.pdf")

            with open(md_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.set_margins(15, 15, 15)
            pdf.set_auto_page_break(auto=True, margin=15)

            has_font = False
            if os.path.exists(font_path):
                try:
                    pdf.add_font("DejaVu", "", font_path)
                    if os.path.exists(font_bold_path):
                        pdf.add_font("DejaVu", "B", font_bold_path)
                    has_font = True
                except Exception:
                    pass

            main_font = "DejaVu" if has_font else "Helvetica"
            pdf.add_page()

            for line in lines:
                line_str = line.strip()
                if not line_str:
                    pdf.ln(3)
                    continue

                if line_str.startswith("# "):
                    pdf.set_font(main_font, "B" if has_font else "", 15)
                    pdf.set_text_color(220, 38, 38)
                    pdf.cell(pdf.epw, 8, line_str[2:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.ln(2)
                elif line_str.startswith("## "):
                    pdf.set_font(main_font, "B" if has_font else "", 12)
                    pdf.set_text_color(30, 41, 59)
                    pdf.cell(pdf.epw, 7, line_str[3:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.ln(1)
                elif line_str.startswith("### "):
                    pdf.set_font(main_font, "B" if has_font else "", 10.5)
                    pdf.set_text_color(71, 85, 105)
                    pdf.cell(pdf.epw, 6, line_str[4:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                elif line_str.startswith("```") or line_str.startswith("---") or line_str.startswith("==="):
                    pdf.ln(2)
                else:
                    pdf.set_font(main_font, "", 9)
                    pdf.set_text_color(30, 30, 30)
                    # Clean markdown formatting characters
                    clean_text = line_str.replace("*", "").replace("`", "").replace("★", "[*]").replace("⚡", "[!]").replace("🦊", "").replace("🌆", "").replace("🚀", "").replace("🎩", "").replace("🎨", "").replace("📖", "").replace("🎉", "").replace("✨", "").replace("📄", "").replace("💡", "").replace("📥", "").replace("↩", "").replace("💬", "")
                    if not has_font:
                        clean_text = clean_text.encode("latin-1", "replace").decode("latin-1")
                    # Safe multi-cell rendering
                    try:
                        pdf.multi_cell(pdf.epw, 5, clean_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    except Exception:
                        pdf.multi_cell(pdf.epw, 5, clean_text[:100], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.output(pdf_file)
            count += 1
            print(f"Created: {pdf_file}")

    print(f"\nSuccessfully compiled {count} phase PDF deliverables!")

if __name__ == "__main__":
    main()
