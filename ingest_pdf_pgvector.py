from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import psycopg2                                     # Python → PostgreSQL connector.
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conn = psycopg2.connect(
    host=os.getenv("PG_HOST", "localhost"),
    port=os.getenv("PG_PORT", "5432"),
    database=os.getenv("PG_DATABASE", "rag_db"),
    user=os.getenv("PG_USER", "postgres"),
    password=os.getenv("PG_PASSWORD")
)

cursor = conn.cursor()

reader = PdfReader("Meta.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

print(len(text))
print(text[:1000])
chunk_size = 1000
overlap = 200

chunks = []

for i in range(0,len(text),chunk_size - overlap):
    chunks.append(text[i:i+chunk_size])

print(f"Total Chunks: {len(chunks)}")


for chunk in chunks:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
        )
    embedding = response.data[0].embedding

    cursor.execute(
        """
        INSERT INTO document_chunks
        (chunk_text, embedding)
        VALUES (%s, %s)
        """,
        (
            chunk,
            embedding
        )
    )    

conn.commit()

print("Embeddings stored successfully!")
cursor.close()
conn.close()
