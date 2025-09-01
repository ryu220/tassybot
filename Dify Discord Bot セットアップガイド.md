# Dify Discord Bot セットアップガイド

## 概要

このガイドでは、DifyのチャットボットをDiscordに接続し、24時間稼働するDiscord botを構築する方法を説明します。

## 前提条件

- Difyでチャットボットが作成済み
- Discordアカウント
- 基本的なコマンドライン操作の知識

## 必要なファイル

プロジェクトには以下のファイルが含まれています：

- `dify_discord_bot.py` - メインのボットコード
- `requirements.txt` - 必要なPythonパッケージ
- `.env.example` - 環境変数の例
- `Dockerfile` - Docker設定
- `docker-compose.yml` - Docker Compose設定
- `test_bot.py` - テスト用スクリプト




## ステップ1: Discord Botの作成

### 1.1 Discord Developer Portalにアクセス

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. Discordアカウントでログイン
3. 右上の「New Application」をクリック

### 1.2 アプリケーションの作成

1. アプリケーション名を入力（例：「Dify Chat Bot」）
2. 「Create」をクリック

### 1.3 Botの設定

1. 左側メニューから「Bot」を選択
2. 「Add Bot」をクリック（既に表示されている場合はスキップ）
3. 「Token」セクションで「Copy」をクリックしてトークンをコピー
   - ⚠️ **重要**: このトークンは秘密情報です。他人と共有しないでください

### 1.4 Bot権限の設定

1. 「OAuth2」→「URL Generator」を選択
2. 「Scopes」で「bot」にチェック
3. 「Bot Permissions」で以下にチェック：
   - Send Messages
   - Read Message History
   - Use Slash Commands
   - Mention Everyone
4. 生成されたURLをコピーしてブラウザで開く
5. Botを追加したいサーバーを選択して「認証」

### 1.5 Bot設定の調整

1. 「Bot」設定に戻る
2. 「Message Content Intent」を有効にする
3. 「Save Changes」をクリック


## ステップ2: Dify APIキーの取得

### 2.1 Difyにログイン

1. [Dify](https://dify.ai/)にアクセス
2. アカウントでログイン

### 2.2 アプリの選択

1. 使用したいチャットボットアプリを選択
2. アプリの詳細画面に移動

### 2.3 APIキーの取得

1. 上部ナビゲーションの「APIアクセス」タブをクリック
2. 「APIキー」セクションでキーを確認
3. キーが表示されていない場合は「作成」をクリック
4. APIキーをコピー
   - ⚠️ **重要**: このキーも秘密情報です

### 2.4 API設定の確認

1. 「API設定」で以下を確認：
   - エンドポイント: `https://api.dify.ai/v1`
   - 認証方式: Bearer Token
2. 必要に応じて設定を調整


## ステップ3: ローカル環境の設定

### 3.1 プロジェクトファイルの準備

1. すべてのプロジェクトファイルを同じディレクトリに配置
2. ターミナル/コマンドプロンプトでそのディレクトリに移動

### 3.2 Python環境の確認

```bash
# Pythonのバージョン確認（3.8以上が必要）
python --version
# または
python3 --version
```

### 3.3 必要パッケージのインストール

```bash
# 必要なパッケージをインストール
pip install -r requirements.txt
# または
pip3 install -r requirements.txt
```

### 3.4 環境変数の設定

1. `.env.example`をコピーして`.env`ファイルを作成：
```bash
cp .env.example .env
```

2. `.env`ファイルを編集して実際の値を設定：
```env
DISCORD_TOKEN=your_actual_discord_bot_token_here
DIFY_API_KEY=your_actual_dify_api_key_here
DIFY_API_BASE=https://api.dify.ai/v1
```

### 3.5 テストの実行

```bash
# ボットコードのテスト
python test_bot.py
```

すべてのテストが成功すれば、設定は完了です。


## ステップ4: ローカルでの実行とテスト

### 4.1 ボットの起動

```bash
# ボットを起動
python dify_discord_bot.py
```

成功すると以下のようなメッセージが表示されます：
```
🚀 ボットを起動中...
[ボット名] has connected to Discord!
Bot is in [サーバー数] guilds
```

### 4.2 動作テスト

1. **メンション機能のテスト**
   - Discordサーバーで `@ボット名 こんにちは` と入力
   - ボットが応答することを確認

2. **DM機能のテスト**
   - ボットにダイレクトメッセージを送信
   - ボットが応答することを確認

3. **コマンド機能のテスト**
   - `!ping` - レイテンシの確認
   - `!status` - ボットの状態確認
   - `!help_dify` - ヘルプメッセージの表示

### 4.3 トラブルシューティング

**ボットが応答しない場合:**
1. Discord Developer Portalで「Message Content Intent」が有効になっているか確認
2. ボットがサーバーに正しく招待されているか確認
3. 環境変数が正しく設定されているか確認

**Dify APIエラーが発生する場合:**
1. Dify APIキーが正しいか確認
2. Difyアプリが公開されているか確認
3. API制限に達していないか確認


## ステップ5: 24時間稼働のためのデプロイ

### 5.1 Koyebでのデプロイ（推奨・無料）

#### 5.1.1 GitHubリポジトリの準備

1. GitHubで新しいリポジトリを作成
2. プロジェクトファイルをアップロード（`.env`ファイルは除く）

#### 5.1.2 Koyebアカウントの作成

1. [Koyeb](https://www.koyeb.com/)にアクセス
2. GitHubアカウントでサインアップ

#### 5.1.3 アプリのデプロイ

1. Koyebダッシュボードで「Create App」をクリック
2. 「Deploy from GitHub」を選択
3. GitHubリポジトリを選択
4. 以下の設定を行う：
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python dify_discord_bot.py`
   - **Port**: 設定不要（Webサービスではないため）

#### 5.1.4 環境変数の設定

1. 「Environment Variables」セクションで以下を追加：
   - `DISCORD_TOKEN`: Discord Botトークン
   - `DIFY_API_KEY`: Dify APIキー
   - `DIFY_API_BASE`: `https://api.dify.ai/v1`

#### 5.1.5 デプロイの実行

1. 「Deploy」をクリック
2. デプロイが完了するまで待機（数分）
3. ログでボットが正常に起動していることを確認

### 5.2 VPSでのデプロイ（有料・高安定性）

#### 5.2.1 VPSの準備

1. VPSプロバイダー（DigitalOcean、Linode、Vultrなど）でサーバーを作成
2. Ubuntu 20.04以上を選択
3. SSHでサーバーに接続

#### 5.2.2 環境のセットアップ

```bash
# システムの更新
sudo apt update && sudo apt upgrade -y

# Pythonとpipのインストール
sudo apt install python3 python3-pip git -y

# プロジェクトのクローン
git clone [your-github-repo-url]
cd [your-repo-name]

# 依存関係のインストール
pip3 install -r requirements.txt
```

#### 5.2.3 環境変数の設定

```bash
# .envファイルの作成
cp .env.example .env
nano .env
```

#### 5.2.4 systemdサービスの作成

```bash
# サービスファイルの作成
sudo nano /etc/systemd/system/dify-discord-bot.service
```

以下の内容を入力：
```ini
[Unit]
Description=Dify Discord Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/[your-repo-name]
ExecStart=/usr/bin/python3 dify_discord_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 5.2.5 サービスの有効化と起動

```bash
# サービスの有効化
sudo systemctl enable dify-discord-bot.service

# サービスの起動
sudo systemctl start dify-discord-bot.service

# 状態の確認
sudo systemctl status dify-discord-bot.service
```


## ステップ6: 運用とメンテナンス

### 6.1 ログの確認

#### Koyebの場合
1. Koyebダッシュボードでアプリを選択
2. 「Logs」タブでリアルタイムログを確認

#### VPSの場合
```bash
# サービスログの確認
sudo journalctl -u dify-discord-bot.service -f

# 最新100行のログを表示
sudo journalctl -u dify-discord-bot.service -n 100
```

### 6.2 ボットの更新

#### Koyebの場合
1. GitHubリポジトリにコードをプッシュ
2. Koyebが自動的に再デプロイ

#### VPSの場合
```bash
# コードの更新
git pull origin main

# サービスの再起動
sudo systemctl restart dify-discord-bot.service
```

### 6.3 監視とアラート

#### 基本的な監視項目
- ボットのオンライン状態
- エラーログの発生
- API使用量
- サーバーリソース使用量

#### 推奨監視ツール
- **Uptime Robot**: 無料でWebサイト/サービスの稼働監視
- **Discord Webhook**: エラー時の通知
- **Grafana + Prometheus**: 詳細なメトリクス監視（上級者向け）

### 6.4 セキュリティ対策

1. **APIキーの定期的な更新**
   - 3-6ヶ月ごとにAPIキーを更新
   - 古いキーは無効化

2. **アクセス制限**
   - ボットの権限を最小限に設定
   - 不要なサーバーからの削除

3. **ログの監視**
   - 異常なアクセスパターンの検出
   - エラー率の監視

### 6.5 パフォーマンス最適化

1. **レスポンス時間の改善**
   - Dify APIのレスポンス時間を監視
   - 必要に応じてタイムアウト設定を調整

2. **リソース使用量の最適化**
   - メモリ使用量の監視
   - 不要なライブラリの削除

3. **スケーリング**
   - 複数サーバーでの負荷分散（大規模運用時）
   - データベースの導入（会話履歴の保存）


## よくある質問（FAQ）

### Q1: ボットが応答しないのですが？
**A:** 以下を確認してください：
1. Discord Developer Portalで「Message Content Intent」が有効になっているか
2. ボットがサーバーに正しく招待されているか
3. 環境変数（DISCORD_TOKEN、DIFY_API_KEY）が正しく設定されているか
4. Difyアプリが公開状態になっているか

### Q2: Dify APIでエラーが発生します
**A:** 以下を確認してください：
1. Dify APIキーが正しいか
2. APIの使用制限に達していないか
3. Difyアプリが正常に動作しているか
4. ネットワーク接続に問題がないか

### Q3: 無料でどのくらい使用できますか？
**A:** 
- **Koyeb**: 月512MB RAM、100GB帯域幅まで無料
- **Dify**: プランによって異なる（公式サイトで確認）
- **Discord**: Bot自体は無料で使用可能

### Q4: 複数のサーバーで使用できますか？
**A:** はい、同じボットを複数のDiscordサーバーに招待して使用できます。

### Q5: 会話履歴は保存されますか？
**A:** 現在の実装では会話履歴は保存されません。必要に応じてデータベースを追加できます。

## トラブルシューティング

### エラー: "discord.errors.LoginFailure"
**原因**: Discord Botトークンが無効
**解決策**: Discord Developer Portalで正しいトークンを確認し、環境変数を更新

### エラー: "requests.exceptions.HTTPError: 401"
**原因**: Dify APIキーが無効
**解決策**: DifyでAPIキーを確認し、環境変数を更新

### エラー: "discord.errors.Forbidden"
**原因**: ボットに必要な権限がない
**解決策**: Discord Developer Portalでボット権限を確認し、サーバーに再招待

### ボットがオフラインになる
**原因**: ホスティングサービスの制限やエラー
**解決策**: ログを確認し、必要に応じてサービスを再起動

## まとめ

このガイドに従って、DifyのチャットボットをDiscordに接続し、24時間稼働するボットを構築できます。

### 主な特徴
- ✅ メンション機能とDM機能
- ✅ Dify APIとの完全統合
- ✅ 24時間無料稼働（Koyeb使用時）
- ✅ 簡単なデプロイとメンテナンス
- ✅ 拡張可能なアーキテクチャ

### 次のステップ
1. 基本機能の動作確認
2. 必要に応じてカスタマイズ
3. 監視とメンテナンス体制の構築
4. ユーザーフィードバックの収集と改善

### サポート
問題が発生した場合は、以下のリソースを参照してください：
- [Discord.py ドキュメント](https://discordpy.readthedocs.io/)
- [Dify ドキュメント](https://docs.dify.ai/)
- [Koyeb ドキュメント](https://www.koyeb.com/docs)

---

**注意**: APIキーやトークンは絶対に公開しないでください。セキュリティを最優先に運用してください。

