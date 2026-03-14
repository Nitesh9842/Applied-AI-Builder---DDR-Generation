import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw

def create_image(filename, text, color):
    # Create a simple image with text
    img = Image.new('RGB', (400, 300), color=color)
    d = ImageDraw.Draw(img)
    d.text((50, 150), text, fill=(0, 0, 0))
    img.save(filename)

def generate_inspection_report(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Site Inspection Report")
    
    # Section 1
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "1. Roof Area Observation")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 120, "Observation: The main roof area shows signs of water pooling near the HVAC unit.")
    c.drawString(50, height - 135, "Probable Root Cause: Blocked drainage pipe under the unit.")
    c.drawString(50, height - 150, "Severity: High.")
    c.drawString(50, height - 165, "Recommended Action: Clear the blockage and inspect for structural damage.")
    
    create_image("roof_image.png", "Roof - Water Pooling", (200, 200, 255))
    c.drawImage("roof_image.png", 50, height - 480, width=300, height=200)
    
    c.showPage()
    
    # Section 2
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "2. Basement Wall Observation")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 120, "Observation: Cracks observed on the north-facing basement wall.")
    c.drawString(50, height - 135, "Probable Root Cause: Soil settlement.")
    c.drawString(50, height - 150, "Severity: Medium.")
    
    create_image("basement_image.png", "Basement Crack", (255, 200, 200))
    c.drawImage("basement_image.png", 50, height - 380, width=300, height=200)
    
    c.save()

def generate_thermal_report(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Thermal Image Report")
    
    # Section 1 corresponding to roof
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Thermal Finding - Roof HVAC")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 120, "Temperature reading near the HVAC unit indicates cold spots (potential moisture).")
    c.drawString(50, height - 135, "Max Temp: 28C, Min Temp: 12C. Delta T: 16C.")
    
    create_image("roof_thermal.png", "Thermal Image - Roof", (100, 100, 200))
    c.drawImage("roof_thermal.png", 50, height - 350, width=300, height=200)
    
    c.showPage()
    
    # Section 2 corresponding to electrical panel (new finding not in inspection)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Thermal Finding - Main Electrical Panel")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 120, "Breaker #4 shows abnormal heating.")
    c.drawString(50, height - 135, "Max Temp: 65C. Recommended Action: immediate inspection by electrician.")
    
    create_image("electrical_thermal.png", "Thermal Image - Panel", (255, 100, 100))
    c.drawImage("electrical_thermal.png", 50, height - 350, width=300, height=200)
    
    c.save()

if __name__ == "__main__":
    generate_inspection_report("mock_inspection.pdf")
    generate_thermal_report("mock_thermal.pdf")
    
    # Cleanup temporary images
    for img in ["roof_image.png", "basement_image.png", "roof_thermal.png", "electrical_thermal.png"]:
        if os.path.exists(img):
            os.remove(img)
    
    print("Generated mock_inspection.pdf and mock_thermal.pdf")
