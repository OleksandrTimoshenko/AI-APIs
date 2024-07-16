from openai import OpenAI
import os
from dotenv import load_dotenv
from handlers.openai_api_handlers import list_all_vector_stores, delete_vector_store
from handlers.work_with_json_handlers import get_all_vector_store_ids

load_dotenv()

PROJECT_NAME =  os.getenv("PROJECT_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    client = OpenAI()
    file_path = os.getenv("ASSISTANTS_FILE")
    all_vectore_stores_in_account = list_all_vector_stores(client)
    used_vectore_stores = get_all_vector_store_ids(file_path)
    unused_vectore_stores = [x for x in all_vectore_stores_in_account if x not in used_vectore_stores]
    print(f"This vector stores unused and will be deleted: {unused_vectore_stores}")
    for unused_vectore_store in unused_vectore_stores:
        delete_vector_store(client, unused_vectore_store)