# GitBucket Mock

GitBucket API統合のための包括的な開発ツールキット。モックサーバー実装と実際のGitBucket Docker環境の両方を提供します。

## 🎯 背景

このプロジェクトは、Model Context Protocol（MCP）を通じてAIアシスタント向けのGitBucket統合を提供する[GitBucket MCP Server](https://github.com/moritalous/gitbucket-mcp)の開発をサポートするために作成されました。

### 開発の動機

GitBucketのMCPサーバーを効率的に開発するため、FastMCPの機能を活用することを決定しました。FastMCPには、OpenAPIスキーマを用意するだけでMCPサーバーを構築する機能が備わっているため、GitBucketのモックをFastAPIで構築してOpenAPIスキーマを生成することで、GitBucketのMCPサーバーが作成できると考えました。

## 🔨 開発プロセス

このモックサーバーの開発は、Amazon Q Developer CLIをコーディングアシスタントとして活用し、段階的なアプローチで進められました。

### 開発手順

1. **GitBucketソースコード調査**
   - GitBucketのソースコードを調査し、API提供されている部分を一覧化
   - URLパスに `/api/v3` が含まれることを手がかりに、APIエンドポイントを特定

2. **APIドキュメント化**
   - 特定したAPIの一覧をMarkdownに出力し、ドキュメント化を実施
   - 成果物は `docs/` ディレクトリに格納
   - TODOリストで進捗管理を行うことで、APIの漏れを防止

3. **データモデル生成**
   - ドキュメント化されたAPIを基に、リクエストとレスポンスの型をPydantic v2形式で生成
   - 成果物は `models/` ディレクトリに格納
   - こちらもTODOリスト管理により作業の完全性を確保

4. **FastAPIルーター実装**
   - 生成されたモデルを基に、FastAPIのルーターを実装
   - 固定値を返却するシンプルな実装により、スキーマ生成に特化

### 開発における工夫

Amazon Q Developerに以下のような内容を指示し、コード生成の品質を向上させました。

- **シンプルな実装**: モックサーバーの目的はOpenAPIスキーマ生成であるため、複雑なロジックは避け、固定値を返却する実装に徹底
- **並行作業対応**: 複数の開発者が同時に作業しても競合が起きないよう、モジュール分割を意識した設計
- **TODOリスト管理**: 作業漏れを防ぐため、Amazon Q Developerに「TODOリストで進捗管理をしながら作業を進めて」と明示的に指示
- **ドキュメント形式の改善**: 当初はリクエストボディがサンプルJSONで生成されていたが、後続処理で不確定なコードが生成されたため、Markdownの表形式での出力に変更

### 技術的な選択

- **プロジェクト管理**: uvのプロジェクト初期化や外部ライブラリーの導入は手作業で実施（生成AIによる予期しないpip実行を回避）
- **FastAPI基盤**: main.pyは公式ドキュメントの最もシンプルな実装を手動で作成
- **段階的開発**: ドキュメント → モデル → ルーターの順序で段階的に開発を進行

### 開発環境の進化

開発期間中にAmazon Q Developerが更新され、Claude 3.5 SonnetからClaude Sonnet 4が使用可能になりました。指示の出し方が洗練されたこともあり、後半の作業では非常にスムーズに開発を進めることができました。

## 🚀 機能

- **モックAPIサーバー**: 開発・テスト用のFastAPIベースGitBucket APIモック実装
- **実際のGitBucket環境**: 実際のGitBucketサーバーを実行するためのDocker設定
- **包括的なAPIドキュメント**: すべてのGitBucketエンドポイントの詳細なAPI仕様

## 📁 プロジェクト構成

```
gitbucket-mock/
├── mock/                   # FastAPIベースのモックサーバー
│   ├── main.py            # メインアプリケーションエントリーポイント
│   ├── routers/           # APIルート実装
│   ├── models/            # Pydanticデータモデル
│   ├── data/              # モックデータプロバイダー
│   └── auth.py            # 認証処理
├── docker/                # GitBucket Docker環境
│   ├── Dockerfile         # GitBucketコンテナ定義
│   └── docker-compose.yml # サービスオーケストレーション
├── docs/                  # APIドキュメント
│   ├── Root.md           # ルートAPIエンドポイント
│   ├── Repositories.md   # リポジトリ管理
│   ├── Issues.md         # 課題追跡
│   ├── PullRequests.md   # プルリクエスト管理
│   └── ...               # その他のAPI仕様
└── README.md             # このファイル
```

## 🏃‍♂️ クイックスタート

### オプション1: モックサーバー（開発推奨）

モックサーバーは完全なGitBucketインストールを必要とせず、即座にAPIレスポンスを提供します。

```bash
# mockディレクトリに移動
cd mock

# 依存関係をインストール（uvを使用）
uv sync

# モックサーバーを起動
uv run python main.py
```

モックサーバーは `http://localhost:8000` で利用可能になります

- **API ベースURL**: `http://localhost:8000/api/v3`
- **インタラクティブドキュメント**: `http://localhost:8000/docs`
- **OpenAPI仕様**: `http://localhost:8000/openapi.json`

### オプション2: 実際のGitBucketサーバー

実際のGitBucket機能でテストする場合：

```bash
# dockerディレクトリに移動
cd docker

# GitBucketサーバーを起動
docker-compose up -d
```

GitBucketは `http://localhost:8080` で利用可能になります

- **Webインターフェース**: `http://localhost:8080`
- **SSH Git アクセス**: `localhost:29418`
- **デフォルト認証情報**: `root` / `root`

## 🔧 使用例

### モックAPIの使用

```bash
# APIルート情報を取得
curl http://localhost:8000/api/v3

# リポジトリ一覧を取得
curl http://localhost:8000/api/v3/repos

# リポジトリ情報を取得
curl http://localhost:8000/api/v3/repos/owner/repo

# 課題一覧を取得
curl http://localhost:8000/api/v3/repos/owner/repo/issues

# 課題を作成
curl -X POST http://localhost:8000/api/v3/repos/owner/repo/issues \
  -H "Content-Type: application/json" \
  -d '{"title": "テスト課題", "body": "これはテスト課題です"}'
```

### 認証

モックサーバーは基本認証のシミュレーションをサポートしています：

```bash
# 基本認証を使用
curl -u username:password http://localhost:8000/api/v3/user

# トークンを使用（ヘッダー）
curl -H "Authorization: token your-token" http://localhost:8000/api/v3/user
```

## 📚 APIドキュメント

詳細なAPI仕様は `docs/` ディレクトリで確認できます：

- **[Root API](docs/Root.md)** - 基本API情報
- **[Repositories](docs/Repositories.md)** - リポジトリ管理
- **[Issues](docs/Issues.md)** - 課題追跡
- **[Pull Requests](docs/PullRequests.md)** - プルリクエスト管理
- **[Users](docs/Users.md)** - ユーザー管理
- **[Organizations](docs/Organizations.md)** - 組織管理
- **[Branches](docs/Branches.md)** - ブランチ操作
- **[Commits](docs/Commits.md)** - コミット情報
- **[Contents](docs/Contents.md)** - ファイルコンテンツ操作
- **[Labels](docs/Labels.md)** - 課題/PRラベル
- **[Milestones](docs/Milestones.md)** - プロジェクトマイルストーン
- **[Releases](docs/Releases.md)** - リリース管理
- **[Tags](docs/Tags.md)** - Gitタグ
- **[Webhooks](docs/Webhooks.md)** - Webhook管理
- **[Collaborators](docs/Collaborators.md)** - リポジトリコラボレーター
- **[Git References](docs/GitRefs.md)** - Git参照操作

## 🛠️ 開発

### モックサーバー開発

```bash
cd mock

# 開発用依存関係をインストール
uv sync --group dev

# 自動リロードで実行
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# コードフォーマット
uv run ruff format .

# リンティング
uv run ruff check .

# 型チェック
uv run pyright
```

### 要件

- **Python**: 3.11+
- **依存関係**: FastAPI, Uvicorn
- **開発ツール**: Ruff, Pyright

### Docker開発

```bash
cd docker

# カスタムイメージをビルド
docker build -t gitbucket-custom .

# カスタム設定で実行
docker-compose up --build
```

## 📄 ライセンス

このプロジェクトはApache License 2.0の下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🔗 関連リンク

- [GitBucket公式リポジトリ](https://github.com/gitbucket/gitbucket)
- [GitBucket APIドキュメント](https://github.com/gitbucket/gitbucket/wiki/API-WebHook)
- [FastAPIドキュメント](https://fastapi.tiangolo.com/)

---

**注意**: これは開発目的のモック実装です。本番環境では公式のGitBucketサーバーをご使用ください。