import streamlit as st
import time
import os
import json
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = 'open_ai_key'

def format_text(text):
    # Split the text into lines
    lines = text.split('\n')
    formatted_lines = []
    
    # Check each line for a bullet point indicator
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(('- ', '* ')):  # Add more conditions if needed
            # Convert to Markdown bullet point
            formatted_lines.append("* " + stripped_line[2:])
        else:
            formatted_lines.append(line)
    
    # Join the lines back together
    return "\n".join(formatted_lines)

# Read document
# with open("parsed_manifesto_pg8-19.txt", "r") as f:
#     document = f.read()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pypdf import PdfReader
# import numpy as np

reader = PdfReader("/Users/kaustubh/Downloads/Modi-Ki-Guarantee-Sankalp-Patra-English_2.pdf")
number_of_pages = len(reader.pages)
pages = []
# with open('parsed_manifesto_pg8-19.txt', 'a') as f:
for i in range(number_of_pages):
    page = reader.pages[i]
    text = page.extract_text()
    pages.append(text)

# Example document and query
# documents = docs  # these would be your document chunks
# vectorizer = TfidfVectorizer()
# tfidf = vectorizer.fit_transform(documents)

# query = vectorizer.transform(["user's question"])
# cosine_similarities = linear_kernel(query, tfidf).flatten()
# relevant_doc_indices = cosine_similarities.argsort()[:-4:-1]  # top 3 relevant pages


# Chat Assistant
client = OpenAI()
# system_instruct = [
#     {
#       "role": "system",
#       "content": "You are a helpful assistant for a political party named 'BJP'. This is the content of the manifesto of the party.\n"+ document + "\nYou will answer user questions about this content. You must not answer any questions not related to BJP manifesto."
#     }]


# Streamed response emulator
def response_generator(response="Hello! How can I assist you today?"):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("ChatGPT-like assistant for BJP manifesto!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": 'Hello! How may I help you today?'}]

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask away!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        # chat_history.append({"role": "user", "content": prompt})

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(pages)

    query = vectorizer.transform([prompt])
    cosine_similarities = linear_kernel(query, tfidf).flatten()
    relevant_doc_indices = cosine_similarities.argsort()[:-5:-1] #top4
    document = ""
    for i in relevant_doc_indices:
        document += pages[i]
    system_instruct = [
    {
      "role": "system",
      "content": "You are a helpful assistant for a political party named 'BJP'. This is the relevant content from the manifesto document of the party.\n"+ document + "\nYou will answer user questions about this content. You must not answer any questions not related to BJP manifesto."
    }]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Call open AI api with entire convo so far
        response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=system_instruct+st.session_state.messages,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
        )

        print(relevant_doc_indices)

        # print(st.session_state.messages)

        json_obj = json.loads(response.model_dump_json())
        reply = json_obj['choices'][0]["message"]["content"]
        # chat_history.append({"role": "assistant", "content": reply})
        formatted_response = format_text(reply)
        # st.markdown(formatted_response)
        response = st.write_stream(response_generator(formatted_response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})