# Life Task Manager

GitHub + Claude Code を使ったライフマネジメントシステム。

## 概要

```
あなた → Claude Code（自然言語で操作）→ GitHub（データ保存）
```

- **タスク管理**: GitHub Issues + Projects
- **知識ベース**: [knowledge-base](https://github.com/tungstenwarawara/knowledge-base) リポジトリ
- **自動ダイジェスト**: GitHub Actions で毎日情報収集

## クイックセットアップ

```bash
# gh CLI をインストール (まだの場合)
# macOS: brew install gh
# Ubuntu: sudo apt install gh

# 認証
gh auth login

# セットアップスクリプトを実行
chmod +x scripts/setup.sh
./scripts/setup.sh
```

これで以下が自動的に設定されます:
- ラベル（Pillar, Type, Priority, Status）
- knowledge-base リポジトリ
- GitHub Project (Life Dashboard)

## 手動セットアップ

### 1. ラベルの設定

```bash
chmod +x scripts/setup-labels.sh
./scripts/setup-labels.sh
```

### 2. GitHub Project の作成

1. [GitHub Projects](https://github.com/tungstenwarawara?tab=projects) にアクセス
2. 「New project」→「Table」を選択
3. プロジェクト名: `Life Dashboard`

#### カスタムフィールドの追加

| フィールド名 | タイプ | 選択肢 |
|------------|--------|--------|
| Status | Single select | Inbox / Today / This Week / Scheduled / Done / Archived |
| Pillar | Single select | Work / Health / Learning / Relationships / Finance / Personal |
| Priority | Single select | High / Medium / Low |
| Energy | Single select | High Focus / Low Focus / Routine |
| Due Date | Date | - |
| Recurrence | Single select | Daily / Weekly / Monthly / None |

#### ビューの作成

1. **Today** (Board): Status でグループ化、Today のみ表示
2. **This Week** (Table): Due Date でソート
3. **By Pillar** (Table): Pillar でグループ化
4. **Routines** (Table): Recurrence != None でフィルタ
5. **Roadmap** (Roadmap): Due Date を使用

### 3. ワークフロー自動化

Project Settings → Workflows で以下を有効化:
- Item added to project → Set Status to "Inbox"
- Item closed → Set Status to "Done"

### 4. knowledge-base リポジトリの作成

[knowledge-base リポジトリ](https://github.com/tungstenwarawara/knowledge-base) を作成し、以下の構造を設定:

```
knowledge-base/
├── journal/          # 日記
├── notes/            # 学習ノート
├── digest/           # 自動収集ダイジェスト
├── resources/        # リソース・リンク集
└── interests.yaml    # 興味関心の設定
```

### 5. GitHub Secrets の設定

Settings → Secrets and variables → Actions で以下を追加:

| Secret名 | 用途 |
|----------|------|
| `ANTHROPIC_API_KEY` | Claude API |
| `YOUTUBE_API_KEY` | YouTube Data API |
| `X_BEARER_TOKEN` | X API (オプション) |

## 使い方

### Claude Code でタスク操作

```bash
claude

> 今日のタスクを見せて
> 「企画書を作成する」をタスクに追加、優先度高、明日まで
> 今日の日記を書きたい
> 今週の振り返りをしよう
```

### Issue からタスク作成

1. [New Issue](../../issues/new/choose) をクリック
2. テンプレートを選択 (Task / Routine / Idea)
3. フォームに入力して作成

## ラベル一覧

### Pillar（領域）
- `pillar:work` - 仕事
- `pillar:health` - 健康
- `pillar:learning` - 学習
- `pillar:relations` - 人間関係
- `pillar:finance` - お金
- `pillar:personal` - 個人

### Type（タイプ）
- `type:task` - 単発タスク
- `type:project` - プロジェクト
- `type:routine` - 定期タスク
- `type:idea` - アイデア・いつかやる

### Priority（優先度）
- `priority:high` - 高
- `priority:medium` - 中
- `priority:low` - 低

### Status（ステータス）
- `status:today` - 今日やる
- `status:this-week` - 今週やる
- `status:blocked` - ブロック中

## 関連リポジトリ

- [knowledge-base](https://github.com/tungstenwarawara/knowledge-base) - 知識ベース・日記・ダイジェスト
