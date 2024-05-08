import streamlit as st
import time
import os
import json
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = 'open_ai_key'

# Read document
with open("parsed_manifesto.txt", "r") as f:
    document = f.read()


# Chat Assistant
client = OpenAI()
system_instruct = [
    {
      "role": "system",
      "content": "You are a helpful assistant for a political party named 'BJP'. This is the content of the manifesto of the party.\n"+ document + "\nYou will answer user questions about this content. You must not answer any questions not related to BJP manifesto."
    }]


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

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Call open AI api with entire convo so far
        response = client.chat.completions.create(
        model="gpt-4-1106-vision-preview",
        messages=system_instruct+st.session_state.messages,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
        )

        print(st.session_state.messages)

        json_obj = json.loads(response.model_dump_json())
        reply = json_obj['choices'][0]["message"]["content"]
        # chat_history.append({"role": "assistant", "content": reply})
        response = st.write_stream(response_generator(reply))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})