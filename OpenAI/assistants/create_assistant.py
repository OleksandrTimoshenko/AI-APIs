from openai import OpenAI
import os
from dotenv import load_dotenv
from work_with_json_handlers import update_assistants_json

load_dotenv()

PROJECT_NAME =  os.getenv("PROJECT_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":

  client = OpenAI()
  file_path = "assistants.json"

  # Step 1: Create a new Assistant with File Search Enabled
  assistant = client.beta.assistants.create(
    name=PROJECT_NAME + " AI assistant",
    instructions=os.getenv("ASSISTANT_INSTRUCTION"),
    model=os.getenv("ASSISTANT_MODEL"),
    tools=[{"type": "file_search"}],
  )

  print("Created assistand ID for " + PROJECT_NAME + ": " + assistant.id)

  # Step 2: Create vactore store
  vector_store = client.beta.vector_stores.create(
    name=f"{PROJECT_NAME} vector store"
  )
  print(f"Vector store: {vector_store.id}")

  # Step 3: Update the assistant to to use the new Vector Store
  assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
  )

  # Step 4: Create the JSON structure and add to or create assistants.json
  update_assistants_json(file_path, assistant.id, vector_store.id, PROJECT_NAME)