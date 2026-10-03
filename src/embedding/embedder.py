import json
from pathlib import Path

from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer


tokenizer = AutoTokenizer.from_pretrained(
    "BAAI/bge-small-en-v1.5"
)

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

CURRENT_DIR = Path(__file__).resolve().parent
folder_path = CURRENT_DIR.parent.parent / "data/processed"


def split_text(text, chunk_size=384, chunk_overlap=50):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    print(f"Tokenized text into {len(tokens)} tokens")

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size

        chunk_tokens = tokens[start:end]

        chunk_text = tokenizer.decode(
            chunk_tokens,
            skip_special_tokens=True
        )

        chunks.append(chunk_text)
        start = end - chunk_overlap 

    return chunks


def main():
    all_chunks = []
    texts = []

    for paper in folder_path.glob("*.json"):
        with open(paper, "r", encoding="utf-8") as f:
            data = json.load(f)

        for page in data["pages"]:
            page_chunks = split_text(page["text"])

            for chunk_index, chunk_text in enumerate(page_chunks):

                texts.append(chunk_text)

                all_chunks.append({
                    "id": f"{data['document_id']}_page{page['page']}_chunk{chunk_index}",
                    "text": chunk_text,
                    "metadata": {
                        "document_id": data["document_id"],
                        "source_file": data["source_file"],
                        "page": page["page"],
                        "chunk_index": chunk_index,
                    }
                })

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    for chunk, embedding in zip(all_chunks, embeddings):
        print ("Embedding =", embedding)
        chunk["embedding"] = embedding.tolist()

    return all_chunks

if __name__ == "__main__":
    main()