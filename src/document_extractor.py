import fitz  # PyMuPDF
import os

class DocumentExtractor:
    def __init__(self, output_img_dir="output/images"):
        self.output_img_dir = output_img_dir
        if not os.path.exists(output_img_dir):
            os.makedirs(output_img_dir)

    def extract(self, pdf_path):
        """
        Extracts text and images from a PDF.
        Returns a formatted string containing the text and image placeholders,
        and a list of image file paths extracted.
        """
        doc_name = os.path.basename(pdf_path).split('.')[0]
        doc = fitz.open(pdf_path)
        
        extracted_content = []
        image_paths = []
        
        img_counter = 1
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract Text
            text = page.get_text("text")
            extracted_content.append(f"--- Page {page_num + 1} ---")
            extracted_content.append(text)
            
            # Extract Images
            image_list = page.get_images(full=True)
            if image_list:
                extracted_content.append(f"\n--- Images on Page {page_num + 1} ---")
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                img_filename = f"{doc_name}_page{page_num+1}_img{img_counter}.{image_ext}"
                img_path = os.path.join(self.output_img_dir, img_filename)
                
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                
                image_paths.append(img_path)
                
                # Append to content so LLM knows this image was on this page
                extracted_content.append(f"[IMAGE_AVAILABLE: {img_path}]")
                
                img_counter += 1
                
        doc.close()
        
        return "\n".join(extracted_content), image_paths

if __name__ == "__main__":
    extractor = DocumentExtractor()
    content, imgs = extractor.extract("../mock_inspection.pdf")
    print(content)
    print("Images:", imgs)
