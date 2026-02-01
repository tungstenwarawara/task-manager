# Knowledge Base

知識ベース・日記・自動収集ダイジェストを管理するリポジトリ。

## ディレクトリ構造

```
knowledge-base/
├── journal/          # 日記
│   └── 2026/
│       └── 02/
│           └── 01.md
├── notes/            # 学習ノート・メモ
│   └── topics/
├── digest/           # 自動収集ダイジェスト
│   └── 2026/
│       └── 02/
│           └── 01.md
├── resources/        # リソース・リンク集
├── interests.yaml    # 興味関心の設定
└── README.md
```

## 日記の書き方

### Claude Code を使う場合

```bash
claude

> 今日の日記を書きたい
```

### 手動で作成する場合

1. `journal/YYYY/MM/` ディレクトリを作成
2. `DD.md` ファイルを作成
3. テンプレートに従って記入

## 自動ダイジェスト

毎日 UTC 6:00 に GitHub Actions が以下を実行:

1. `interests.yaml` に基づいて情報を収集
2. Claude API で要約・フィルタリング
3. `digest/YYYY/MM/DD.md` として保存

### 設定変更

`interests.yaml` を編集して:

- トピックの追加・削除
- キーワードの変更
- ソースの有効化・無効化
- 優先度の調整

## 関連リポジトリ

- [task-manager](https://github.com/tungstenwarawara/task-manager) - タスク管理
