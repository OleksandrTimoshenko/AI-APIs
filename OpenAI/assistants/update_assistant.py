from openai import OpenAI
import os, sys
from dotenv import load_dotenv
#from handlers.work_with_json_handlers import update_assistants_json
from handlers.openai_api_handlers import update_assistant

load_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/../.env")

PROJECT_NAME =  os.getenv("PROJECT_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":

  if len(sys.argv) != 2:
        print("Usage: script.py assistant_id>, or")
        assistant_id = input("Enter your assistant_id: ")
  else:
        assistant_id = sys.argv[1]

  client = OpenAI()
  updated_assistant = update_assistant(client, assistant_id, f"{PROJECT_NAME} AI assistant", os.getenv("ASSISTANT_INSTRUCTION"), os.getenv("ASSISTANT_MODEL"))
  print(f"Assistant {updated_assistant.id} updated.")