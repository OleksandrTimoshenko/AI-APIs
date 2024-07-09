def list_all_vector_stores(client):
    vector_stores = client.beta.vector_stores.list()
    print(vector_stores)

def list_vector_store_files(client, vector_store_id):
    vector_store_files = client.beta.vector_stores.files.list(
    vector_store_id=vector_store_id
    )
    for i in vector_store_files.data:
        print(i.id)

def delete_vector_store_file(client, vector_store_id, vector_store_file_id):
    client.beta.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=vector_store_file_id
    )
    print(f"File {vector_store_file_id} deleted from vector store {vector_store_id}")

def upload_vector_store_file(client, vector_store_id, filename):
    file_streams = open(filename, "rb")
    vector_store_file = client.beta.vector_stores.files.upload_and_poll(vector_store_id=vector_store_id, file=file_streams)
    print(f"File {filename} uploaded to vector store {vector_store_id}")
    return vector_store_file.id