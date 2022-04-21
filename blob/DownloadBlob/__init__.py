import logging
import tempfile
import os
import uuid

import azure.functions as func
from azure.storage.blob import BlobClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 環境変数から接続文字列の取得
    # https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#environment-variables
    blob_connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    # ファイルを保存するパスは、ローカルデバッグなら "./Download" (local.settings.json で定義), Function App なら ./tmp 
    # 一時ファイル: https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#temporary-files
    download_path = tempfile.gettempdir()

    container_name = "sample-data"

    # Blob の "sample-data" container に "sample.txt" または "cat.png" が存在する想定
    blob_name = "sample.txt"
    # blob_name = "cat.png"
    
    local_file_path = f"{download_path}/{str(uuid.uuid4())}-{blob_name}"
    logging.info(f"local_file_path: {local_file_path}" )

    # BlobClient: https://docs.microsoft.com/ja-jp/azure/developer/python/sdk/storage/azure-storage-blob/azure.storage.blob.blobclient
    blob_client = BlobClient.from_connection_string(blob_connection_string, container_name, blob_name)

    if blob_client.exists() == False:
         return func.HttpResponse(f"ERROR: 事前に Blob の {container_name} コンテナーに {blob_name} をアップロードしてね！")
    
    with open(local_file_path, "wb") as local_blob:
        stream = blob_client.download_blob()
        local_blob.write(stream.readall())

    return func.HttpResponse(f"Downloaded file: '{local_file_path}'")
