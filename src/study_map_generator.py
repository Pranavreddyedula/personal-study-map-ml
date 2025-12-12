import os
import zipfile
from data_processing import load_social_json, extract_topics
from pdf_export import export_pdf
from ics_export import export_ics

def generate_study_map(data, out_dir="output"):
    os.makedirs(out_dir, exist_ok=True)

    df = load_social_json(data)
    df = extract_topics(df)

    topic_weights = {}
    for topics in df["topics"]:
        for t in topics:
            topic_weights[t] = topic_weights.get(t, 0) + 1

    study_items = [
        {"topic": t, "weight": score}
        for t, score in sorted(topic_weights.items(), key=lambda x: -x[1])
    ]

    pdf_path = os.path.join(out_dir, "study_map.pdf")
    ics_path = os.path.join(out_dir, "study_plan.ics")

    export_pdf(study_items, pdf_path)
    export_ics(study_items, ics_path)

    zip_path = os.path.join(out_dir, "study-map.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(pdf_path, "study_map.pdf")
        z.write(ics_path, "study_plan.ics")

    return zip_path.replace("\\", "/")
