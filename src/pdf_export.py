from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from utils import ensure_dir, timestamp_str, logger

def export_pdf(study_items, path, title="Personal Study Map"):
    """
    study_items: list of dicts {topic, weight}
    """
    out_dir = path.rsplit("/",1)[0] if "/" in path else "."
    ensure_dir(out_dir)

    try:
        c = canvas.Canvas(path, pagesize=letter)
        width, height = letter
        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(72, height - 72, title)
        c.setFont("Helvetica", 10)
        c.drawString(72, height - 90, f"Generated: {datetime.utcnow().isoformat()} UTC")

        # Body list
        c.setFont("Helvetica", 12)
        y = height - 120
        for i, it in enumerate(study_items, start=1):
            line = f"{i}. {it.get('topic')} (score: {it.get('weight')})"
            c.drawString(72, y, line)
            y -= 16
            if y < 72:
                c.showPage()
                y = height - 72

        c.save()
        logger.info("Exported PDF to %s", path)
    except Exception as e:
        logger.error("Failed to create PDF: %s", e)
        raise
