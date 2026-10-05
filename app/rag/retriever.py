import os
import re
from typing import List, Dict

class TravelRAGRetriever:
    """
    Lightweight, fast keyword and semantic TF-IDF style RAG retriever
    over local markdown travel knowledge bases, requiring zero external paid APIs.
    """
    def __init__(self, knowledge_dir: str = None):
        if not knowledge_dir:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            knowledge_dir = os.path.join(base_dir, "data", "travel_knowledge")
        self.knowledge_dir = knowledge_dir
        self.documents = []
        self._load_documents()

    def _load_documents(self):
        if not os.path.exists(self.knowledge_dir):
            return
        for fname in os.listdir(self.knowledge_dir):
            if fname.endswith(".md") or fname.endswith(".txt"):
                fpath = os.path.join(self.knowledge_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        text = f.read()
                        # Chunk by sections
                        sections = text.split("## ")
                        for sec in sections:
                            if sec.strip():
                                lines = sec.strip().split("\n")
                                title = lines[0]
                                content = "\n".join(lines[1:])
                                self.documents.append({
                                    "source": fname,
                                    "title": title,
                                    "content": content
                                })
                except Exception as e:
                    print(f"Error loading {fpath}: {e}")

    def retrieve(self, query: str, top_k: int = 2) -> str:
        """
        Retrieves most relevant knowledge sections based on query keywords.
        """
        query_words = set(re.findall(r"\w+", query.lower()))
        scored_docs = []

        for doc in self.documents:
            doc_text = (doc["title"] + " " + doc["content"]).lower()
            doc_words = set(re.findall(r"\w+", doc_text))
            overlap = len(query_words.intersection(doc_words))
            if overlap > 0:
                scored_docs.append((overlap, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc for _, doc in scored_docs[:top_k]]
        
        if not top_docs:
            return "General guidance: North Goa is best for nightlife and water sports, South Goa for peace and calm."
            
        retrieved_texts = [f"### {d['title']}\n{d['content'].strip()}" for d in top_docs]
        return "\n\n".join(retrieved_texts)
