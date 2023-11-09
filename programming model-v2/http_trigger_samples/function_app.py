import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="http_trigger_auth")
def http_trigger_auth(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    oid = req.headers.get('X-MS-CLIENT-PRINCIPAL-ID')

    if not oid:
        oid = "No OID found"
        
    return func.HttpResponse(oid)
