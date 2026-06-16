import re
import json
import os
import subprocess
import base64
from typing import Dict, Any, Optional

# ==============================================================================
# CONFIGURATION: Dynamic Schema
# ==============================================================================
EXTRACTION_SCHEMA = {
    "issuer": {"label": "Cơ quan ban hành", "patterns": [r"^([^\n\r]+)"]},
    "number": {"label": "Số hiệu", "patterns": [r"Số:\s*([^\n\r]+)", r"Số\s*([^\n\r]+)"]},
    "date": {"label": "Ngày ban hành", "patterns": [r"ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})"]},
    "subject": {"label": "Trích yếu", "patterns": [r"(?:V/v|Về việc)\s*(.*?)(?=\n|\.|$)", "Tóm tắt nội dung chính của văn bản"]},
    "deadline": {"label": "Thời hạn", "patterns": [
        r"hiệu lực\s*từ\s*ngày\s*(\d{1,2}\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4}))",
        r"trước\s*ngày\s*(\d{1,2}\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4}))",
        r"hoàn thành\s*trước\s*ngày\s*(\d{1,2}\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4}))",
    ]}
}

INPUT_LIMIT = 10000 
TEXT_THRESHOLD = 200 # Increased threshold to avoid noise from footers

class LegalVisionExtractor:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def _preprocess(self, text: str) -> str:
        if not text: return ""
        return text[:INPUT_LIMIT].replace('\r', '\n')

    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        # Step 1: Try extracting text using pdftotext
        text = ""
        try:
            result = subprocess.run(['pdftotext', '-l', '3', pdf_path, '-'], capture_output=True, text=True, encoding='utf-8')
            text = result.stdout
        except Exception:
            pass

        # Check if text is substantial
        is_text_rich = len(text.strip()) >= TEXT_THRESHOLD
        
        # Try extracting even if it's not "rich" to see if we get something useful
        extracted_data_str = self._extract_from_text(text)
        extracted_data = json.loads(extracted_data_str)
        
        # If it's not text-rich OR the extraction failed to find key info (issuer OR number)
        if not is_text_rich or (extracted_data.get("issuer") == "Unknown" or extracted_data.get("number") == "Unknown" or len(str(extracted_data.get("issuer", ""))) < 3):
            # TRIGGER VISION FALLBACK
            try:
                img_output_prefix = f"/tmp/vision_{os.path.basename(pdf_path)}"
                subprocess.run(['pdftoppm', '-singlefile', '-png', '-r', '150', pdf_path, img_output_prefix], check=True)
                img_path = f"{img_output_prefix}.png"

                with open(img_path, "rb") as img_file:
                    base64_img = base64.b64encode(img_file.read()).decode('utf-8')

                return {
                    "status": "scan_detected",
                    "vision_required": True,
                    "image_path": img_path,
                    "base64_payload": base64_img,
                    "message": "Vision payload ready. Use Vision API to parse."
                }
            except Exception as e:
                return {"status": "error", "message": f"Vision preparation failed: {str(e)}"}
        
        return {
            "status": "text_extracted",
            "data": extracted_data_str,
            "vision_required": False
        }

    def _extract_from_text(self, raw_text: str) -> str:
        text = self._preprocess(raw_text)
        results = {}
        for field_key, config in self.schema.items():
            patterns = config.get("patterns", [])
            found_value = "Unknown"
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.S)
                if match:
                    found_value = match.group(0).strip() if not match.groups() else match.group(1).strip()
                    break
            results[field_key] = found_value
        return json.dumps(results, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    extractor = LegalVisionExtractor(EXTRACTION_SCHEMA)
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path.lower().endswith('.pdf'):
            print(json.dumps(extractor.process_pdf(path), ensure_ascii=False, indent=2))
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    print(extractor._extract_from_text(f.read()))
            except:
                print(extractor._extract_from_text(sys.argv[1]))
    else:
        print(json.dumps({"error": "No input provided"}, indent=2))
