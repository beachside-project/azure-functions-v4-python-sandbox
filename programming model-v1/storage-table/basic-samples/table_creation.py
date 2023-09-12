import os
from dotenv import find_dotenv, load_dotenv
from azure.data.tables import TableServiceClient

TABLE_NAME = "SampleTable"

def main():
  # このファイルと同じパスに ".env" ファイルを追加して、
  # "AZURE_STORAGE_CONNECTION_STRING" をセットする必要あり。
  load_dotenv(find_dotenv())

  # TableServiceClient Class: https://docs.microsoft.com/en-us/python/api/azure-data-tables/azure.data.tables.tableserviceclient?view=azure-python
  # Samples: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/tables/azure-data-tables/samples/sample_create_client.py
  table_service_client = TableServiceClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"])

  # "create_table()" だけじゃなく "create_table_if_not_exists" もある
  # table_client = table_service_client.create_table("SapleTable1")
  table_client = table_service_client.create_table_if_not_exists(TABLE_NAME)
  print(f"table name: {table_client.table_name}")


if __name__ == "__main__":
  main()