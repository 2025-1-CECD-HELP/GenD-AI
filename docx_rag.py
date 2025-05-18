from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPNEAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")
NAMESPACE = os.getenv("NAMESPACE")

def retrieve_context(query, top_k=5):
    """
    Embeds the query, searches Pinecone, and returns the top_k matches with metadata.
    """
    pinecone = Pinecone(
        api_key=PINECONE_API_KEY,
        )

    index = pinecone.Index(INDEX_NAME)

    q_emb = pinecone.inference.embed(
        model="multilingual-e5-large",
        inputs=query,
        parameters={"input_type": "passage", "truncate": "END"}
    )

    result = index.query(
        vector=q_emb.get("data")[0]['values'],
        top_k=top_k,
        include_values=True,
        include_metadata=True,
        namespace=NAMESPACE
    )
    return result.matches

def chat_with_sources(query):
    client = OpenAI(
    api_key=OPNEAI_API_KEY
    )
    """
    Retrieves context, constructs a prompt with source annotations,
    and calls ChatGPT to generate a response that cites each PDF source.
    """
    matches = retrieve_context(query)

    context_sections = []
    for m in matches:
        ctx = m.metadata.get("text", "")  # if you stored text in metadata
        src = m.metadata["source"]
        context_sections.append(f"[{src} ]\n{ctx}")

    context_text = "\n\n".join(context_sections)


    system_prompt = (
        "You are a helpful assistant. Use the following context to answer "
        "the user’s question, and for each piece of information you use, "
        "indicate its source in square brackets like [source.pdf, page X].\n\n"
        f"{context_text}"
    )

    response = client.responses.create(    
        model="gpt-4.1-mini-2025-04-14",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": query}
        ],
        temperature=0.2
    )
    return response.output_text