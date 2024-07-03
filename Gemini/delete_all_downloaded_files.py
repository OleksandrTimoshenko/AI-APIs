import google.generativeai as genai
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    # list files
    for file in genai.list_files():
        #print(file.name, " -> ", file.display_name)
        genai.delete_file(file.name)
        print(f"Deleted {file.display_name} file.")
