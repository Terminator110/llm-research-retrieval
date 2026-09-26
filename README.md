# LLM Research Retrieval

A RAG-based chatbot for answering questions about LLM research papers published in 2025.

## Project Status

This project is currently under development. The initial ingestion stage is complete, including programmatic PDF downloading, PDF-to-text extraction, page-level text preservation, and basic text normalization. The remaining RAG pipeline will be added incrementally.

## Pipeline

```text
LLM Research Papers
        ↓
PDF Ingestion
        ↓
PDF → Text
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Retrieval
        ↓
LLM Generation
        ↓
Answer + Sources
```

## Current Focus

The repository currently implements the **PDF → text ingestion stage**. The next stage is document chunking, followed by embeddings, vector retrieval, and question answering.

## Data

The initial corpus consists of LLM research papers published in 2025. Papers are downloaded programmatically from their source URLs rather than manually added to the repository.

More implementation details will be documented as the project progresses.
