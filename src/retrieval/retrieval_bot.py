from sentence_transformers import SentenceTransformer
from openai import OpenAI
import chromadb
import os
from dotenv import load_dotenv


model = SentenceTransformer("BAAI/bge-small-en-v1.5")

load_dotenv()
CHAT_API_KEY = os.environ.get("CHAT_API_KEY")
chat_client = OpenAI(api_key=CHAT_API_KEY, base_url="https://openrouter.ai/api/v1")

client = chromadb.PersistentClient(path="storage/chroma")
table = client.get_collection("ai_research_papers")

def retrieve(question, n_results=3):

    query_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    results = table.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
    return results


def answer_question(question):

    results = retrieve(question)

    documents = results["documents"][0]
    print(f"Retrieved {documents} /n for the question: {question}")

    context = "\n\n".join(documents)

    prompt = f"""
            Base answer off the following context and answer the question.

            Context:
            {context}

            Question:
            {question}
            """

    response = chat_client.responses.create(
        model="qwen/qwen3.8-27b:free",
        input=prompt
    )

    return response.output_text

def main():

    while True:
        question = input("\nQuestion: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()