# Strage - Table samples (Python)

## local.settings.json

デバッグ実行するには、以下の local.setting.json を追加し `AZURE_STORAGE_CONNECTION_STRING` に storage account の接続文字列をセットする必要があります。

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_STORAGE_CONNECTION_STRING": "",
  }
}
```

## Python x Table の参考ドキュメント

ここに Getting started な説明とサンプルコードがある。Retry Policy configuration とかも書かれてる

- [Azure Tables client library for Python | Microsoft Docs](https://docs.microsoft.com/en-us/python/api/overview/azure/data-tables-readme?view=azure-python)


SDK の repo で。`samples` の中で基本的なサンプルは見つけれる:

- [azure-sdk-for-python: azure-data-tables - GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/tables/azure-data-tables)

  
