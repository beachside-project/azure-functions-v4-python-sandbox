import os
import azure.functions as func
import json
import logging
from openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery, VectorFilterMode

ADA_DEPLOYMENT_NAME = "text-embedding-ada-002"
GPT_DEPLOYMENT_NAME = "gpt-4"

aoai_client = AzureOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_key=os.getenv("AZURE_OPENAI_API_KEY"), api_version="2023-05-15")

DEPLOYMENT_ID = "text-embedding-ada-002"
SEMANTIC_CONFIG_NAME = "semantic-config1"
search_client = SearchClient(os.getenv("COGNITIVE_SEARCH_ENDPOINT"), os.getenv("COGNITIVE_SEARCH_INDEX_NAME"), AzureKeyCredential(os.getenv("COGNITIVE_SEARCH_QUERY_KEY")))


def semantic_ranking(text: str, lang: str):
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_semantic_search.py
    # lang: ja-jp, en-us 
    results = search_client.search(search_text=text, 
                            query_type="semantic", # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/azure/search/documents/_search_client.py#L205
                            semantic_configuration_name=SEMANTIC_CONFIG_NAME)
                            # query_language=lang の指定は不要になった？
                            
    logging.info(f"results:{results}")
          
    items = []
    for result in results:
        items.append(
            {
            "title": result["title"],
            "content": result["content"],
            "category": result["category"],
            "reranker_score": result["@search.reranker_score"]
            }
        )

    return items

def semantic_ranking_with_vector(text: str, lang: str):
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_semantic_search.py
    vector = get_embedding(text)
    vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=5, fields="contentVector")
    results = search_client.search(
            text,
            top=5,
            vector_queries=[vector_query],
            query_type="semantic",
            semantic_configuration_name=SEMANTIC_CONFIG_NAME)
            # query_language=lang)

    items = []
    for result in results:
        content = result["content"]
        items.append({"title": result["title"],
            "content": content,
            "category": result["category"],
            "search_score": result['@search.score'],
            "reranker_score": result["@search.reranker_score"]
        })

    return items


def vector_search(text: str):
    # ベクター化した質問の文章を使って、Cognitive Search でベクター検索
    vector = get_embedding(text)
    vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=3, fields="contentVector")
    search_results = search_client.search(search_text="", vector_queries=[vector_query], select=["title", "content", "category"])

    items = []
    for search_result in search_results:
        items.append({"title": search_result["title"], "content": search_result["content"], "category": search_result["category"], "score": search_result["@search.score"]})

    return items


def vector_search_with_filter(text: str, category: str):
    # フィルターをかける場合は、vector_filter_mode で pre fileter (default) or post filter ができる。
    # https://github.com/Azure/cognitive-search-vector-pr/blob/main/demo-python/code/azure-search-vector-python-sample.ipynb
    vector = get_embedding(text)
    vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=3, fields="contentVector")
    results = search_client.search(
        search_text="",
        vector_queries=[vector_query],
        vector_filter_mode=VectorFilterMode.PRE_FILTER,
        filter=f"category eq '{category}'",
        select=["title", "content", "category"],
    )

    items = []
    for result in results:
        items.append({"title": result["title"], "content": result["content"], "category": result["category"], "score": result["@search.score"]})

    return items


def get_embedding(text: str):
    embedding = aoai_client.embeddings.create(input=text, model=ADA_DEPLOYMENT_NAME).data[0].embedding
    return embedding


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="search", methods=["GET"])
def search(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get("query")
    if not query:
        return func.HttpResponse("クエリ文字列 'query' に検索したい文字列を指定してください。", status_code=400)

    search_results = vector_search(query)
    logging.info(f"search_results:{search_results}")

    return func.HttpResponse(json.dumps(search_results), mimetype="application/json", status_code=200)


@app.route(route="search-filter", methods=["GET"])
def search_filter(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get("query")

    if not query:
        return func.HttpResponse("クエリ文字列 'query' に検索したい文字列を指定してください。", status_code=400)

    category = req.params.get("category")

    search_results = vector_search_with_filter(query, category)
    logging.info(f"search_results:{search_results}")

    return func.HttpResponse(json.dumps(search_results), mimetype="application/json", status_code=200)


@app.route(route="semantic-ranking", methods=["GET"])
def semantic_ranking_func(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get("query")

    if not query:
        return func.HttpResponse("クエリ文字列 'query' に検索したい文字列を指定してください。", status_code=400)

    query = req.params.get("query")
    lang = req.params.get("lang")

    search_results = semantic_ranking(query, lang)
    logging.info(f"search_results:{search_results}")

    return func.HttpResponse(json.dumps(search_results), mimetype="application/json", status_code=200)


@app.route(route="semantic-vector", methods=["GET"])
def semantic_vector_func(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get("query")

    if not query:
        return func.HttpResponse("クエリ文字列 'query' に検索したい文字列を指定してください。", status_code=400)

    query = req.params.get("query")
    lang = req.params.get("lang")

    search_results = semantic_ranking_with_vector(query, lang)
    return func.HttpResponse(json.dumps(search_results), mimetype="application/json", status_code=200)
