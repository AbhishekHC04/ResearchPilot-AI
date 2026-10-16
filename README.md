# ResearchPilot AI

An AI-powered PDF question-answering application built using Retrieval-Augmented Generation (RAG), semantic search, and a locally hosted language model.

## Features

- Upload and process PDF documents.
- Extract and split text into chunks.
- Retrieve relevant passages using semantic similarity.
- Generate answers using Ollama and Qwen 2.5 3B.
- Display source citations with document names and page numbers.
- Automated testing with Pytest.

## Tech Stack

- Python 3.12
- Streamlit
- Ollama
- Qwen 2.5 3B
- Sentence Transformers
- Pytest

## Project Structure

```text
ResearchPilot-AI/
├── app.py
├── src/
│   └── researchpilot/
│       ├── answer_generator.py
│       ├── pdf_processor.py
│       ├── pipeline.py
│       ├── semantic_search.py
│       └── text_chunker.py
├── tests/
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AbhishekHC04/ResearchPilot-AI.git
cd ResearchPilot-AI
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Ollama and download the model

Install Ollama from https://ollama.com/, then run:

```bash
ollama pull qwen2.5:3b
```

### 4. Run the application

```powershell
streamlit run app.py --server.fileWatcherType none
```

### 5. Run the tests

```powershell
python -m pytest -q
```

**Latest verified test result:** 19 tests passed.

## Author

Abhishek HC

GitHub: https://github.com/AbhishekHC04
<!-- CI workflow enabled -->
