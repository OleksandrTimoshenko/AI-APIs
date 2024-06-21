from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import os
from dotenv import load_dotenv
import re
import sys

load_dotenv()

class EventHandler(AssistantEventHandler):
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)

  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)

  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)

  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

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

# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.

# start main process with streaming
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant_id,
  instructions=os.getenv("RUN_INSTRUCTION"),
  event_handler=EventHandler(),
) as stream:
  stream.until_done()

'''
# start main process without streaming
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
'''