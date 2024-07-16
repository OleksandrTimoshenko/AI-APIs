from openai import OpenAI
import os, sys
from dotenv import load_dotenv
from handlers.openai_api_handlers import delete_vector_store_file, upload_vector_store_file
from handlers.work_with_json_handlers import *

'''
Hints about logic
1. every file from trainingData folder will be uploaded to AI asistant
2. if file with such name already exist it will be updated
3. If we will have more than one file with one name all of them will be deleted and replaced with new one (so avoid names duplications)
4. If vector store doesn`t used in any asistant program will inform you about that
5. If vector store used in more than 1 assiatant all of tham will be effected
'''

def get_all_files(folder):
    # Get a list of all files in the specified folder and its subfolders
    files = []
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                files.append(file_path)
    return files

if __name__ == "__main__":
  load_dotenv()

  PROJECT_NAME =  os.getenv("PROJECT_NAME")
  os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

  client = OpenAI()

  if len(sys.argv) != 2:
        print("Usage: script.py vector_store_id>, or")
        vector_store_id = input("Enter your vector_store_id: ")
  else:
        vector_store_id = sys.argv[1]
  file_path = os.getenv("ASSISTANTS_FILE")
  updated_files = get_all_files("./trainingData")
  get_assistants_using_vector_store(vector_store_id, file_path)
  files_in_vector_store = get_files_from_vector_store(vector_store_id, file_path)

  for file in updated_files:
      filename = os.path.basename(file)
      # deleting existing in vector store files by names
      for file_id in get_file_ids_in_vector_store(filename, files_in_vector_store):
          delete_vector_store_file(client, vector_store_id, file_id)
          delete_vector_store_file_from_json(vector_store_id, file_id, file_path)
      # add new file to vector store
      new_file_id = upload_vector_store_file(client, vector_store_id, file)
      add_vector_store_file_to_json(vector_store_id, filename, new_file_id, file_path)
