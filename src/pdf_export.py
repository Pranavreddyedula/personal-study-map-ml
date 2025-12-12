from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def export_pdf(study_items, path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Personal Study Map")

    c.setFont("Helvetica", 12)
    y = 700
    for item in study_items:
        c.drawString(50, y, f"- {item['topic']} (score: {item['weight']})")
        y -= 20

        if y < 80:
            c.showPage()
            y = 700

    c.save()
