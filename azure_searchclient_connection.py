from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
import os
from dotenv import load_dotenv

load_dotenv()

service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
key = os.getenv("AZURE_SEARCH_API_KEY")

# Create the SearchIndexClient
index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

# Check if the index exists
try:
    index = index_client.get_index(index_name)
    print(f"Index '{index_name}' exists. Details: {index}")
    for field in index.fields:
        print(f"Field name: {field.name}, Type: {field.type}")

except Exception as e:
    print(f"An error occurred: {e}")


