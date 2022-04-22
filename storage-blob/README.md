# Blob 操作 (Python)

## local.settings.json

デバッグ実行するには、以下の local.setting.json を追加し `AZURE_STORAGE_CONNECTION_STRING` に storage account の接続文字列をセットする必要があります。

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "TMP": "./Download"
    "AZURE_STORAGE_CONNECTION_STRING": "",
  }
}
```



## Python x Blob の参考ドキュメント

基本的なサンプルコードはここをみるのがベター。

- [User Guide (Azure Storage Blobs client library for Python) | Microsoft Docs](https://docs.microsoft.com/ja-JP/azure/developer/python/sdk/storage/storage-blob-readme)

- [azure-storage-blob Package reference](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/?view=azure-python)


## 非同期を利用する際は

- `aiohttp` のインストール
- import は `azure.storage.blob.aio` に変更
- メソッドの定義に async つけて、あとは良しなに非同期メソッドを呼ぶ



## Functions 全般の参考ドキュメント

最初に見るドキュメント:

- [Azure Functions の Python 開発者向けガイド](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python)


Tips:

- [Azure Functions で Python アプリのスループット パフォーマンスを向上させる](https://docs.microsoft.com/ja-jp/azure/azure-functions/python-scale-performance-reference)
- [Azure Functions での Python エラーのトラブルシューティング](https://docs.microsoft.com/ja-jp/azure/azure-functions/recover-python-functions?tabs=vscode)
- [Azure Functions で Python アプリのメモリ使用量をプロファイルする](https://docs.microsoft.com/ja-jp/azure/azure-functions/python-memory-profiler-reference)


