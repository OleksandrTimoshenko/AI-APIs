from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import sys

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if len(sys.argv) != 2:
    print("Usage: script.py <assistant_id>, or")
    assistant_id = input("Enter your assistant_id: ")
else:
    assistant_id = sys.argv[1]

client = OpenAI()

# creating a Thread
thread = client.beta.threads.create()

# add message to Thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content=os.getenv("THREAD_QUESTION")
)

print("thread ID: " + thread.id)

# start main process
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant_id,
  instructions=os.getenv("RUN_INSTRUCTION")
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  #print(messages)
  content = messages.data[0].content[0].text.value
  cleaned_content = re.sub(r"【\d+†source】", "", content)
  cleaned_content = cleaned_content.strip()
  print(cleaned_content)
else:
  print(run)