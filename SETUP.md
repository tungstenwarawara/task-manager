# セットアップガイド

Life Task Manager を利用するための詳細なセットアップ手順です。

## 前提条件

- GitHub アカウント
- gh CLI ([インストール](https://cli.github.com/))
- Git

## Step 1: gh CLI のセットアップ

```bash
# インストール
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
winget install GitHub.cli

# 認証
gh auth login
```

## Step 2: ラベルの設定

```bash
cd task-manager
./scripts/setup-labels.sh
```

作成されるラベル:
- **Pillar**: work, health, learning, relations, finance, personal
- **Type**: task, routine, project, idea
- **Priority**: high, medium, low
- **Status**: today, this-week, blocked

## Step 3: knowledge-base リポジトリの作成

### GitHub で新規リポジトリを作成

1. https://github.com/new にアクセス
2. Repository name: `knowledge-base`
3. Visibility: **Private** (推奨)
4. 「Create repository」をクリック

### 初期化スクリプトを実行

```bash
./scripts/init-knowledge-base.sh
```

または手動で:

```bash
# ホームディレクトリに移動
cd ~

# クローン
git clone https://github.com/YOUR_USERNAME/knowledge-base.git
cd knowledge-base

# ディレクトリ作成
mkdir -p journal notes/topics digest resources

# テンプレートをコピー
cp ~/task-manager/templates/knowledge-base/* .
cp ~/task-manager/templates/knowledge-base/journal/* journal/

# コミット & プッシュ
git add -A
git commit -m "Initialize knowledge-base"
git push
```

## Step 4: GitHub Project の作成

1. https://github.com/YOUR_USERNAME?tab=projects にアクセス
2. 「New project」→「Table」を選択
3. プロジェクト名: `Life Dashboard`

### カスタムフィールドを追加

「+ Add field」から以下を追加:

| フィールド | タイプ | 値 |
|-----------|--------|-----|
| Status | Single select | Inbox, Today, This Week, Scheduled, Done, Archived |
| Pillar | Single select | Work, Health, Learning, Relationships, Finance, Personal |
| Priority | Single select | High, Medium, Low |
| Energy | Single select | High Focus, Low Focus, Routine |
| Due Date | Date | - |
| Recurrence | Single select | Daily, Weekly, Monthly, None |

### ビューを作成

1. **Today** (Board view)
   - Filter: Status = Today
   - Group by: Priority

2. **This Week** (Table view)
   - Filter: Status = This Week
   - Sort by: Due Date

3. **By Pillar** (Table view)
   - Group by: Pillar

4. **Routines** (Table view)
   - Filter: Recurrence != None

### ワークフローを設定

Project Settings → Workflows:
- ✅ Item added to project → Set Status to "Inbox"
- ✅ Item closed → Set Status to "Done"

## Step 5: GitHub Secrets の設定

Settings → Secrets and variables → Actions → New repository secret

| Secret | 用途 | 取得方法 |
|--------|------|----------|
| `ANTHROPIC_API_KEY` | 自動ダイジェスト生成 | https://console.anthropic.com/ |
| `YOUTUBE_API_KEY` | YouTube からの情報収集 | https://console.cloud.google.com/ |

## Step 6: 動作確認

```bash
# Claude Code を起動
claude

# テスト
> 今日のタスクを見せて
> テストタスク をタスクに追加
> 日記を書きたい
```

## トラブルシューティング

### gh が認証されていない

```bash
gh auth status
gh auth login
```

### ラベルが見つからない

```bash
./scripts/setup-labels.sh
```

### knowledge-base にアクセスできない

リポジトリが存在し、権限があるか確認:
```bash
gh repo view YOUR_USERNAME/knowledge-base
```

## 完了チェックリスト

- [ ] gh CLI インストール & 認証
- [ ] ラベル設定完了
- [ ] knowledge-base リポジトリ作成
- [ ] GitHub Project 作成
- [ ] カスタムフィールド設定
- [ ] ワークフロー有効化
- [ ] ANTHROPIC_API_KEY 設定
- [ ] Claude Code で動作確認
