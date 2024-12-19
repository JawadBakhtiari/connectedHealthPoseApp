'''Helper functions relating to cloud storage.'''

import data.datastore.const as const
from azure.storage.blob import BlobServiceClient

def get_blob_client(container_name: str, blob_name: str):
    '''
    Return a blob client for a given container name and blob name.
    '''
    blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)
    return blob_service_client.get_blob_client(container_name, blob_name)
