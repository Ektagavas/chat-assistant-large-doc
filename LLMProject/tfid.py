from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pypdf import PdfReader
# import numpy as np

reader = PdfReader("/Users/kaustubh/Downloads/Modi-Ki-Guarantee-Sankalp-Patra-English_2.pdf")
number_of_pages = len(reader.pages)
docs = []
# with open('parsed_manifesto_pg8-19.txt', 'a') as f:
for i in range(number_of_pages):
    page = reader.pages[i]
    text = page.extract_text()
    docs.append(text)

# Example document and query
documents = docs  # these would be your document chunks
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(documents)

query = vectorizer.transform(["user's question"])
cosine_similarities = linear_kernel(query, tfidf).flatten()
relevant_doc_indices = cosine_similarities.argsort()[:-4:-1]  # top 3 relevant pages


