# src/app.py
import os
import json
from flask import Flask, request, render_template_string, send_from_directory, url_for
from study_map_generator import generate_study_map
from pdf_processing import extract_text_from_pdf
from mindmap_generator import generate_mindmap_from_text

app = Flask(__name__)

INDEX_HTML = """
<h2>Personal Study Map Generator</h2>
<p>Choose a sample JSON or upload one (generates PDF + ICS) — OR upload a PDF to generate a mind-map image.</p>

<h3>Option A — JSON (study map)</h3>
<form method="post" enctype="multipart/form-data">
  <fieldset>
    <legend><strong>JSON input</strong></legend>
    {% if samples %}
      <div>
        {% for s in samples %}
          <label style="display:block; margin:6px 0;">
            <input type="radio" name="sample" value="{{s}}" {% if loop.first %}checked{% endif %}> {{s}}
            &nbsp;<a href="{{ url_for('serve_data_file', filename=s) }}" target="_blank">view</a>
          </label>
        {% endfor %}
      </div>
    {% endif %}
    <input type="file" name="datafile" accept=".json" />
    <br/><br/>
    <button name="action" value="generate_json" type="submit">Generate Study Map</button>
  </fieldset>
</form>

<hr>
<h3>Option B — PDF (mind map)</h3>
<form method="post" enctype="multipart/form-data">
  <fieldset>
    <legend><strong>Upload PDF</strong></legend>
    <input type="file" name="pdffile" accept=".pdf" />
    <br/><br/>
    <button name="action" value="generate_pdf" type="submit">Generate Mind Map</button>
  </fieldset>
</form>

{% if link %}
<hr>
<p>Download output:</p>
<a href="{{link}}">{{ link }}</a>
{% endif %}
"""

def list_sample_files():
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        return []
    return [fn for fn in sorted(os.listdir(data_dir)) if fn.lower().endswith(".json")]

@app.route("/", methods=["GET", "POST"])
def index():
    samples = list_sample_files()
    link = None

    if request.method == "POST":
        action = request.form.get("action")
        # JSON -> study map
        if action == "generate_json":
            uploaded = request.files.get("datafile")
            if uploaded and uploaded.filename:
                try:
                    data = json.load(uploaded)
                except Exception as e:
                    return f"Failed to parse uploaded JSON: {e}", 400
            else:
                selected = request.form.get("sample")
                if selected and selected in samples:
                    sample_path = os.path.join(os.getcwd(), "data", selected)
                    try:
                        with open(sample_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    except Exception as e:
                        return f"Failed to load sample file: {e}", 500
                else:
                    return "No datafile uploaded and no sample selected.", 400

            zip_path = generate_study_map(data, out_dir="output")
            link = url_for("download_output", filename=os.path.basename(zip_path))

        # PDF -> mind map
        elif action == "generate_pdf":
            pdf = request.files.get("pdffile")
            if not pdf or not pdf.filename:
                return "No PDF uploaded.", 400
            # extract text
            try:
                text = extract_text_from_pdf(pdf)
            except Exception as e:
                return f"Failed to extract text from PDF: {e}", 500

            # generate mindmap
            try:
                out_path, top_terms = generate_mindmap_from_text(text, out_dir="output", basename="mindmap")
            except Exception as e:
                return f"Failed to generate mind map: {e}", 500

            link = url_for("download_output", filename=os.path.basename(out_path))

    return render_template_string(INDEX_HTML, samples=samples, link=link)

@app.route("/data/<path:filename>")
def serve_data_file(filename):
    data_dir = os.path.join(os.getcwd(), "data")
    return send_from_directory(data_dir, filename)

@app.route("/output/<path:filename>")
def download_output(filename):
    out_dir = os.path.join(os.getcwd(), "output")
    return send_from_directory(out_dir, filename, as_attachment=True)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
