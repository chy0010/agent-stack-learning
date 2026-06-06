from openai import OpenAI
from dotenv import load_dotenv
import psycopg2
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

question = input("Ask: ")

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

question_embedding = response.data[0].embedding

cursor.execute(
    """
    SELECT chunk_text
    FROM document_chunks
    ORDER BY embedding <=> %s::vector
    LIMIT 3
    """,
    (question_embedding,)
)

rows = cursor.fetchall()

context = "\n".join(row[0]for row in rows)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content":
            """
            Answer only using the provided context.
            If the answer is not present,
            say it is not available.
            """
        },
        {
            "role": "user",
            "content":f"""Context:{context}Question:{question}"""
        }
    ]
)

print(response.choices[0].message.content)

cursor.close()
conn.close()