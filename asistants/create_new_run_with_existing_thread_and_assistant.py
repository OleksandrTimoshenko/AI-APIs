from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import os
from dotenv import load_dotenv
import sys
import re

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

if len(sys.argv) != 3:
    print("Usage: script.py <assistant_id> <thread_id>, or")
    assistant_id = input("Enter your assistant_id: ")
    thread_id = input("Enter thread id:")
else:
    assistant_id = sys.argv[1]
    thread_id = sys.argv[2]

client = OpenAI()

# add message to Thread
message = client.beta.threads.messages.create(
  thread_id=thread_id,
  role="user",
  content=os.getenv("THREAD_QUESTION")
)

# it use also thread history, so I need to add context to every calculation
#total_tokens = count_tokens(os.getenv("RUN_INSTRUCTION") + os.getenv("THREAD_QUESTION"), model=os.getenv("ASSISTANT_MODEL"))
#print(f"Estimated tokens for the run: {total_tokens}")

# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.

'''
# start main process with streaming
with client.beta.threads.runs.stream(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions=os.getenv("RUN_INSTRUCTION"),
  event_handler=EventHandler(),
) as stream:
  stream.until_done()

'''
# start main process without streaming
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions=os.getenv("RUN_INSTRUCTION")#,
  #max_prompt_tokens=5000,
  #max_completion_tokens=2000
  # Error
  # Run(id='run_gu0axPjFjvBMNGTOrCWToy3x', assistant_id='asst_qUhQPm06NSyrsWqmceIQnW9j', cancelled_at=None, completed_at=None, created_at=1719836471, expires_at=None, failed_at=1719836474, incomplete_details=None, instructions='Please address the user as Dear Astounder. The user has a premium account', last_error=LastError(code='server_error', message='Sorry, something went wrong.'), max_completion_tokens=2000, max_prompt_tokens=5000, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1719836473, status='failed', thread_id='thread_SRgj1Fdh2Y3twJWClaxD3C0p', tool_choice='auto', tools=[FileSearchTool(type='file_search', file_search=None)], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=Usage(completion_tokens=18, prompt_tokens=1469, total_tokens=1487), temperature=1.0, top_p=1.0, tool_resources={})
  
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread_id
  )
  #print(messages)
  content = messages.data[0].content[0].text.value
  cleaned_content = re.sub(r"【\d+†source】", "", content)
  cleaned_content = cleaned_content.strip()
  print(cleaned_content)
  usage = run.usage
  print(f"Total tokens used: {usage.total_tokens}")
  print(f"Prompt tokens used: {usage.prompt_tokens}")
  print(f"Completion tokens used: {usage.completion_tokens}")
else:
  print(run)
