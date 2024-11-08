from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta, timezone
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import json

service_name = 'name'
index_name = 'name'
api_key = 'key'
endpoint = f'https://{service_name}.search.windows.net'
connection_string = "string
container_name = "name"


# # Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# List blobs in the container
client = SearchClient(endpoint=endpoint,
                       index_name=index_name,
                       credential=AzureKeyCredential(api_key))

time_threshold = datetime.now(timezone.utc) - timedelta(days=1)  # upto one day old data


blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


new_files = []

for blob in container_client.list_blobs():
    if blob.last_modified >= time_threshold:
        new_files.append(blob.name)

updated_files=[]

if new_files:
    print("Newly updated files:")
    for file in new_files:
        updated_files.append(file)
        
else:
    print("No newly updated files found.")


print(updated_files)


for file_id in updated_files:
    results = client.search(search_text=file_id)
    if results:
        found = any(True for _ in results)  
        if found:
            print(f"File with ID '{file_id}' is indexed.")
        else:
            print(f"File with ID '{file_id}' is not indexed.")
    else:
        print(f"No results returned for file ID '{file_id}'.")




