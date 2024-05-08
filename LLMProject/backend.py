import os
import json
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = 'open_ai_key'

# Read document
f = open("parsed_manifesto_pg8-19.txt", "r")
document = f.read()


# Chat Assistant
client = OpenAI()
chat_history = [
    {
      "role": "system",
      "content": "You are a helpful assistant for a political party named 'BJP'. This is the content of the manifesto of the party. "+ document + "You will answer user questions about this content. You must not answer any questions not related to BJP manifesto."
    },
    {"role": "assistant",
     "content": "Hello! How may I help you today?"
     },
    # {
    #   "role": "user",
    #   "content": "Hi, I have few questions about BJP manifesto. Can you tell me in 2 bullet points, what promises BJP made to women of country?"
    # },
  ]

try:
  print('Assistant: Hi! How may I help you today?')
  while True:
    # Take question from user
    val = input("\nUser: ") 
    msg = {"role": "user",
           "content": val}
    chat_history.append(msg)

    # Call open AI api with entire convo so far
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=chat_history,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
    )

    json_obj = json.loads(response.model_dump_json())
    reply = json_obj['choices'][0]["message"]["content"]
    print('\nAssistant: ', reply)
    msg = {"role": "assistant",
           "content": reply}
    chat_history.append(msg)

except KeyboardInterrupt:
  print('\nChat Closed...Thank you!')




# assistant = client.beta.assistants.retrieve(assistant_id='asst_mwJGR4V0UnVscbUouGSK3PTh')

# thread = client.beta.threads.create()

# message = client.beta.threads.messages.create(
#   thread_id=thread.id,
#   role="user",
#   content="Hi, I want to know what promises BJP made for women in 2 bullet points only."
# )

# run = client.beta.threads.runs.create_and_poll(
#   thread_id=thread.id,
#   assistant_id=assistant.id
# )

# if run.status == 'completed': 
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages)
# else:
#   print(run.status)