# Strage - Table samples (Python)

## デバッグ実行の準備

Azure Functions のサンプルと、素の python のサンプルがあります。デバッグ実行にあたってそれぞれで環境変数をセットする準備がことなります。


## Azure Functions のサンプル: local.settings.json の追加

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

## 素の python のサンプル: .env の追加

素の python のサンプルの場合は、`python-dotenv` を使用しているため、実行するファイルと同じパスに .env ファイルの追加が必要です。中身は以下です。

```
AZURE_STORAGE_CONNECTION_STRING=<ADLS Gen2 の接続文字列>
```


## Python x Table の参考ドキュメント

ここに Getting started な説明とサンプルコードがある。Retry Policy configuration とかも書かれてる

- [Azure Tables client library for Python | Microsoft Docs](https://docs.microsoft.com/en-us/python/api/overview/azure/data-tables-readme?view=azure-python)


SDK の repo で。`samples` の中で基本的なサンプルは見つけれる:

- [azure-sdk-for-python: azure-data-tables - GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/tables/azure-data-tables)

  
