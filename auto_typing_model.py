"""
Main Auto-Typing Model
Complete solution for extracting PDF data and populating Excel files
"""

import os
import sys
from datetime import datetime
from pdf_extractor import PDFDataExtractor
from data_processor import DataProcessor
from excel_writer import ExcelWriter

class AutoTypingModel:
    def __init__(self, pdf_path: str, excel_template_path: str = None, output_path: str = None):
        self.pdf_path = pdf_path
        self.excel_template_path = excel_template_path
        self.output_path = output_path or f"auto_typed_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Initialize components
        self.extractor = PDFDataExtractor(pdf_path)
        self.processor = DataProcessor()
        self.writer = ExcelWriter(self.output_path)
        
        # Processing statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'extraction_time': 0,
            'processing_time': 0,
            'writing_time': 0,
            'total_records': 0,
            'valid_records': 0,
            'error_records': 0
        }
    
    def run(self) -> bool:
        """Run the complete auto-typing process"""
        print("=" * 60)
        print("AUTO-TYPING MODEL - Starting Process")
        print("=" * 60)
        
        self.stats['start_time'] = datetime.now()
        
        try:
            # Step 1: Extract data from PDF
            print("\n1. Extracting data from PDF...")
            extraction_start = datetime.now()
            
            raw_data = self.extractor.get_extracted_data()
            self.stats['total_records'] = len(raw_data)
            self.stats['extraction_time'] = (datetime.now() - extraction_start).total_seconds()
            
            print(f"   ✓ Extracted {len(raw_data)} records from PDF")
            
            if not raw_data:
                print("   ❌ No data extracted from PDF. Please check the PDF format.")
                return False
            
            # Step 2: Process and validate data
            print("\n2. Processing and validating data...")
            processing_start = datetime.now()
            
            processed_data = self.processor.process_customer_data(raw_data)
            validation_report = self.processor.get_validation_report()
            
            self.stats['valid_records'] = validation_report['total_records']
            self.stats['error_records'] = validation_report['error_count']
            self.stats['processing_time'] = (datetime.now() - processing_start).total_seconds()
            
            print(f"   ✓ Processed {validation_report['total_records']} valid records")
            print(f"   ✓ {validation_report['error_count']} records had validation errors")
            print(f"   ✓ Success rate: {validation_report['success_rate']:.1f}%")
            
            # Step 3: Write to Excel
            print("\n3. Writing data to Excel...")
            writing_start = datetime.now()
            
            success = self.writer.create_excel_file(processed_data, self.excel_template_path)
            if success:
                # Create summary sheet
                self.writer.create_summary_sheet(validation_report)
                self.writer.workbook.save(self.output_path)
                
                self.stats['writing_time'] = (datetime.now() - writing_start).total_seconds()
                print(f"   ✓ Excel file created successfully: {self.output_path}")
            else:
                print("   ❌ Failed to create Excel file")
                return False
            
            # Step 4: Generate final report
            self.stats['end_time'] = datetime.now()
            self.print_final_report()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during processing: {str(e)}")
            return False
    
    def print_final_report(self):
        """Print final processing report"""
        total_time = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        print("\n" + "=" * 60)
        print("PROCESSING COMPLETE - Final Report")
        print("=" * 60)
        print(f"Total Processing Time: {total_time:.2f} seconds")
        print(f"  - PDF Extraction: {self.stats['extraction_time']:.2f} seconds")
        print(f"  - Data Processing: {self.stats['processing_time']:.2f} seconds")
        print(f"  - Excel Writing: {self.stats['writing_time']:.2f} seconds")
        print(f"\nRecords Processed: {self.stats['total_records']}")
        print(f"Valid Records: {self.stats['valid_records']}")
        print(f"Error Records: {self.stats['error_records']}")
        print(f"Success Rate: {(self.stats['valid_records'] / self.stats['total_records'] * 100):.1f}%")
        print(f"\nOutput File: {self.output_path}")
        print("=" * 60)
    
    def preview_data(self, num_records: int = 10):
        """Preview extracted data before processing"""
        print(f"\nPreviewing first {num_records} records from PDF:")
        print("-" * 50)
        
        raw_data = self.extractor.get_extracted_data()
        
        for i, record in enumerate(raw_data[:num_records]):
            print(f"{i+1:3d}. {record['CUSTOMER NAME']:<25} | {record['CRN']}")
        
        if len(raw_data) > num_records:
            print(f"     ... and {len(raw_data) - num_records} more records")
        
        print(f"\nTotal records found: {len(raw_data)}")

def main():
    """Main function to run the auto-typing model"""
    # File paths
    pdf_path = "/workspace/DOC-20221124-WA0102-1 (1) (1).pdf"
    excel_template = "/workspace/DOC-20221124-WA0102-2.xlsx"
    output_path = "/workspace/auto_typed_output.xlsx"
    
    # Check if files exist
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    if not os.path.exists(excel_template):
        print(f"⚠️  Excel template not found: {excel_template}")
        print("   Will create new Excel file without template")
        excel_template = None
    
    # Create and run the model
    model = AutoTypingModel(pdf_path, excel_template, output_path)
    
    # Preview data first
    model.preview_data(10)
    
    # Auto-proceed for background execution
    print("\n" + "=" * 60)
    print("Proceeding with auto-typing process...")
    
    success = model.run()
    if success:
        print("\n🎉 Auto-typing process completed successfully!")
    else:
        print("\n❌ Auto-typing process failed. Please check the error messages above.")

if __name__ == "__main__":
    main()