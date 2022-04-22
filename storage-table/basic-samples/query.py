import os
from uuid import uuid4
from dotenv import find_dotenv, load_dotenv
from azure.data.tables import TableClient, UpdateMode

TABLE_NAME = "SampleTable"

def main():
  print("Run query.py")
  load_dotenv(find_dotenv())

  # TableClient: https://docs.microsoft.com/en-us/python/api/azure-data-tables/azure.data.tables.tableclient?view=azure-python
  with TableClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"], TABLE_NAME) as table_client:

    entity = {
      "PartitionKey": "PK1",
      "RowKey": str(uuid4()),
      "Name":"yokohama",
      "Game": "Fortnite"
    }

    # ✅ Insert: Key (PartitionKey + RowKey) が被ると 409。戻り値の型は "Dict"
    inserted_result = table_client.create_entity(entity)

    # ✅ Get Single Entity: PartitionKey + RowKey を指定して entity を取得
    got_result = table_client.get_entity(entity["PartitionKey"], entity["RowKey"])
    # print(f"get_entity() result: {json.dumps(got_result)}")
    print(f"get_entity() result: {got_result}")

    # ✅ Update entity
    # UpdateMode.REPLACE: entity 全体を置き換える。
    # UpdateMode.MERGE: 指定した property のみ置き換える (存在しない property でも OK)。
    got_result["Nothing"] = "Fortnite Season 4"
    table_client.update_entity(mode=UpdateMode.REPLACE, entity=got_result)

    # PropX を追加して entity を更新
    entity_to_merge = {
      "PartitionKey": got_result["PartitionKey"],
      "RowKey": got_result["RowKey"],
      "PropX":"Hello",
    }
    table_client.update_entity(mode=UpdateMode.MERGE, entity=entity_to_merge)

    # ✅ Upsert entity
    # メソッド名 Upsert() を使うだけで、基本的に Update と同様
    # https://github.com/Azure/azure-sdk-for-python/blob/azure-data-tables_12.3.0/sdk/tables/azure-data-tables/samples/sample_update_upsert_merge_entities.py#L155-L163
    

    # ✅ Delete entity
    print(f'Delete entity (PK {got_result["PartitionKey"]} / RK {got_result["RowKey"]})')
    
    table_client.delete_entity(got_result["PartitionKey"], got_result["RowKey"])


    print("Done query.py")


if __name__ == "__main__":
  main()