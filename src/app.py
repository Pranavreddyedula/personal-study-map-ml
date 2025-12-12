from flask import Flask, request, render_template_string
import json
from study_map_generator import generate_study_map

app = Flask(__name__)

HTML = """
<h2>Personal Study Map Generator</h2>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="datafile" accept=".json" />
  <br><br>
  <button type="submit">Generate Study Map</button>
</form>

{% if link %}
<hr>
<p>Download Output:</p>
<a href="{{link}}">study-map.zip</a>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    link = None

    if request.method == "POST":
        if "datafile" not in request.files:
            return render_template_string(HTML, link=None)

        f = request.files["datafile"]
        data = json.load(f)

        zip_path = generate_study_map(data, out_dir="output")
        link = "/" + zip_path

    return render_template_string(HTML, link=link)

@app.route("/output/<path:filename>")
def download(filename):
    from flask import send_from_directory
    return send_from_directory("output", filename)

if __name__ == "__main__":
    app.run(debug=True)
