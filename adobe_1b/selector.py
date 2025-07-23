from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_sections(persona, job, pdf_chunks):
    query = f"{persona['role']} needs to {job['task']}"
    texts = []
    metadata = []

    for doc in pdf_chunks:
        for chunk in doc["chunks"]:
            texts.append(chunk["text"])
            metadata.append({
                "document": doc["filename"],
                "section_title": chunk["heading"],
                "page_number": chunk["page"]
            })

    if not texts:
        print("⚠️ No valid sections found to rank. Returning empty results.")
        return [], []

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([query] + texts)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    for i, score in enumerate(similarities):
        metadata[i]["score"] = score
        metadata[i]["text"] = texts[i]

    top = sorted(metadata, key=lambda x: -x["score"])[:5]

    extracted = []
    refined = []
    for i, item in enumerate(top):
        extracted.append({
            "document": item["document"],
            "section_title": item["section_title"],
            "importance_rank": i + 1,
            "page_number": item["page_number"]
        })
        refined.append({
            "document": item["document"],
            "refined_text": item["text"],
            "page_number": item["page_number"]
        })

    return extracted, refined
