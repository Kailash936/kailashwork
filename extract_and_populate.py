#!/usr/bin/env python3

import PyPDF2
import pandas as pd
import openpyxl
from openpyxl import load_workbook
import re
import os

def extract_pdf_content(pdf_path):
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def read_excel_structure(excel_path):
    """Read and analyze the existing Excel file structure"""
    try:
        # Load the workbook
        workbook = load_workbook(excel_path)
        sheet = workbook.active
        
        print("Excel file structure:")
        print(f"Sheet name: {sheet.title}")
        print(f"Max row: {sheet.max_row}")
        print(f"Max column: {sheet.max_column}")
        
        # Print current content
        print("\nCurrent content:")
        for row in range(1, min(sheet.max_row + 1, 20)):  # Show first 20 rows
            row_data = []
            for col in range(1, min(sheet.max_column + 1, 10)):  # Show first 10 columns
                cell_value = sheet.cell(row=row, column=col).value
                row_data.append(str(cell_value) if cell_value is not None else "")
            print(f"Row {row}: {row_data}")
        
        return workbook, sheet
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None, None

def parse_pdf_content(text):
    """Parse PDF content and structure it for Excel"""
    # Split text into lines and clean up
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Try to identify structured data patterns
    structured_data = []
    
    # Look for common patterns like dates, numbers, names, etc.
    for i, line in enumerate(lines):
        # Skip very short lines that might be headers or separators
        if len(line) < 3:
            continue
            
        # Look for lines that might contain structured information
        # This is a basic parser - you might need to customize based on your PDF content
        if any(keyword in line.lower() for keyword in ['date', 'name', 'amount', 'total', 'description', 'item']):
            structured_data.append(['Header', line])
        elif re.match(r'^\d+[\.\)]\s+', line):  # Numbered items
            structured_data.append(['Item', line])
        elif re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', line):  # Date patterns
            structured_data.append(['Date', line])
        elif re.match(r'^\$?\d+[.,]\d{2}', line):  # Money amounts
            structured_data.append(['Amount', line])
        else:
            structured_data.append(['Text', line])
    
    return structured_data

def populate_excel(workbook, sheet, structured_data):
    """Populate Excel file with structured data"""
    try:
        # Clear existing content (optional - you might want to keep headers)
        # sheet.delete_rows(1, sheet.max_row)
        
        # Add headers
        headers = ['Type', 'Content', 'Page', 'Line']
        for col, header in enumerate(headers, 1):
            sheet.cell(row=1, column=col, value=header)
        
        # Add data
        for row_idx, (data_type, content) in enumerate(structured_data, 2):
            sheet.cell(row=row_idx, column=1, value=data_type)
            sheet.cell(row=row_idx, column=2, value=content)
            sheet.cell(row=row_idx, column=3, value=1)  # Page number (simplified)
            sheet.cell(row=row_idx, column=4, value=row_idx - 1)  # Line number
        
        # Auto-adjust column widths
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            sheet.column_dimensions[column_letter].width = adjusted_width
        
        return True
    except Exception as e:
        print(f"Error populating Excel: {e}")
        return False

def main():
    # File paths
    pdf_path = "/workspace/DOC-20221124-WA0102-1 (1) (1).pdf"
    excel_path = "/workspace/DOC-20221124-WA0102-2.xlsx"
    output_path = "/workspace/DOC-20221124-WA0102-2_updated.xlsx"
    
    print("=== Document Content Extraction and Excel Population ===")
    
    # Step 1: Read Excel structure
    print("\n1. Reading Excel file structure...")
    workbook, sheet = read_excel_structure(excel_path)
    if not workbook:
        return
    
    # Step 2: Extract PDF content
    print("\n2. Extracting PDF content...")
    pdf_text = extract_pdf_content(pdf_path)
    if not pdf_text:
        print("No content extracted from PDF")
        return
    
    print(f"Extracted {len(pdf_text)} characters from PDF")
    print("First 500 characters of PDF content:")
    print(pdf_text[:500])
    print("...")
    
    # Step 3: Parse PDF content
    print("\n3. Parsing PDF content...")
    structured_data = parse_pdf_content(pdf_text)
    print(f"Parsed {len(structured_data)} structured items")
    
    # Step 4: Populate Excel
    print("\n4. Populating Excel file...")
    if populate_excel(workbook, sheet, structured_data):
        # Save the updated workbook
        workbook.save(output_path)
        print(f"Excel file updated and saved as: {output_path}")
        
        # Show summary
        print(f"\nSummary:")
        print(f"- PDF content extracted: {len(pdf_text)} characters")
        print(f"- Structured items created: {len(structured_data)}")
        print(f"- Excel file updated: {output_path}")
    else:
        print("Failed to populate Excel file")

if __name__ == "__main__":
    main()