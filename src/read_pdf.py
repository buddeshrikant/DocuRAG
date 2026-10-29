import pymupdf
from pathlib import Path

PROJECT_DIR =Path(__file__).resolve().parent.parent

## Define the input PDF and output text file
PDF_PATH = (
    PROJECT_DIR
    /"data"
    /"documents"
    /"infosys_annual_report.pdf"
)
OUTPUT_PATH =(
    PROJECT_DIR
    /"data"
    /"documents"
    /"infosys_annual_report.txt"
)
# open the pdf
document =pymupdf.open(PDF_PATH)

#print the total number of pages
print("PDF opened successfully!")
print("total pages=", len(document))

# extract text from the first page
# first_page = document[0]
# text = first_page.get_text()

# Extract text from every page
all_pages_text = []
for  page_number,page in enumerate(document,start=1):
    page_text = page.get_text()
    #keep all the number with its tex
    all_pages_text.append(
        f"\n---page{page_number}----\n{page_text}"
    )

# close the pdf
document.close()

# Combine all page text into one string
full_text = "\n".join(all_pages_text)

# Save the extracted text
OUTPUT_PATH.write_text(full_text, encoding="utf-8")

print("Text extraction completed!")
print("Output saved to:", OUTPUT_PATH)
print("Total characters extracted:", len(full_text))
print("Output file size (characters):", OUTPUT_PATH.stat().st_size)
