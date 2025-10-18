"""
Data Processing and Validation Module
Handles data cleaning, validation, and formatting
"""

import re
import pandas as pd
from typing import List, Dict, Tuple

class DataProcessor:
    def __init__(self):
        self.validation_errors = []
        self.processed_data = []
    
    def validate_crn(self, crn: str) -> bool:
        """Validate CRN format"""
        # CRN should be 10 digits
        if not crn.isdigit() or len(crn) != 10:
            return False
        return True
    
    def validate_name(self, name: str) -> bool:
        """Validate customer name format"""
        # Name should contain only letters, spaces, and common punctuation
        if not name or len(name.strip()) < 2:
            return False
        
        # Check if name contains mostly alphabetic characters
        alpha_chars = sum(1 for c in name if c.isalpha())
        total_chars = len(name.replace(' ', ''))
        
        if total_chars == 0:
            return False
        
        return (alpha_chars / total_chars) >= 0.7
    
    def clean_name(self, name: str) -> str:
        """Clean and normalize customer name"""
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name.strip())
        
        # Remove special characters except spaces and common punctuation
        name = re.sub(r'[^\w\s.-]', '', name)
        
        # Title case the name
        name = name.title()
        
        return name
    
    def clean_crn(self, crn: str) -> str:
        """Clean and normalize CRN"""
        # Remove all non-digit characters
        crn = re.sub(r'\D', '', crn)
        
        # Ensure it's exactly 10 digits
        if len(crn) == 10:
            return crn
        elif len(crn) > 10:
            return crn[:10]
        else:
            return crn.zfill(10)
    
    def process_customer_data(self, raw_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Process and validate customer data"""
        processed_data = []
        errors = []
        
        for i, record in enumerate(raw_data):
            try:
                # Clean and validate name
                original_name = record['CUSTOMER NAME']
                cleaned_name = self.clean_name(original_name)
                
                if not self.validate_name(cleaned_name):
                    errors.append(f"Row {i+1}: Invalid name format - '{original_name}'")
                    continue
                
                # Clean and validate CRN
                original_crn = record['CRN']
                cleaned_crn = self.clean_crn(original_crn)
                
                if not self.validate_crn(cleaned_crn):
                    errors.append(f"Row {i+1}: Invalid CRN format - '{original_crn}'")
                    continue
                
                # Create processed record
                processed_record = {
                    'CUSTOMER NAME': cleaned_name,
                    'CRN': cleaned_crn,
                    'PROGRAM': record.get('PROGRAM', ''),
                    'RO_NAME': record.get('RO_NAME', ''),
                    'MANUFACTURERDESC': record.get('MANUFACTURERDESC', ''),
                    'ASSETCAT': record.get('ASSETCAT', ''),
                    'MAKE': record.get('MAKE', ''),
                    'RO_NAME.1': record.get('RO_NAME.1', ''),
                    'ASSESTCAT': record.get('ASSESTCAT', ''),
                    'MANUFACTURER': record.get('MANUFACTURER', '')
                }
                
                processed_data.append(processed_record)
                
            except Exception as e:
                errors.append(f"Row {i+1}: Processing error - {str(e)}")
        
        self.validation_errors = errors
        self.processed_data = processed_data
        
        return processed_data
    
    def get_validation_report(self) -> Dict[str, any]:
        """Get validation report"""
        return {
            'total_records': len(self.processed_data),
            'errors': self.validation_errors,
            'error_count': len(self.validation_errors),
            'success_rate': len(self.processed_data) / (len(self.processed_data) + len(self.validation_errors)) * 100 if (len(self.processed_data) + len(self.validation_errors)) > 0 else 0
        }
    
    def remove_duplicates(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Remove duplicate records based on CRN"""
        seen_crns = set()
        unique_data = []
        
        for record in data:
            crn = record['CRN']
            if crn not in seen_crns:
                seen_crns.add(crn)
                unique_data.append(record)
        
        return unique_data

def main():
    """Test the processor"""
    # Sample data for testing
    sample_data = [
        {'CUSTOMER NAME': 'AANCHAL JOSHI', 'CRN': '5041885433', 'PROGRAM': '', 'RO_NAME': '', 'MANUFACTURERDESC': '', 'ASSETCAT': '', 'MAKE': '', 'RO_NAME.1': '', 'ASSESTCAT': '', 'MANUFACTURER': ''},
        {'CUSTOMER NAME': 'AIMAN ALI', 'CRN': '5111926597', 'PROGRAM': '', 'RO_NAME': '', 'MANUFACTURERDESC': '', 'ASSETCAT': '', 'MAKE': '', 'RO_NAME.1': '', 'ASSESTCAT': '', 'MANUFACTURER': ''},
        {'CUSTOMER NAME': 'invalid name 123', 'CRN': '123', 'PROGRAM': '', 'RO_NAME': '', 'MANUFACTURERDESC': '', 'ASSETCAT': '', 'MAKE': '', 'RO_NAME.1': '', 'ASSESTCAT': '', 'MANUFACTURER': ''}
    ]
    
    processor = DataProcessor()
    processed = processor.process_customer_data(sample_data)
    
    print("Processed data:")
    for record in processed:
        print(f"{record['CUSTOMER NAME']} - {record['CRN']}")
    
    report = processor.get_validation_report()
    print(f"\nValidation Report:")
    print(f"Total records: {report['total_records']}")
    print(f"Errors: {report['error_count']}")
    print(f"Success rate: {report['success_rate']:.1f}%")

if __name__ == "__main__":
    main()