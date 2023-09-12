import logging
import os
import json
import tempfile

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tempFilePath = tempfile.gettempdir()
    print(tempFilePath)

    vals = json.dumps({**{}, **os.environ})
    print(vals)
    return func.HttpResponse(vals)
