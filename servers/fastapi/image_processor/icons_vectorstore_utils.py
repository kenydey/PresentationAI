import json
import os
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


def get_icons_vectorstore():
    vector_store_path = "assets/icons_vectorstore.json"

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(vector_store_path):
        vector_store = InMemoryVectorStore.load(vector_store_path, embeddings)
        return vector_store

    vector_store = InMemoryVectorStore(embeddings)

    with open("assets/icons.json", "r") as f:
        icons = json.load(f)

    texts = [icon["name"] for icon in icons["icons"]]
    documents = [Document(id=text, page_content=text) for text in texts]
    vector_store.add_documents(documents)
    vector_store.dump(vector_store_path)
    return vector_store
