import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Add the 'src' directory to sys.path to resolve ModuleNotFoundError on Render
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from document_extractor import DocumentExtractor
from llm_processor import LLMProcessor

# Initialize Flask App
# Serving static files from the 'static' folder
app = Flask(__name__, static_folder="../static", static_url_path="/static")
CORS(app)

# Ensure output directory exists before mounting
os.makedirs("output/images", exist_ok=True)
os.makedirs("temp_uploads", exist_ok=True)

@app.route("/")
def serve_frontend():
    return app.send_static_file("index.html")

# Serve generated images to the frontend securely
@app.route("/output/images/<path:filename>")
def serve_output_images(filename):
    # Need absolute route resolution since flask app runs in src/
    output_dir = os.path.abspath(os.path.join(os.getcwd(), "output", "images"))
    from flask import send_from_directory
    return send_from_directory(output_dir, filename)

@app.route("/api/generate", methods=["POST"])
def generate_ddr():
    load_dotenv()
    if not os.getenv("OPENROUTER_API_KEY"):
        return jsonify({"detail": "OPENROUTER_API_KEY environment variable not configured on the server."}), 500

    if "inspection" not in request.files or "thermal" not in request.files:
        return jsonify({"detail": "Missing required files (inspection or thermal)."}), 400

    inspection = request.files["inspection"]
    thermal = request.files["thermal"]

    if inspection.filename == '' or thermal.filename == '':
        return jsonify({"detail": "No selected file"}), 400

    # Save uploaded files temporarily
    insp_path = os.path.join("temp_uploads", inspection.filename)
    therm_path = os.path.join("temp_uploads", thermal.filename)

    inspection.save(insp_path)
    thermal.save(therm_path)

    try:
        extractor = DocumentExtractor(output_img_dir="output/images")
        
        # Extract content
        inspection_text, insp_imgs = extractor.extract(insp_path)
        thermal_text, therm_imgs = extractor.extract(therm_path)

        # Generate report
        processor = LLMProcessor()
        report_markdown = processor.generate_report(inspection_text, thermal_text)

        # Cleanup the temporary PDFs
        os.remove(insp_path)
        os.remove(therm_path)
        
        # Convert local image paths to URL paths that frontend can reach relative to the page
        # The markdown currently has [IMAGE_AVAILABLE: output/images/name.png]
        # and ![]() markdown which resolves cleanly with the route above.

        return jsonify({
            "success": True,
            "markdown": report_markdown,
            "images_extracted": len(insp_imgs) + len(therm_imgs)
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
