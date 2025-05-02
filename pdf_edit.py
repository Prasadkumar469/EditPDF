import fitz  # PyMuPDF

def replace_text_preserving_format_single(page, old_text, new_text):
    # Default values
    font_size = 12
    font_name = "helv"  # fallback font
    font_color = (0, 0, 0)

    # Try to extract original span attributes
    spans = page.get_text("dict")["blocks"]
    found = False
    for block in spans:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if old_text in span["text"]:
                    font_size = span["size"]
                    font_name = span["font"]
                    color_int = span["color"]
                    r = (color_int >> 16) & 255
                    g = (color_int >> 8) & 255
                    b = color_int & 255
                    font_color = (r / 255, g / 255, b / 255)
                    found = True
                    break
            if found:
                break
        if found:
            break

    # Cover original text
    text_instances = page.search_for(old_text)
    for inst in text_instances:
        rect = fitz.Rect(inst)
        page.draw_rect(rect, fill=(1, 1, 1), color=None, overlay=True)

        # Insert replacement text
        x, y = rect.x0, rect.y1 - 3  # lower the baseline more
        page.insert_text(
            (x, y),
            new_text,
            fontname=font_name,
            fontsize=font_size,
            color=font_color,
            overlay=True
        )

def replace_text_preserving_format(input_pdf, output_pdf, replacements):
    doc = fitz.open(input_pdf)
    for page in doc:
        for old_text, new_text in replacements:
            replace_text_preserving_format_single(page, old_text, new_text)

    doc.save(output_pdf)
    print(f"✅ Output saved to: {output_pdf}")

# Example usage
replacements = [
    ("90 days", "60 days"),
    ("(90)", "(60)"),
    ("Ninety days", "Sixty days")
]

replace_text_preserving_format("C:\\code\\training\\may\\output.pdf", "output1.pdf", replacements)
