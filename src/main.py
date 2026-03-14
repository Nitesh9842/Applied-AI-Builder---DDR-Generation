import os
import sys
import argparse
from dotenv import load_dotenv

from document_extractor import DocumentExtractor
from llm_processor import LLMProcessor

def main():
    parser = argparse.ArgumentParser(description="Generate DDR Report from Inspection and Thermal Reports")
    parser.add_argument("--inspection", type=str, required=True, help="Path to Inspection Report PDF")
    parser.add_argument("--thermal", type=str, required=True, help="Path to Thermal Report PDF")
    parser.add_argument("--output", type=str, default="DDR_Report.md", help="Path to output Markdown file")
    
    args = parser.parse_args()

    # Load environment variables (API Key)
    load_dotenv()
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not found. Please set it in a .env file or environment.")
        sys.exit(1)

    print(f"Processing Inspection Report: {args.inspection}")
    print(f"Processing Thermal Report: {args.thermal}")

    extractor = DocumentExtractor()
    
    # 1. Extract content
    try:
        inspection_text, insp_imgs = extractor.extract(args.inspection)
        thermal_text, therm_imgs = extractor.extract(args.thermal)
    except Exception as e:
        print(f"Error extracting documents: {e}")
        sys.exit(1)

    print(f"Extracted {len(insp_imgs)} images from Inspection Report.")
    print(f"Extracted {len(therm_imgs)} images from Thermal Report.")

    # 2. Process with LLM
    print("Generating DDR report using AI...")
    try:
        processor = LLMProcessor()
        report_markdown = processor.generate_report(inspection_text, thermal_text)
    except Exception as e:
        print(f"Error processing with LLM: {e}")
        sys.exit(1)

    # 3. Save report
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_markdown)
        print(f"Success! DDR generated at {args.output}")
    except Exception as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
