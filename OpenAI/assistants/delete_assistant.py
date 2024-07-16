from openai import OpenAI
import os, sys
from dotenv import load_dotenv
from handlers.work_with_json_handlers import delete_assistant_from_json, get_vector_stores_by_assistant, is_vector_store_used_by_other_assistants, is_file_id_used_in_vector_stores
from handlers.openai_api_handlers import delete_vector_store, delete_assistant

load_dotenv()

PROJECT_NAME =  os.getenv("PROJECT_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":

  if len(sys.argv) != 2:
        print("Usage: script.py assistant_id>, or")
        assistant_id = input("Enter your assistant_id: ")
  else:
        assistant_id = sys.argv[1]

  client = OpenAI()

  file_path = os.getenv("ASSISTANTS_FILE")
  files_in_deleted_vectore_store = []
  list_of_vector_stores_used_in_this_assistant = get_vector_stores_by_assistant(assistant_id, file_path)
  for vector_store in list_of_vector_stores_used_in_this_assistant:
    # if VS is not used in anoter assistant
    if not is_vector_store_used_by_other_assistants(vector_store['vector_store_id'], assistant_id, file_path):
        for file in vector_store['files']:
            files_in_deleted_vectore_store.append(file['vector_store_file_id'])
        delete_vector_store(client, vector_store['vector_store_id'])
  delete_assistant_from_json(assistant_id, file_path)
  delete_assistant(client, assistant_id)
  for file in files_in_deleted_vectore_store:
      # if file not used in another VS
      if not is_file_id_used_in_vector_stores(file, file_path):
          client.files.delete(file)

