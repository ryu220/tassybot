# Dify Discord Bot

DifyのチャットボットをDiscordに接続し、24時間稼働するDiscord botです。

## 🚀 特徴

- **Dify統合**: DifyのAIチャットボットとシームレスに連携
- **24時間稼働**: 無料のクラウドサービスで常時稼働
- **簡単設定**: 環境変数の設定だけで動作
- **メンション対応**: ボットをメンションして質問可能
- **DM対応**: ダイレクトメッセージでの質問も可能
- **コマンド機能**: 基本的なボット管理コマンドを搭載

## 📋 必要な準備

- Difyでチャットボットが作成済み
- Discordアカウント
- GitHubアカウント（デプロイ用）

## 🛠️ セットアップ

詳細なセットアップ手順は [setup_guide.md](setup_guide.md) を参照してください。

### クイックスタート

1. **リポジトリのクローン**
```bash
git clone [this-repository-url]
cd dify-discord-bot
```

2. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

3. **環境変数の設定**
```bash
cp .env.example .env
# .envファイルを編集してトークンとAPIキーを設定
```

4. **ボットの起動**
```bash
python dify_discord_bot.py
```

## 📁 ファイル構成

```
├── dify_discord_bot.py    # メインのボットコード
├── requirements.txt       # 必要なPythonパッケージ
├── .env.example          # 環境変数の例
├── Dockerfile            # Docker設定
├── docker-compose.yml    # Docker Compose設定
├── test_bot.py           # テスト用スクリプト
├── setup_guide.md        # 詳細セットアップガイド
├── deployment_comparison.md # デプロイ方法比較
└── README.md             # このファイル
```

## 🎯 使用方法

### Discord内での操作

1. **メンション機能**
   ```
   @ボット名 こんにちは、調子はどう？
   ```

2. **ダイレクトメッセージ**
   - ボットにDMを送信するだけで応答

3. **コマンド機能**
   - `!ping` - ボットの応答確認
   - `!status` - ボットの状態確認
   - `!help_dify` - ヘルプメッセージ

## 🌐 デプロイオプション

### 無料オプション（推奨）
- **Koyeb**: 完全無料で24時間稼働
- **Render**: 無料プラン（スリープあり）

### 有料オプション
- **VPS**: 月額$3-5で高い安定性
- **AWS EC2**: 1年間無料枠あり

詳細は [deployment_comparison.md](deployment_comparison.md) を参照。

## 🔧 カスタマイズ

### 機能の追加
- `dify_discord_bot.py`を編集して新しいコマンドや機能を追加
- Dify APIの他のエンドポイントを活用

### 設定の変更
- 環境変数でAPIエンドポイントやその他の設定を変更可能

## 📊 監視とメンテナンス

- ログの確認方法
- エラー対応
- パフォーマンス最適化

詳細は [setup_guide.md](setup_guide.md) の「運用とメンテナンス」セクションを参照。

## ⚠️ 注意事項

- APIキーやトークンは絶対に公開しないでください
- `.env`ファイルはGitにコミットしないでください
- 定期的にAPIキーを更新してください

## 📞 サポート

問題が発生した場合は、以下のリソースを参照してください：
- [Discord.py ドキュメント](https://discordpy.readthedocs.io/)
- [Dify ドキュメント](https://docs.dify.ai/)

## 📄 ライセンス

MIT License

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します。

