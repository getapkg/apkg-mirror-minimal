from flask import Flask, jsonify, send_from_directory, abort
from pathlib import Path
import json

app = Flask(__name__)

# Base folder for releases
RELEASES_DIR = Path(__file__).parent / "releases" / "0.1"
RELEASES_DIR.mkdir(parents=True, exist_ok=True)

# Path to the static packages.json
PKG_JSON_PATH = Path(__file__).parent / "packages.json"

@app.route("/")
def index():
    return "This. is a mirror for getASH"
# Serve packages.json
@app.route("/releases/0.1/packages.json")
def packages_json():
    if not PKG_JSON_PATH.exists():
        return jsonify({"packages": {}})  # empty if file missing
    try:
        with open(PKG_JSON_PATH, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to read packages.json: {e}"}), 500

# Serve ZIP files
@app.route("/releases/0.1/<zipfile>")
def serve_zip(zipfile):
    zip_path = RELEASES_DIR / zipfile
    if zip_path.exists():
        return send_from_directory(RELEASES_DIR, zipfile)
    else:
        abort(404, description="File not found")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
