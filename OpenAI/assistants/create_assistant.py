from openai import OpenAI
import os
from dotenv import load_dotenv
from handlers.work_with_json_handlers import update_assistants_json
from handlers.openai_api_handlers import create_assistant, create_vector_store, add_vector_store_to_assistant

load_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/../.env")

PROJECT_NAME =  os.getenv("PROJECT_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":

  client = OpenAI()
  file_path = os.getenv("ASSISTANTS_FILE")

  # Step 1: Create a new Assistant with File Search Enabled
  assistant = create_assistant(client, f"{PROJECT_NAME} AI assistant", os.getenv("ASSISTANT_INSTRUCTION"), os.getenv("ASSISTANT_MODEL"))
  print("Created assistand ID for " + PROJECT_NAME + ": " + assistant.id)

  # Step 2: Create vactore store
  vector_store = create_vector_store(client, f"{PROJECT_NAME} vector store")

  # Step 3: Update the assistant to to use the new Vector Store
  add_vector_store_to_assistant(client, assistant.id, vector_store.id)

  # Step 4: Create the JSON structure and add to or create assistants.json
  update_assistants_json(file_path, assistant.id, vector_store.id, PROJECT_NAME)