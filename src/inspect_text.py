
from pathlib import Path
import pymupdf

# Find the project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_DIR / "data" / "documents" / "infosys_annual_report.pdf"
TEXT_PATH = PROJECT_DIR / "data" / "documents" / "infosys_annual_report.txt"

# Read the extracted text
full_text = TEXT_PATH.read_text(encoding="utf-8")

print("========== TEXT FILE CHECK ==========")
print("Characters:", len(full_text))
print("Number of page markers:", full_text.count("--- Page "))

# Check text extraction quality page by page
document = pymupdf.open(PDF_PATH)

empty_pages = []
short_pages = []

for page_number, page in enumerate(document, start=1):
    page_text = page.get_text().strip()

    if len(page_text) == 0:
        empty_pages.append(page_number)
    elif len(page_text) < 50:
        short_pages.append(page_number)

document.close()

print("\n========== PAGE CHECK ==========")
print("Total PDF pages:", 372)
print("Pages with no extracted text:", empty_pages)
print("Pages with fewer than 50 characters:", short_pages)

# Preview a small section of the extracted text
print("\n========== TEXT PREVIEW ==========")
print(full_text[:1500])

# Look for financial keywords
print("\n========== KEYWORD CHECK ==========")

keywords = [
    "revenue",
    "net profit",
    "risk factors",
    "financial statements",
    "total assets",
]

for keyword in keywords:
    print(f"{keyword}: {full_text.lower().count(keyword.lower())} occurrences")
