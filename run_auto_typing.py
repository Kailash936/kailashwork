#!/usr/bin/env python3
"""
Simple script to run the auto-typing model
Usage: python3 run_auto_typing.py
"""

from auto_typing_model import AutoTypingModel
import os

def main():
    # File paths
    pdf_path = "/workspace/DOC-20221124-WA0102-1 (1) (1).pdf"
    excel_template = "/workspace/DOC-20221124-WA0102-2.xlsx"
    output_path = "/workspace/auto_typed_output.xlsx"
    
    print("🚀 Starting Auto-Typing Model")
    print("=" * 50)
    
    # Check if files exist
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    if not os.path.exists(excel_template):
        print(f"⚠️  Excel template not found: {excel_template}")
        print("   Will create new Excel file without template")
        excel_template = None
    
    # Create and run the model
    model = AutoTypingModel(pdf_path, excel_template, output_path)
    
    # Preview data first
    print("\n📋 Previewing extracted data:")
    model.preview_data(5)
    
    # Run the complete process
    print("\n⚙️  Running auto-typing process...")
    success = model.run()
    
    if success:
        print(f"\n✅ Success! Output saved to: {output_path}")
        print(f"📊 Check the 'Summary' sheet for processing statistics")
        return True
    else:
        print("\n❌ Process failed. Check error messages above.")
        return False

if __name__ == "__main__":
    main()