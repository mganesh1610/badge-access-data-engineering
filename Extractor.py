import subprocess
import re
import pandas as pd
from pathlib import Path

def extract_cardholder_data(pdf_filename: str, output_excel: str):
    """
    Extracts cardholder access data from the specified PDF file (looked up in the working directory)
    and writes it to an Excel file.

    Arguments:
        pdf_filename (str): Name of the PDF file (e.g., 'Cardholder Access to Readers 001-050.pdf').
        output_excel (str): Path where the Excel output will be saved.
    """
    # Dynamically get the full path of the file in the working directory
    cwd = Path.cwd()
    pdf_path = cwd / pdf_filename
    text_path = pdf_path.with_suffix('.txt')

    # Check if the PDF file exists
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Convert PDF to text using pdftotext
    subprocess.run(['pdftotext', '-layout', str(pdf_path), str(text_path)], check=True)

    # Read text lines
    with open(text_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.rstrip('\n') for line in f]

    header_keywords = [
        'Cardholder Access to Readers', 'OnGuard', 'Report Date',
        
        'Standard Time', 'Cardholders have access', 'Page'
    ]
    re_badge = re.compile(r'\b(\d{3,10})\b')

    records = []
    current_reader = None
    current_name = None
    i = 0
    n_lines = len(lines)

    while i < n_lines:
        line = lines[i].replace('\x0c', '').strip()

        if line.startswith('Reader:'):
            current_reader = line.split(':', 1)[1].strip()
            i += 1
            continue

        skip = False
        if not line:
            skip = True
        else:
            for kw in header_keywords:
                if kw in line:
                    skip = True
                    break
        if skip or (line.startswith('Name') and 'Badge ID' in line):
            i += 1
            continue
        if line.startswith('Assignment Active') or line.startswith('Assignment Deactive') \
           or line.startswith('Timezone/Elevator Level'):
            i += 1
            continue

        match = re_badge.search(line)
        if match:
            badge_id = match.group(1)
            name_segment = line[:match.start()].strip()
            if name_segment:
                current_name = name_segment
            name = current_name

            remainder = line[match.end():].strip()

            j = i + 1
            while j < n_lines:
                next_line = lines[j].replace('\x0c', '').strip()
                if not next_line:
                    j += 1
                    continue
                if next_line.startswith('Reader:') or \
                   any(kw in next_line for kw in header_keywords) or \
                   next_line.startswith('Name') and 'Badge ID' in next_line or \
                   next_line.startswith('Assignment Active') or \
                   next_line.startswith('Assignment Deactive') or \
                   next_line.startswith('Timezone/Elevator Level'):
                    break
                if re_badge.search(next_line):
                    break
                remainder += ' ' + next_line
                j += 1

            parts = remainder.split()
            if len(parts) >= 5:
                active_date = parts[0]
                active_time = parts[1]
                deactive_date = parts[2]
                deactive_time = parts[3]
                badge_active = f"{active_date} {active_time}"
                badge_deactive = f"{deactive_date} {deactive_time}"
                via_access = ' '.join(parts[4:])
            else:
                badge_active = ''
                badge_deactive = ''
                via_access = remainder

            records.append([current_reader, name, badge_id, badge_active, badge_deactive, via_access])
            i = j
        else:
            i += 1

    columns = ['Reader', 'Name', 'Badge ID', 'Badge Active', 'Badge Deactive', 'Via Access Level']
    df = pd.DataFrame(records, columns=columns)
    df.to_excel(output_excel, index=False)
    print(f"Extracted {len(df)} records to {output_excel!s}")

# Example usage:
extract_cardholder_data('BDC 2nd Floor Lab Cardholders.pdf', 'BDC 2nd Floor Lab Cardholders.xlsx')
