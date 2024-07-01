from openai import OpenAI
import os
from dotenv import load_dotenv
import datetime
#import tiktoken
#from PyPDF2 import PdfReader

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

"""
def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
    
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
    return text
"""

if __name__ == "__main__":

  client = OpenAI()

  #assistant_creation_tokens = count_tokens(os.getenv("ASSISTANT_INSTRUCTION"), model=os.getenv("ASSISTANT_MODEL")) + 1  # +1 for the model name
  #print(f"Estimated tokens for assistant creation: {assistant_creation_tokens}")

  total_training_tokens = 0
  file_paths = get_all_files("./trainingData")
  """
  for path in file_paths:
    # TODO: add different files pypes here
    if path.endswith(".pdf"):
      text = extract_text_from_pdf(path)
      total_training_tokens += count_tokens(text, model=os.getenv("ASSISTANT_MODEL"))
  
  print(f"Estimated tokens for training: {total_training_tokens}")
  """


  # Step 1: Create a new Assistant with File Search Enabled
  assistant = client.beta.assistants.create(
    name=PROJECT_NAME + " AI assistant",
    instructions=os.getenv("ASSISTANT_INSTRUCTION"),
    model=os.getenv("ASSISTANT_MODEL"),
    tools=[{"type": "file_search"}],
  )

  ### You can do Steps 2 and 3 every time when files changed

  # Step 2: Upload files and add them to a Vector Store
  vector_store = client.beta.vector_stores.create(name=PROJECT_NAME + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  file_streams = [open(path, "rb") for path in file_paths]
  # Use the upload and poll SDK helper to upload the files, add them to the vector store,
  # and poll the status of the file batch for completion.
  file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
  )
  # You can print the status and the file counts of the batch to see the result of this operation.
  print(file_batch.status)
  print(file_batch.file_counts)
  print(vector_store.id)

  # Step 3: Update the assistant to to use the new Vector Store
  # TODO: investigate fow we can add only changed files to model (if it`s possible)
  assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
  )

  print("Created assistand ID for " + PROJECT_NAME + ": " + assistant.id)
