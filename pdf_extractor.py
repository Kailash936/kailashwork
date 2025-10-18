"""
PDF Data Extractor Module
Extracts customer names and CRNs from PDF documents
"""

import PyPDF2
import re
import pandas as pd
from typing import List, Tuple, Dict

class PDFDataExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.extracted_data = []
    
    def extract_text_from_pdf(self) -> str:
        """Extract all text content from PDF"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                all_text = ""
                
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    all_text += text + "\n"
                
                return all_text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()
    
    def extract_customer_data(self) -> List[Tuple[str, str]]:
        """Extract customer names and CRNs from PDF text"""
        text = self.extract_text_from_pdf()
        if not text:
            return []
        
        # Clean the text
        text = self.clean_text(text)
        
        # Pattern to match customer name and CRN pairs
        # CRN pattern: 10-digit number
        crn_pattern = r'\b\d{10}\b'
        
        # Find all CRNs in the text
        crn_matches = re.findall(crn_pattern, text)
        
        customer_data = []
        
        # Process each CRN match
        for crn in crn_matches:
            # Find the position of this CRN in the text
            crn_pos = text.find(crn)
            
            # Look backwards to find the customer name
            # Go back up to 50 characters to find the name
            start_pos = max(0, crn_pos - 50)
            name_section = text[start_pos:crn_pos].strip()
            
            # Extract the last word sequence that looks like a name
            # Split by spaces and take the last few words that are alphabetic
            words = name_section.split()
            name_words = []
            
            # Go backwards through words to find the name
            for word in reversed(words):
                # Check if word contains mostly letters
                if word.isalpha() or (word.replace('.', '').replace('-', '').isalpha()):
                    name_words.insert(0, word)
                else:
                    break
            
            # Join the name words
            name = ' '.join(name_words).strip()
            
            # Clean up the name
            name = re.sub(r'\s+', ' ', name).strip()
            
            # Validate the name and CRN
            if name and len(name) > 2 and len(crn) == 10 and 'CUSTOMER NAME' not in name.upper():
                customer_data.append((name, crn))
        
        return customer_data
    
    def get_extracted_data(self) -> List[Dict[str, str]]:
        """Get extracted data in dictionary format"""
        raw_data = self.extract_customer_data()
        
        formatted_data = []
        for name, crn in raw_data:
            formatted_data.append({
                'CUSTOMER NAME': name,
                'CRN': crn,
                'PROGRAM': '',
                'RO_NAME': '',
                'MANUFACTURERDESC': '',
                'ASSETCAT': '',
                'MAKE': '',
                'RO_NAME.1': '',
                'ASSESTCAT': '',
                'MANUFACTURER': ''
            })
        
        return formatted_data

def main():
    """Test the extractor"""
    extractor = PDFDataExtractor('/workspace/DOC-20221124-WA0102-1 (1) (1).pdf')
    data = extractor.get_extracted_data()
    
    print(f"Extracted {len(data)} customer records")
    print("\nFirst 5 records:")
    for i, record in enumerate(data[:5]):
        print(f"{i+1}. {record['CUSTOMER NAME']} - {record['CRN']}")

if __name__ == "__main__":
    main()