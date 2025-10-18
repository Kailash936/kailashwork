# Auto-Typing Model

A complete solution for automatically extracting customer data from PDF documents and populating Excel files.

## Features

- **PDF Data Extraction**: Automatically extracts customer names and CRNs from PDF files
- **Data Validation**: Validates and cleans extracted data
- **Excel Population**: Populates Excel files with structured data
- **Error Handling**: Comprehensive error reporting and validation
- **Summary Reports**: Generates processing statistics and summaries

## Files Structure

```
/workspace/
├── auto_typing_model.py      # Main application
├── pdf_extractor.py          # PDF data extraction module
├── data_processor.py         # Data processing and validation
├── excel_writer.py           # Excel file creation and writing
├── requirements.txt          # Python dependencies
├── README_AUTO_TYPING.md     # This file
├── DOC-20221124-WA0102-1 (1) (1).pdf  # Input PDF
├── DOC-20221124-WA0102-2.xlsx         # Excel template
└── auto_typed_output.xlsx    # Generated output
```

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python auto_typing_model.py
```

### Programmatic Usage
```python
from auto_typing_model import AutoTypingModel

# Create model instance
model = AutoTypingModel(
    pdf_path="path/to/input.pdf",
    excel_template_path="path/to/template.xlsx",  # Optional
    output_path="path/to/output.xlsx"             # Optional
)

# Run the process
success = model.run()
```

## Input Format

The model expects PDF files with customer data in the format:
```
CUSTOMER NAME CRN
AANCHAL JOSHI 5041885433
AIMAN ALI 5111926597
...
```

## Output Format

The model generates Excel files with the following columns:
- CUSTOMER NAME
- CRN
- PROGRAM
- RO_NAME
- MANUFACTURERDESC
- ASSETCAT
- MAKE
- RO_NAME.1
- ASSESTCAT
- MANUFACTURER

## Features

### Data Extraction
- Extracts customer names and CRNs from PDF
- Handles various PDF formats and layouts
- Supports different CRN formats (with/without dots, spaces)

### Data Processing
- Validates CRN format (10 digits)
- Cleans and normalizes customer names
- Removes duplicates
- Comprehensive error reporting

### Excel Generation
- Creates formatted Excel files
- Auto-adjusts column widths
- Adds borders and styling
- Includes summary sheet with statistics

## Error Handling

The model includes comprehensive error handling:
- PDF reading errors
- Data validation errors
- Excel writing errors
- Detailed error reporting

## Performance

- Processes hundreds of records in seconds
- Memory efficient for large PDFs
- Detailed timing statistics

## Example Output

```
============================================================
AUTO-TYPING MODEL - Starting Process
============================================================

1. Extracting data from PDF...
   ✓ Extracted 150 records from PDF

2. Processing and validating data...
   ✓ Processed 148 valid records
   ✓ 2 records had validation errors
   ✓ Success rate: 98.7%

3. Writing data to Excel...
   ✓ Excel file created successfully: auto_typed_output.xlsx

============================================================
PROCESSING COMPLETE - Final Report
============================================================
Total Processing Time: 2.34 seconds
  - PDF Extraction: 0.45 seconds
  - Data Processing: 0.23 seconds
  - Excel Writing: 1.66 seconds

Records Processed: 150
Valid Records: 148
Error Records: 2
Success Rate: 98.7%

Output File: auto_typed_output.xlsx
============================================================
```