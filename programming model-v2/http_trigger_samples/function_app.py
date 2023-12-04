import azure.functions as func
import logging

# import os
# import tempfile
from azure.storage.blob import BlobClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="http_trigger_auth")
def http_trigger_auth(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    oid = req.headers.get('X-MS-CLIENT-PRINCIPAL-ID')

    # %TMP% maps to %SYSTEMDRIVE%\local\Temp.

    if not oid:
        oid = "No OID found"

    return func.HttpResponse(oid)


@app.route(route="local_tmp")
def local_tmp(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    blob_name = "sample.docx"
    container_name = "public"
    conn = "DefaultEndpointsProtocol=https;AccountName=styokosandbox;AccountKey=J5BjsRyuAE0LH/O5ZynxsNaDFv0YFnsf6ONpm0eict9DsxPm0KbDvCBhJE2eQp47YZ2UOtPcGlH8GslHY9kZMQ==;EndpointSuffix=core.windows.net"

    client = BlobClient.from_connection_string(conn_str=conn, container_name=container_name, blob_name=blob_name)

    docx_path = f"tmp/{blob_name}"
    # pdf_path=f"tmp/sample.pdf"

    with open(docx_path, "wb") as docx:
        blob_data = client.download_blob()    
        blob_data.readinto(docx)

    # convert docx to pdf  
    # %TMP% maps to %SYSTEMDRIVE%\local\Temp.

    return func.HttpResponse("OK")
