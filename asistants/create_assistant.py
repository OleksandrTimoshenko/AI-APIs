from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME =  os.getenv("PROJECT_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def get_all_files(folder):
    # Get a list of all files in the specified folder
    files = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files

if __name__ == "__main__":

  client = OpenAI()

  # Step 1: Create a new Assistant with File Search Enabled
  assistant = client.beta.assistants.create(
    name=PROJECT_NAME + " AI assistant",
    instructions=os.getenv("ASSISTANT_INSTRUCTION"),
    model=os.getenv("ASSISTANT_MODEL"),
    tools=[{"type": "file_search"}],
  )

  print("Created assistand ID for " + PROJECT_NAME + ": " + assistant.id)
