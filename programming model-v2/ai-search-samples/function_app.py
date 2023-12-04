import os
import azure.functions as func
import json
import logging
import openai

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import RawVectorQuery, VectorFilterMode

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15"
DEPLOYMENT_ID = "text-embedding-ada-002"
search_client = SearchClient(os.getenv("COGNITIVE_SEARCH_ENDPOINT"),
                             os.getenv("COGNITIVE_SEARCH_INDEX_NAME"), 
                             AzureKeyCredential(os.getenv("COGNITIVE_SEARCH_QUERY_KEY")))


def vector_search(text: str):
    # ベクター化した質問の文章を使って、Cognitive Search でベクター検索
    vector_query = RawVectorQuery(vector=get_embedding(text), k=3, fields="contentVector")
    search_results = search_client.search(
        search_text="",
        vector_queries=[vector_query],
        select=["title", "content", "category"],
    )

    items = []
    for search_result in search_results:
        items.append({
            "title": search_result["title"],
            "content": search_result["content"],
            "category": search_result["category"],
            "score": search_result["@search.score"]
        })
        
    return items


def vector_search_with_filter(text: str, category: str):
    # フィルターをかける場合は、vector_filter_mode で pre fileter (default) or post filter ができる。
    # https://github.com/Azure/cognitive-search-vector-pr/blob/main/demo-python/code/azure-search-vector-python-sample.ipynb
    vector = get_embedding(text)
    vector_query = RawVectorQuery(vector=vector, k=3, fields="contentVector")
    results = search_client.search(
        search_text="",
        vector_queries=[vector_query],
        vector_filter_mode=VectorFilterMode.PRE_FILTER,
        filter=f"category eq '{category}'",
        select=["title", "content", "category"],
    )

    items = []
    for result in results:
        items.append({
            "title": result["title"],
            "content": result["content"],
            "category": result["category"],
            "score": result["@search.score"]
        })
        
    return items

def get_embedding(text: str):
    embedding = openai.Embedding.create(input=text, deployment_id=DEPLOYMENT_ID)["data"][0]["embedding"]
    return embedding

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="search", methods=["GET"])
def search(req: func.HttpRequest) -> func.HttpResponse:

    query = req.params.get('query')
    if not query:
        return func.HttpResponse(
            "クエリ文字列 'query' に検索したい文字列を指定してください。",
             status_code=400
        )

    search_results = vector_search(query)
    logging.info(f"search_results:{search_results}")

    return func.HttpResponse(
            json.dumps(search_results),
            mimetype="application/json",
            status_code=200
    )

@app.route(route="search_filter", methods=["GET"])
def search_filter(req: func.HttpRequest) -> func.HttpResponse:

    query = req.params.get('query')

    if not query:
        return func.HttpResponse(
            "クエリ文字列 'query' に検索したい文字列を指定してください。",
             status_code=400
        )
    
    category = req.params.get('category')

    search_results = vector_search_with_filter(query, category)
    logging.info(f"search_results:{search_results}")

    return func.HttpResponse(
            json.dumps(search_results),
            mimetype="application/json",
            status_code=200
    )
