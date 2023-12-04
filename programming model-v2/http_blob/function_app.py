import azure.functions as func
from azure.storage.blob import BlobClient
# import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    blob_name = "sample.docx"
    container_name = "public"
    conn = "DefaultEndpointsProtocol=https;AccountName=styokosandbox;AccountKey=J5BjsRyuAE0LH/O5ZynxsNaDFv0YFnsf6ONpm0eict9DsxPm0KbDvCBhJE2eQp47YZ2UOtPcGlH8GslHY9kZMQ==;EndpointSuffix=core.windows.net"

    client = BlobClient.from_connection_string(conn_str=conn, container_name=container_name, blob_name=blob_name)

    docx_path = f"{blob_name}"
    pdf_path = f"sample.pdf"

    with open(docx_path, "wb") as docx:
        blob_data = client.download_blob()
        blob_data.readinto(docx)

    # convert docx to pdf  
    # %TMP% maps to %SYSTEMDRIVE%\local\Temp.


    return func.HttpResponse("oid")