# Patient Data Loading for Tumor Board Emulation

This document explains how to use the new patient data loading functionality in the `board_emulation.py` script.

## Overview

The tumor board emulation system now supports loading patient information from external files, making it easier for doctors to:
- Input patient data without modifying code
- Share patient cases between different users
- Maintain a database of patient cases
- Iterate on patient data through back-and-forth interactions

## Supported File Formats

### 1. JSON Format (Recommended)
- **Extension**: `.json`
- **Structure**: Standard JSON with all required fields
- **Advantages**: Structured, easy to validate, supports complex data types
- **Best for**: Production use, automated systems, data exchange

**Example**: `patient_data_example.json`

### 2. TXT Format (Simple)
- **Extension**: `.txt`
- **Structure**: Key=value pairs, one per line
- **Advantages**: Human-readable, easy to edit, supports comments
- **Best for**: Quick edits, manual input, simple cases

**Example**: `patient_data_example.txt`

## Required Fields

All patient data files must contain these required fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `patient_id` | string | Unique patient identifier | "CASE-2024-001" |
| `age` | number | Patient age in years | 58 |
| `gender` | string | Patient gender | "female" |
| `tumor_size` | number | Tumor size in cm | 3.2 |
| `tumor_stage` | string | TNM staging | "T2N1M0" |
| `biopsy_result` | string | Biopsy findings | "Invasive ductal carcinoma..." |
| `imaging_result` | string | Imaging findings | "3.2 cm irregular mass..." |
| `symptoms` | array | List of symptoms | ["palpable mass", "pain"] |
| `medical_history` | array | Medical history | ["hypertension", "diabetes"] |

## Usage

### Basic Usage
```bash
# Run with sample case (default)
python board_emulation.py

# Load from JSON file
python board_emulation.py --file patient_data.json

# Load from TXT file
python board_emulation.py --file patient_data.txt

# Enable debug mode with file loading
python board_emulation.py --file patient_data.json --debug

# Show help
python board_emulation.py --help
```

### Command Line Options
- `--file` or `-f`: Specify patient data file path
- `--debug` or `-d`: Enable debug mode (shows detailed prompts)
- `--help` or `-h`: Show usage information

## File Examples

### JSON Example
```json
{
    "patient_id": "CASE-2024-002",
    "age": 65,
    "gender": "male",
    "tumor_size": 4.5,
    "tumor_stage": "T3N2M0",
    "biopsy_result": "Invasive adenocarcinoma, grade 3, KRAS mutation positive",
    "imaging_result": "4.5 cm irregular mass in right colon, multiple enlarged lymph nodes",
    "symptoms": ["abdominal pain", "weight loss", "fatigue"],
    "medical_history": ["hypertension", "diabetes", "family history of cancer"]
}
```

### TXT Example
```txt
# Patient Case Data
patient_id=CASE-2024-003
age=72
gender=female
tumor_size=2.8
tumor_stage=T2N0M0
biopsy_result=Well-differentiated adenocarcinoma, grade 1
imaging_result=2.8 cm polypoid mass in sigmoid colon
symptoms=rectal bleeding, mild abdominal discomfort
medical_history=hyperlipidemia, post-menopausal, regular screening
```

## Workflow for Doctors

### 1. Initial Case Creation
1. Create a new patient data file (JSON or TXT)
2. Fill in all required fields
3. Save the file with a descriptive name

### 2. Tumor Board Review
1. Run the emulation with your patient file:
   ```bash
   python board_emulation.py --file your_patient.json
   ```
2. Review the AI-generated recommendations
3. Note any questions or areas needing clarification

### 3. Iterative Refinement
1. Edit the patient data file to add new information
2. Re-run the emulation to get updated recommendations
3. Continue this process until satisfied with the analysis

### 4. Case Documentation
1. Keep the final patient data file for records
2. Use the AI recommendations as a starting point for real tumor board discussions
3. Share the file with colleagues for additional input

## Error Handling

The system provides helpful error messages for common issues:

- **Missing file**: Clear indication if the specified file doesn't exist
- **Invalid format**: Detailed error messages for JSON syntax errors
- **Missing fields**: List of required fields that are missing
- **Data type errors**: Clear indication of invalid numeric values
- **Fallback behavior**: Automatically creates a sample case if file loading fails

## Tips for Best Results

1. **Use descriptive patient IDs**: Include date and case number for easy tracking
2. **Be specific with symptoms**: List all relevant symptoms, even minor ones
3. **Include molecular markers**: Add genetic/molecular information when available
4. **Document imaging details**: Be thorough with imaging findings and measurements
5. **Update iteratively**: Start with basic information and add details as available
6. **Use consistent terminology**: Follow standard medical terminology for better AI understanding

## Troubleshooting

### Common Issues
1. **File not found**: Check file path and ensure file exists
2. **Invalid JSON**: Use a JSON validator to check syntax
3. **Missing fields**: Ensure all required fields are present
4. **Permission errors**: Check file read permissions

### Getting Help
- Run `python board_emulation.py --help` for usage information
- Check the error messages for specific guidance
- Verify file format matches the examples provided

## Future Enhancements

Planned improvements include:
- Support for additional file formats (CSV, Excel)
- Template generation for common cancer types
- Integration with hospital information systems
- Automated validation of medical terminology
- Support for image attachments and reports
