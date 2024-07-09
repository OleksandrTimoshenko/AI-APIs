from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# creating a Thread
thread = client.beta.threads.create()

print("thread ID: " + thread.id)
