import logging
import os
import uuid
import azure.functions as func
from azure.storage.blob import BlobClient, ContainerClient

# async 使うならこれ + aiohttp の install
# from azure.storage.blob.aio import BlobClient, BlobServiceClient, ContainerClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 環境変数から接続文字列の取得
    # https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#environment-variables
    blob_connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    container_name = "upload"

    # container が無い場合はエラーになるので事前に作る必要あり。createIfNotExists 的なメソッドはない...
    # ContainerClient: https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.containerclient?view=azure-python
    container_client = ContainerClient.from_connection_string(conn_str=blob_connection_string,container_name=container_name)
    if container_client.exists() == False:
        container_client.create_container()
        logging.info(f"Container({container_name}) created")
    
    # ローカルのファイルをアップロード
    local_file_path = "./SampleData/sample.png"
    blob_name = str(uuid.uuid4()) + ".png"

    # BlobClient: https://docs.microsoft.com/ja-jp/azure/developer/python/sdk/storage/azure-storage-blob/azure.storage.blob.blobclient
    blob_client = BlobClient.from_connection_string(blob_connection_string, container_name, blob_name)
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)

    return func.HttpResponse(f"Uploaded {container_name}/{blob_name}")
