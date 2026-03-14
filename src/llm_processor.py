import os
from openai import OpenAI

class LLMProcessor:
    def __init__(self, api_key=None, base_url=None, model_id=None):
        if not api_key:
            api_key = os.getenv("OPENROUTER_API_KEY")
        if not base_url:
            base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        if not model_id:
            model_id = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY must be set in environment variables or passed during initialization.")
            
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model_id = model_id

    def generate_report(self, inspection_text, thermal_text):
        system_instruction = """You are an expert AI system tasked with generating a Detailed Diagnostic Report (DDR) for clients based on an Inspection Report and a Thermal Report.

You will receive content extracted from both reports. The content includes raw text and indicators of where images were found, formatted as `[IMAGE_AVAILABLE: path/to/image.png]`. 

Your goal is to build a structured, client-friendly report that merges information logically without duplicate points.

Important Rules:
- Do NOT invent facts not present in the documents.
- If information conflicts between the inspection and thermal reports, you MUST mention the conflict.
- If information is missing for an expected section or detail, write "Not Available".
- Use simple, client-friendly language, avoiding unnecessary technical jargon.
- Embed the extracted images under the appropriate observation or section using Markdown format: `![Description](path/to/image.png)`.
- Use the exact path provided in `[IMAGE_AVAILABLE: path]`.
- Do not include unrelated images. If an expected image is missing, explicitly mention "Image Not Available."

Output Requirements (DDR Structure):
Your generated report must contain the following exact headings. Do not output anything else outside this template:
# Property Issue Summary
# Area-wise Observations
# Probable Root Cause
# Severity Assessment
# Recommended Actions
# Additional Notes
# Missing or Unclear Information
"""

        user_prompt = f"""### Inspection Report Content ###
{inspection_text}

### Thermal Report Content ###
{thermal_text}

Please generate the final DDR Markdown report based on the provided documents.
"""

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Low temperature for factual reporting
        )
        return response.choices[0].message.content
