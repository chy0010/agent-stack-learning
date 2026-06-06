from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


reader = PdfReader("Meta.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

#print(text[:1000])
#print(len(text))

chunk_size = 1000
overlap = 200
chunks = []



for i in range(0, len(text), chunk_size - overlap):
    chunks.append(text[i:i + chunk_size])

#print("Number of chunks:", len(chunks))
#print(chunks[0])can 

embeddings = []

for chunk in chunks:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    embeddings.append(response.data[0].embedding)

#print("Embeddings Created:", len(embeddings))

question = input("Ask: ")

question_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
).data[0].embedding


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )

scores = []

for embedding in embeddings:

    score = cosine_similarity(
        question_embedding,
        embedding
    )

    scores.append(score)


indexed_scores = list(enumerate(scores))

indexed_scores.sort(key=lambda x: x[1],reverse=True)

top_chunks = []

for idx, score in indexed_scores[:3]:
    top_chunks.append(chunks[idx])

context = "\n\n".join(top_chunks)

print("\nTop Chunks:\n")

#for idx, score in indexed_scores[:3]:
#    print(f"Chunk {idx} Score: {score}")


response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {
            "role": "system",
            "content": "Answer only from the provided context."
        },
        {
            "role": "user",
            "content":
            f"""
            Context:{context}
            Question:{question}
            """
        }
    ]
)

print(response.choices[0].message.content)