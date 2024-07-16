import os
import json

def update_assistants_json(file_path, assistant_id, vector_store_id, PROJECT_NAME):
  assistant_json = {
        "assigned_assistant_name": f"{PROJECT_NAME} AI assistant",
        "assigned_assistant_id": assistant_id,
        "vector_stores": [
            {
                "vector_store_name": f"{PROJECT_NAME} vector store",
                "vector_store_id": vector_store_id,
                "files": []
            }
        ]
    }

  # Check if the file already exists
  if os.path.exists(file_path):
      # Load the existing file
      with open(file_path, "r") as json_file:
          data = json.load(json_file)
          
      # Check if "assistants" array exists
      if "assistants" in data:
          # Append the new assistant to the existing array
          data["assistants"].append(assistant_json)
      else:
          # Create the "assistants" array and add the new assistant
          data["assistants"] = [assistant_json]
  else:
      # Create a new structure with the "assistants" array
      data = {
          "assistants": [assistant_json]
      }
   # Write the updated structure back to the file in a human-readable format
  with open(file_path, "w") as json_file:
      json.dump(data, json_file, indent=4)

  print(f"JSON file updated: {file_path}")

def get_assistants_using_vector_store(vector_store_id, file_path):

    # Check if the file exists
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    # Load the existing file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Check if "assistants" array exists
    if "assistants" not in data:
        print("No assistants found in the file.")
        return

    # Find assistants using the given vector store ID
    affected_assistants = []
    for assistant in data["assistants"]:
        for vector_store in assistant.get("vector_stores", []):
            if vector_store["vector_store_id"] == vector_store_id:
                affected_assistants.append({
                    "assigned_assistant_name": assistant["assigned_assistant_name"],
                    "assigned_assistant_id": assistant["assigned_assistant_id"]
                })

    if affected_assistants:
        print("This vector store is used by the following assistants:")
        for assistant in affected_assistants:
            print(f"- {assistant['assigned_assistant_name']} (ID: {assistant['assigned_assistant_id']})")
    else:
        print("WARNING!!!: No assistants are using this vector store.")

def get_files_from_vector_store(vector_store_id, file_path):

    # Check if the file exists
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    # Load the existing file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Check if "assistants" array exists
    if "assistants" not in data:
        print("No assistants found in the file.")
        return

    # Find the files in the given vector store ID
    for assistant in data["assistants"]:
        for vector_store in assistant.get("vector_stores", []):
            if vector_store["vector_store_id"] == vector_store_id:
                return vector_store["files"]

    print("Vector store not found.")
    return []

def get_file_ids_in_vector_store(filename, files_in_vector_store):
    file_ids = []
    for file_info in files_in_vector_store:
        if file_info['filename'] == filename:
            file_ids.append(file_info['vector_store_file_id'])
    return file_ids

def delete_vector_store_file_from_json(vector_store_id, file_id, json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Iterate through assistants
    for assistant in data["assistants"]:
        # Iterate through vector stores within each assistant
        for vector_store in assistant["vector_stores"]:
            if vector_store["vector_store_id"] == vector_store_id:
                # Filter out the file with the given file_id
                vector_store["files"] = [
                    file for file in vector_store["files"]
                    if file["vector_store_file_id"] != file_id
                ]
    
    # Save the updated JSON data back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def add_vector_store_file_to_json(vector_store_id, filename, new_file_id, json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # New file object to add
    new_file = {
        "filename": filename,
        "vector_store_file_id": new_file_id
    }
    
    # Iterate through assistants
    for assistant in data["assistants"]:
        # Iterate through vector stores within each assistant
        for vector_store in assistant["vector_stores"]:
            if vector_store["vector_store_id"] == vector_store_id:
                # Add the new file to the files array
                vector_store["files"].append(new_file)
    
    # Save the updated JSON data back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def delete_assistant_from_json(assistant_id, json_file):

    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Filter out the assistant with the given assistant_id
    data["assistants"] = [
        assistant for assistant in data["assistants"]
        if assistant["assigned_assistant_id"] != assistant_id
    ]
    
    # Save the updated JSON data back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def get_all_vector_store_ids(json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    vector_store_ids = []
    
    # Iterate through assistants and their vector stores to collect vector store IDs
    for assistant in data["assistants"]:
        for vector_store in assistant.get("vector_stores", []):
            vector_store_ids.append(vector_store["vector_store_id"])
    
    return vector_store_ids

def get_vector_stores_by_assistant(assistant_id, json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Iterate through assistants to find the matching assistant_id
    for assistant in data["assistants"]:
        if assistant["assigned_assistant_id"] == assistant_id:
            return assistant.get("vector_stores", [])
    
    return []  # Return an empty list if the assistant_id is not found

def is_vector_store_used_by_other_assistants(vector_store_id, current_assistant_id, json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    using_assistants = []
    
    # Iterate through assistants and their vector stores to check usage
    for assistant in data["assistants"]:
        if assistant["assigned_assistant_id"] == current_assistant_id:
            continue  # Skip the current assistant
        for vector_store in assistant.get("vector_stores", []):
            if vector_store["vector_store_id"] == vector_store_id:
                using_assistants.append(assistant["assigned_assistant_name"])
    
    # Print the list of assistants that use the vector store
    if using_assistants:
        print(f"Vector store '{vector_store_id}' is used by the following assistants (excluding current assistant): {using_assistants}")
        return True
    else:
        print(f"Vector store '{vector_store_id}' is not used by any other assistants.")
        return False

def is_file_id_used_in_vector_stores(file_id, json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    using_vector_stores = []
    
    # Iterate through assistants and their vector stores to check file usage
    for assistant in data["assistants"]:
        for vector_store in assistant.get("vector_stores", []):
            for file in vector_store.get("files", []):
                if file["vector_store_file_id"] == file_id:
                    using_vector_stores.append(vector_store["vector_store_name"])
    
    # Print the names of vector stores that use the file
    if using_vector_stores:
        print(f"File ID '{file_id}' is used by the following vector stores: {using_vector_stores}")
        return True
    else:
        print(f"File ID '{file_id}' is not used by any vector stores.")
        return False