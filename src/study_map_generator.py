import os
import zipfile
from datetime import datetime
from data_processing import load_social_json, extract_topics
from pdf_export import export_pdf
from ics_export import export_ics
from utils import ensure_dir, safe_filename, timestamp_str, logger

def _unique_basename(prefix="study_map"):
    return f"{safe_filename(prefix)}_{timestamp_str()}"

def generate_study_map(data, out_dir="output"):
    """
    Orchestrates creation of study_map.pdf, study_plan.ics and a zip.
    Returns the full zip path (so app can serve it).
    """
    ensure_dir(out_dir)
    try:
        df = load_social_json(data)
    except Exception as e:
        logger.error("Failed to load social json: %s", e)
        raise

    topics = extract_topics(df, prefer_hashtags=True, top_n=20)

    # filenames
    base = _unique_basename("study_map")
    pdf_path = os.path.join(out_dir, f"{base}.pdf")
    ics_path = os.path.join(out_dir, f"{base}.ics")
    zip_path = os.path.join(out_dir, f"{base}.zip")

    # create artifacts
    try:
        export_pdf(topics, pdf_path)
        export_ics(topics, ics_path)
    except Exception as e:
        logger.error("Failed to export artifacts: %s", e)
        raise

    # make a zip containing both
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(pdf_path, arcname=os.path.basename(pdf_path))
            z.write(ics_path, arcname=os.path.basename(ics_path))
        logger.info("Created zip: %s", zip_path)
    except Exception as e:
        logger.error("Failed to create zip: %s", e)
        raise

    return zip_path
