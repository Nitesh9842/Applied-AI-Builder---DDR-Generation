# Applied AI Builder - DDR Report Generation

This AI system automates the generation of a client-ready Detailed Diagnostic Report (DDR) by intelligently fusing data from an Inspection Report and a Thermal Report. It utilizes Gemini 2.5 Flash and PyMuPDF to extract text and images, synthesizing them into a structured Markdown format without hallucinating facts.

## Features
- **Integrated Image & Text Extraction**: Parses PDF documents to extract raw text and local images.
- **Smart Formatting**: Dynamically embeds extracted image links (`![Description](path/to/img)`) correctly into the appropriate Area-wise Observations so that findings are visually supported.
- **Conflict Handling**: Identifies discrepancies between thermal and visual inspections.
- **Missing Info Resolution**: Automatically declares `Not Available` for missing expected values.

## Project Structure
```text
├── src/
│   ├── document_extractor.py   # Extracts text and local images from PDFs
│   ├── llm_processor.py        # Gemini 2.5 API integration and prompting
│   └── main.py                 # CLI orchestration script
├── requirements.txt            # Project dependencies
├── .env.example                # Sample environment variables config
└── README.md                   # Project documentation
```

## Setup & Execution

### 1. Install Dependencies
Ensure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Rename `.env.example` to `.env` and insert your active OpenRouter API key.
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4o-mini
```

### 3. Run the System

You can run the application using either the Command Line Interface or the Modern Web Backend.

#### Option A: Web Interface (Recommended)
Launch the Flask server:
```bash
cd src
python app.py
```
Then, navigate to `http://127.0.0.1:5000` in your web browser to upload the PDF documents and generate the report natively.

#### Option B: Command Line Interface
Pass the file paths for the respective reports to the CLI:
```bash
python src/main.py --inspection path/to/Inspection_Report.pdf --thermal path/to/Thermal_Report.pdf --output DDR_Report.md
```
The script will save extracted images in an `output/images/` folder relative to where it was executed, and generate the final client-ready `DDR_Report.md` document natively linking them!
