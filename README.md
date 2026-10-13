
# LLM Research Retrieval

A Retrieval-Augmented Generation (RAG) chatbot for exploring and answering questions about LLM research papers published in 2025. The project combines PDF ingestion, token-based chunking, dense vector embeddings, semantic retrieval, and LLM-based answer generation with source citations.

## Project Status

**Core RAG pipeline implemented; retrieval evaluation is underway.**

Current capabilities include:

- Programmatic downloading of research papers in PDF format.
- PDF-to-text extraction with page-level text preservation.
- Text normalization and token-based chunking.
- Dense embeddings using `BAAI/bge-small-en-v1.5`.
- Persistent vector storage and semantic retrieval using ChromaDB.
- LLM-based answer generation through OpenRouter.
- Source metadata for tracing retrieved information to its document and page.

## Architecture

```text
LLM Research Papers (2025)
          |
          v
    PDF Ingestion
          |
          v
    Text Extraction
          |
          v
    Token-Based Chunking
          |
          v
    BGE Embeddings
          |
          v
    ChromaDB Vector Store
          |
          v
    Semantic Retrieval
          |
          v
    LLM Answer Generation
          |
          v
    Answer with Source Citations
```

## Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| PDF processing | PyMuPDF |
| Tokenization | Hugging Face Transformers |
| Embeddings | Sentence Transformers - BGE-small-en-v1.5 |
| Vector database | ChromaDB |
| LLM integration | OpenAI-compatible API via OpenRouter |
| Configuration | Python dotenv |

## Repository Structure

```text
llm-research-retrieval/
├── data/
│   ├── raw/                 # Downloaded research PDFs
│   └── processed/           # Extracted and normalized text
├── storage/
│   └── chroma/              # Persistent vector database
├── src/
│   ├── ingestion/
│   │   └── pdf2text.py      # PDF download and text extraction
│   ├── embedding/
│   │   ├── embedder.py      # Chunking and embedding generation
│   │   └── vector_store.py  # Vector storage and retrieval
│   └── retrieval/
│       └── retrieval_bot.py # Retrieval and answer generation
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

### 1. PDF Ingestion

Research papers are downloaded programmatically from their source URLs rather than manually added to the repository.

### 2. Text Extraction

PyMuPDF extracts text from PDF documents while preserving page-level information for source attribution.

### 3. Chunking

Extracted text is divided into token-based chunks with overlap to preserve useful context for retrieval.

### 4. Embedding Generation

Each chunk is converted into a dense vector representation using `BAAI/bge-small-en-v1.5`.

### 5. Vector Storage and Retrieval

ChromaDB stores the embeddings, chunk text, and associated metadata. When a question is submitted, the system retrieves semantically relevant passages.

### 6. Answer Generation

The retrieved passages are provided as context to an LLM, which generates a natural-language answer.

### 7. Source Attribution

Document and page metadata help trace retrieved passages back to their original research papers.

## Setup

### Prerequisites

- Python
- An OpenRouter API key
- The Python dependencies listed in `requirements.txt`

### Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
CHAT_API_KEY=your_openrouter_api_key
```

Keep API keys and other secrets out of version control. Ensure `.env` is included in `.gitignore`.


## Running the Project

Run all commands from the project root directory in the following order.

### 1. Extract Text from PDFs

Download research papers from their source URLs, extract text using PyMuPDF, preserve page-level information, and save the processed text for subsequent stages.

```bash
python src/ingestion/pdf2text.py
```

### 2. Generate Embeddings and Populate ChromaDB

Process the extracted text, split it into token-based chunks, generate dense embeddings using `BAAI/bge-small-en-v1.5`, and store the chunk text, embeddings, and metadata in the persistent ChromaDB collection.

```bash
python src/embedding/vector_store.py
```

### 3. Run the Retrieval Chatbot

Launch the chatbot to submit questions about the research papers. The system retrieves relevant passages from ChromaDB and uses an LLM through OpenRouter to generate answers with source citations.

```bash
python src/retrieval/retrieval_bot.py
```

### Configuration and Requirements

- Install the dependencies listed in `requirements.txt`.
- Configure `CHAT_API_KEY` in your `.env` file with a valid OpenRouter API key.
- Run the PDF extraction and vector-store initialization stages before starting the chatbot.

## Demo

A screenshot of the working chatbot will be added here.

<!-- Replace the placeholder below after adding the actual screenshot. -->
<!-- ![RAG chatbot demo](docs/images/chatbot-demo.png) -->

## Evaluation - In Progress

The current focus is establishing a measurable baseline for retrieval quality and answer reliability.

Planned evaluation areas include:

- Recall@K and Precision@K.
- Mean Reciprocal Rank (MRR).
- A manually verified dataset of questions and relevant chunks.
- Analysis of retrieved context and source attribution.
- Assessment of answer relevance, factual grounding, and completeness.

Evaluation results will be documented after the baseline measurements are completed.

## Future Improvements

- Expand the research-paper corpus.
- Improve retrieval quality based on evaluation results.
- Investigate advanced retrieval and reranking strategies.
- Compare the baseline against document-aware RAG approaches.
- Document evaluation results and limitations.

## Project Goal

Build a reproducible RAG baseline for research-paper question answering, with traceable sources and measurable retrieval quality.
