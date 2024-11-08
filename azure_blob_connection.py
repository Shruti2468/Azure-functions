import os
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import glob
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobBlock, BlobClient, StandardBlobTier

# Implementing passwordless connections to Azure services
account_url = "https://<storagename>.blob.core.windows.net"
default_credential = DefaultAzureCredential()

load_dotenv()

# Create the BlobServiceClient object
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

container_name = 'name'

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)
folder_path = glob.glob("data/*")

try:
    print("Azure Blob Storage Python quickstart sample")

    # Create a local directory to hold blob data
    local_path = ".\data"

    for local_path in folder_path:
        upload_file_path = local_path
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(local_path))

        with open(upload_file_path, "rb") as data:
            blob_client = blob_client.upload_blob(data=data, overwrite=True)
            # , standard_blob_tier=StandardBlobTier.COOL
            print("uploaded: ", os.path.basename(local_path))

    print("\nListing blobs...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)
    print("\nDownloading files")
    download_local_path = ".//downloads"
    os.makedirs(download_local_path, exist_ok=True)

    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t downloading " + blob.name)
        # Replace '/' with os.sep to maintain directory structure sep is path separator 
        download_file_path = os.path.join(download_local_path, blob.name.replace('/', os.sep))
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())
except Exception as ex:
    print('Exception:')
    print(ex)
