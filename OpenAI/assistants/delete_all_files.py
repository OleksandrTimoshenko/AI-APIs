from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/../.env")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def delete_all_files(client):
    # List all files
    files = client.files.list()

    # Iterate through the files and delete each one
    for file in files.data:
        file_id = file.id
        client.files.delete(file_id)
        print(f"Deleted file: {file_id}")

    print("All files have been deleted.")

delete_all_files(client)
