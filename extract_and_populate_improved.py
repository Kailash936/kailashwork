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

def parse_customer_data(text):
    """Parse customer data from PDF text"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    customers = []
    current_customer = {}
    
    for line in lines:
        # Skip header lines
        if line.upper() in ['CUSTOMER NAME', 'CRN', 'CUSTOMER NAME CRN']:
            continue
            
        # Check if line contains a CRN (10-digit number)
        crn_match = re.search(r'\b(\d{10})\b', line)
        if crn_match:
            crn = crn_match.group(1)
            # Extract name (everything before the CRN)
            name_part = line[:crn_match.start()].strip()
            if name_part:
                customers.append({
                    'CUSTOMER NAME': name_part,
                    'CRN': crn,
                    'PROGRAM': '',  # Will be filled based on context
                    'RO_NAME': '',  # Will be filled based on context
                    'MANUFACTURERDESC': '',  # Will be filled based on context
                    'ASSETCAT': '',  # Will be filled based on context
                    'MAKE': '',  # Will be filled based on context
                })
        else:
            # If no CRN found, this might be a continuation of a name
            # or a different type of data
            if customers and not re.match(r'^\d', line):
                # This might be a continuation of the last customer's name
                pass
    
    return customers

def populate_excel_with_customers(workbook, sheet, customers):
    """Populate Excel file with customer data"""
    try:
        # Clear existing data but keep headers
        # Delete rows 2 onwards (keep header row)
        if sheet.max_row > 1:
            sheet.delete_rows(2, sheet.max_row)
        
        # Ensure headers are in the first row
        headers = ['CUSTOMER NAME', 'CRN', 'PROGRAM', 'RO_NAME', 'MANUFACTURERDESC', 'ASSETCAT', 'MAKE', 'RO_NAME', 'ASSESTCAT']
        for col, header in enumerate(headers, 1):
            sheet.cell(row=1, column=col, value=header)
        
        # Add customer data
        for row_idx, customer in enumerate(customers, 2):
            sheet.cell(row=row_idx, column=1, value=customer['CUSTOMER NAME'])
            sheet.cell(row=row_idx, column=2, value=customer['CRN'])
            sheet.cell(row=row_idx, column=3, value=customer['PROGRAM'])
            sheet.cell(row=row_idx, column=4, value=customer['RO_NAME'])
            sheet.cell(row=row_idx, column=5, value=customer['MANUFACTURERDESC'])
            sheet.cell(row=row_idx, column=6, value=customer['ASSETCAT'])
            sheet.cell(row=row_idx, column=7, value=customer['MAKE'])
            sheet.cell(row=row_idx, column=8, value=customer['RO_NAME'])
            sheet.cell(row=row_idx, column=9, value=customer['ASSETCAT'])
        
        # Auto-adjust column widths
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if cell.value and len(str(cell.value)) > max_length:
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
    workbook = load_workbook(excel_path)
    sheet = workbook.active
    
    print("Excel file structure:")
    print(f"Sheet name: {sheet.title}")
    print(f"Max row: {sheet.max_row}")
    print(f"Max column: {sheet.max_column}")
    
    # Step 2: Extract PDF content
    print("\n2. Extracting PDF content...")
    pdf_text = extract_pdf_content(pdf_path)
    if not pdf_text:
        print("No content extracted from PDF")
        return
    
    print(f"Extracted {len(pdf_text)} characters from PDF")
    
    # Step 3: Parse customer data
    print("\n3. Parsing customer data from PDF...")
    customers = parse_customer_data(pdf_text)
    print(f"Found {len(customers)} customers")
    
    # Show first few customers
    print("\nFirst 10 customers:")
    for i, customer in enumerate(customers[:10]):
        print(f"{i+1}. {customer['CUSTOMER NAME']} - {customer['CRN']}")
    
    # Step 4: Populate Excel
    print("\n4. Populating Excel file with customer data...")
    if populate_excel_with_customers(workbook, sheet, customers):
        # Save the updated workbook
        workbook.save(output_path)
        print(f"Excel file updated and saved as: {output_path}")
        
        # Show summary
        print(f"\nSummary:")
        print(f"- PDF content extracted: {len(pdf_text)} characters")
        print(f"- Customers found: {len(customers)}")
        print(f"- Excel file updated: {output_path}")
    else:
        print("Failed to populate Excel file")

if __name__ == "__main__":
    main()