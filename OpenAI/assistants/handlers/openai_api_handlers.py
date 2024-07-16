def list_all_vector_stores(client):
    vector_stores_ids = []
    vector_stores = client.beta.vector_stores.list()
    for vector_store in vector_stores.data:
        vector_stores_ids.append(vector_store.id)
    return vector_stores_ids

def list_vector_store_files(client, vector_store_id):
    vector_store_files = []
    vector_store_files = client.beta.vector_stores.files.list(
    vector_store_id=vector_store_id
    )
    for file in vector_store_files.data:
        vector_store_files.append(file.id)
    return vector_store_files

def delete_vector_store_file(client, vector_store_id, vector_store_file_id):
    client.beta.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=vector_store_file_id
    )
    print(f"File {vector_store_file_id} deleted from vector store {vector_store_id}")

def delete_vector_store(client, vector_store_id):
    client.beta.vector_stores.delete(
         vector_store_id=vector_store_id
    )
    print(f"Vectore store {vector_store_id} deleted")

def upload_vector_store_file(client, vector_store_id, filename):
    file_streams = open(filename, "rb")
    vector_store_file = client.beta.vector_stores.files.upload_and_poll(vector_store_id=vector_store_id, file=file_streams)
    print(f"File {filename} uploaded to vector store {vector_store_id}")
    return vector_store_file.id

def delete_assistant(client, assistant_id):
    response = client.beta.assistants.delete(assistant_id)
    print(response)

def create_assistant(client, assistant_name, assistant_instruction, model):
  assistant = client.beta.assistants.create(
    name=assistant_name,
    instructions=assistant_instruction,
    model=model,
    tools=[{"type": "file_search"}])
  return assistant

def create_vector_store(client, name):
    vector_store = client.beta.vector_stores.create(name=name)
    print(f"Vector store: {vector_store.id}")
    return vector_store

def add_vector_store_to_assistant(client, assistant_id, vector_store_id):
    client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
  )