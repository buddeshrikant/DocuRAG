# DocuRAG � Document Intelligence & Question Answering System

DocuRAG is a Retrieval-Augmented Generation (RAG) project that enables users to ask questions about documents and receive answers grounded in the document content.

The system processes a PDF document, extracts its text, splits the text into smaller chunks, converts the chunks into numerical embeddings, and stores them in a FAISS vector index. When a user asks a question, DocuRAG retrieves relevant passages and uses a language model to generate an answer based on those passages.

## Technology Stack

- **Python** � Core programming language
- **PyMuPDF** � PDF text extraction
- **Sentence Transformers** � Text embeddings using `all-MiniLM-L6-v2`
- **FAISS** � Vector indexing and similarity search
- **Groq API** � Large language model inference
- **NumPy** � Numerical operations on embedding vectors

## Current Features

- Extract text from PDF documents
- Split extracted text into page-aware chunks with overlap
- Generate vector embeddings for document chunks
- Build and save a FAISS similarity-search index
- Retrieve relevant passages for a user question
- Generate answers grounded in retrieved passages, with PDF page citations

## Setup and Usage

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv rag
.\rag\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure the Groq API key

```powershell
$env:GROQ_API_KEY = Read-Host "Paste your Groq API key"
```

Never share your API key or commit it to Git.

### 4. Run the question-answering system

```powershell
python src/ask_question.py
```

Ensure the PDF has been processed and the FAISS index and chunk metadata files have been generated before running the question-answering script.

### 5. Build the search index

After generating `data/documents/chunks_preview.txt`, run:

```powershell
python src/build_index.py
```

This generates the FAISS vector index and chunk metadata files used during question answering.

## Rebuild the Document Pipeline

Run these commands from the project root directory, in order.

### 1. Extract text from the PDF

```powershell
python src/read_pdf.py
```

This extracts text from the PDF and saves it to `data/documents/infosys_annual_report.txt`.

### 2. Split the extracted text into chunks

```powershell
python src/chunk_text.py
```

This creates page-aware chunks in `data/documents/chunks_preview.txt`, using a chunk size of 1,000 characters and an overlap of 200 characters.

### 3. Build the FAISS search index

```powershell
python src/build_index.py
```

This generates `data/faiss_index.bin` and `data/chunks_metadata.pkl`.

### 4. Ask questions about the document

First, configure your Groq API key in PowerShell as described in the Setup and Usage section. Then run:

```powershell
python src/ask_question.py
```
