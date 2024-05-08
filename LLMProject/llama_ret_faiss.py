# from langchain_community.llms import Ollama
# from langchain_core.prompts import ChatPromptTemplate
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a world class technical documentation writer."),
#     ("user", "{input}")
# ])
# llm = Ollama(model="llama3")
# from langchain_core.output_parsers import StrOutputParser
# output_parser = StrOutputParser()
# chain = prompt | llm | output_parser

# print(chain.invoke({"input": "how can langsmith help with testing?"}))
from langchain_core.documents import Document
from pypdf import PdfReader
# import numpy as np

reader = PdfReader("/Users/kaustubh/Downloads/Modi-Ki-Guarantee-Sankalp-Patra-English_2.pdf")
number_of_pages = len(reader.pages)
docs = []
# with open('parsed_manifesto_pg8-19.txt', 'a') as f:
for i in range(8,16):
    page = reader.pages[i]
    text = page.extract_text()
    docs.append(Document(page_content=text))

from langchain_community.llms import Ollama
llm = Ollama(model="llama3")

from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model='llama3')

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

from langchain.chains import create_retrieval_chain

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": "Tell 2 bullet points for infrasture and economy in manifesto"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...