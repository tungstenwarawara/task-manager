# GitHub上でlifeOS風タスク管理システムを構築する計画

## コンセプト

```
┌─────────────────────────────────────────────────────────────┐
│                      あなた（ユーザー）                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code（インターフェース）              │
│  - 自然言語でタスク追加・更新                                   │
│  - 日記の記録                                                 │
│  - 情報の検索・要約                                            │
│  - 週次レビューの実行                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub（データベース）                       │
│                                                              │
│  task-manager/              knowledge-base/                  │
│  ├── Issues: タスク          ├── journal/: 日記               │
│  ├── Project: ダッシュボード   ├── notes/: 学習ノート            │
│  └── .github/: 自動化        ├── digest/: 自動収集ダイジェスト   │
│                              └── interests.yaml: 興味関心設定  │
│                                                              │
│  GitHub Actions: 毎日の自動情報収集 → ダイジェスト生成            │
└─────────────────────────────────────────────────────────────┘
```

---

## システム構成

### リポジトリ構成

```
tungstenwarawara/
│
├── task-manager/                    # タスク管理リポジトリ
│   ├── .github/
│   │   ├── workflows/
│   │   │   └── daily-digest.yml     # 毎日の情報収集ワークフロー
│   │   └── ISSUE_TEMPLATE/
│   │       ├── task.yml
│   │       └── routine.yml
│   ├── scripts/
│   │   └── collect-news.py          # 情報収集スクリプト
│   └── README.md
│
├── knowledge-base/                  # 知識ベースリポジトリ
│   ├── journal/                     # 日記
│   │   └── 2026/
│   │       └── 02/
│   │           └── 01.md
│   ├── notes/                       # 学習ノート・メモ
│   │   └── topics/
│   ├── digest/                      # 自動収集ダイジェスト
│   │   └── 2026/
│   │       └── 02/
│   │           └── 01.md
│   ├── resources/                   # リソース・リンク集
│   └── interests.yaml               # 興味関心の設定ファイル
│
└── [User-level Project]
    └── Life Dashboard               # 両リポジトリを統合
```

### GitHub Project設定

**Project: Life Dashboard**（ユーザーレベルで作成）

| カスタムフィールド | タイプ | 選択肢 |
|------------------|--------|--------|
| Status | 単一選択 | Inbox / Today / This Week / Scheduled / Done / Archived |
| Pillar | 単一選択 | Work / Health / Learning / Relationships / Finance / Personal |
| Priority | 単一選択 | High / Medium / Low |
| Energy | 単一選択 | High Focus / Low Focus / Routine |
| Due Date | 日付 | - |
| Recurrence | 単一選択 | Daily / Weekly / Monthly / None |

**ビュー構成:**
- Today（カンバン）: 今日のタスク
- This Week（テーブル）: 週次計画
- By Pillar（テーブル）: 領域別
- Routines（テーブル）: 定期タスク一覧
- Roadmap（ロードマップ）: 長期計画

---

## Claude Code連携

### 想定される操作例

```bash
# Claude Codeを起動して自然言語で操作
claude

> 今日のタスクを見せて
> 「企画書を作成する」をタスクに追加、優先度高、明日まで
> 今日の日記を書きたい
> 今週の振り返りをしよう
> 最近のAI関連のダイジェストを見せて
> 「毎週月曜に週次レビュー」を定期タスクに追加
```

### Claude Codeカスタムコマンド（.claude/commands/）

```
task-manager/.claude/commands/
├── add-task.md      # タスク追加
├── daily-review.md  # 日次レビュー
├── weekly-review.md # 週次レビュー
└── journal.md       # 日記記入
```

---

## 自動情報収集システム

### 興味関心の設定（interests.yaml）

```yaml
# knowledge-base/interests.yaml
topics:
  - name: AI/機械学習
    keywords:
      - LLM
      - Claude
      - GPT
      - 機械学習
      - deep learning
    sources:
      - arxiv
      - hacker_news
      - techcrunch
      - reddit
      - youtube
      - x_twitter
    priority: high

  - name: プログラミング
    keywords:
      - Python
      - TypeScript
      - Rust
    sources:
      - hacker_news
      - reddit
      - youtube
    priority: medium

  - name: ビジネス/スタートアップ
    keywords:
      - startup
      - VC
      - 資金調達
    sources:
      - techcrunch
      - hacker_news
      - reddit
      - x_twitter
    priority: medium

sources:
  arxiv:
    type: api
    url: https://export.arxiv.org/api/query

  hacker_news:
    type: api
    url: https://hacker-news.firebaseio.com/v0

  techcrunch:
    type: rss
    url: https://techcrunch.com/feed/

  reddit:
    type: api
    url: https://www.reddit.com/r/{subreddit}/.json
    subreddits:
      - MachineLearning
      - programming
      - technology
      - startups

  youtube:
    type: api
    url: https://www.googleapis.com/youtube/v3
    note: YouTube Data API v3を使用（API Key必要）
    search_queries:
      - AI tutorial
      - programming
      - tech news

  x_twitter:
    type: api
    note: |
      X API は制限が厳しいため、代替手段を検討:
      1. Nitter (非公式フロントエンド) のRSSフィード
      2. 特定リストのRSS化サービス
      3. X API Basic プラン ($100/月) を契約
    alternatives:
      - nitter_rss: https://nitter.net/{username}/rss
```

### GitHub Actions ワークフロー

```yaml
# .github/workflows/daily-digest.yml
name: Daily Digest

on:
  schedule:
    - cron: '0 6 * * *'  # 毎日朝6時（UTC）
  workflow_dispatch:      # 手動実行も可能

jobs:
  collect-and-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fetch news from sources
        run: python scripts/collect-news.py

      - name: Generate digest with Claude API
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/generate-digest.py

      - name: Commit digest to knowledge-base
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add digest/
          git commit -m "Add daily digest for $(date +%Y-%m-%d)"
          git push
```

### ダイジェスト出力例

```markdown
# Daily Digest - 2026-02-01

## AI/機械学習 (5件)

### Claude 4.5 Opusがリリース
Anthropicが最新モデルを発表...
[続きを読む](https://...)

### 新しい推論手法の論文
arXivに投稿された新しいアプローチ...
[続きを読む](https://arxiv.org/...)

## プログラミング (3件)
...

---
*このダイジェストは自動生成されました*
```

---

## 日記システム

### 日記テンプレート

```markdown
# 2026-02-01 (土)

## 今日やったこと
-

## 学んだこと
-

## 明日やること
-

## 気づき・感想

## 気分 (1-5):

---
*Created: 2026-02-01 22:00*
```

### Claude Codeでの日記記入フロー

```
> 日記を書きたい

Claude: 今日の日記を始めましょう。まず、今日やったことを教えてください。

> プロジェクトの企画書を完成させた。あとミーティングが2つあった

Claude: 素晴らしいですね。何か学んだことや気づきはありましたか？

> ミーティングで新しいツールを知った。明日試してみたい

Claude: 日記を作成しました。他に追加したいことはありますか？
```

---

## 実装フェーズ

### Phase 1: 基盤構築 (Week 1)
1. task-manager リポジトリのセットアップ
   - ラベル体系の設定
   - Issue テンプレートの作成
2. knowledge-base リポジトリの作成
   - ディレクトリ構造の作成
   - 日記テンプレートの作成
3. GitHub Project (Life Dashboard) の作成
   - カスタムフィールドの設定
   - ビューの作成

### Phase 2: Claude Code連携 (Week 2)
1. カスタムスラッシュコマンドの作成
   - タスク追加コマンド
   - 日記記入コマンド
   - レビューコマンド
2. gh CLI を使った操作スクリプト

### Phase 3: 自動情報収集 (Week 3)
1. interests.yaml の作成と設定
2. 情報収集スクリプトの実装
   - RSS/API からのデータ取得
   - Claude API でのフィルタリング・要約
3. GitHub Actions ワークフローの設定
4. knowledge-base への自動コミット

### Phase 4: 定期タスク・レビュー (Week 4)
1. 定期タスク管理の仕組み
2. 週次レビューテンプレート
3. 月次レビューテンプレート

---

## 決定事項

| 項目 | 決定 |
|------|------|
| 情報収集ソース | Hacker News, arXiv, TechCrunch, Reddit, YouTube, X |
| ダイジェスト頻度 | 毎日 |
| knowledge-base | private リポジトリ |
| 領域（Pillar） | Work / Health / Learning / Relationships / Finance / Personal |

## 必要なAPIキー・認証情報

GitHub Secrets に以下を設定する必要があります：

| Secret名 | 用途 | 取得方法 |
|----------|------|----------|
| `ANTHROPIC_API_KEY` | Claude APIでダイジェスト生成 | [Anthropic Console](https://console.anthropic.com/) |
| `YOUTUBE_API_KEY` | YouTube Data API | [Google Cloud Console](https://console.cloud.google.com/) |
| `X_BEARER_TOKEN` | X API (オプション) | [X Developer Portal](https://developer.twitter.com/) |

**注意**: X API は Basic プランで $100/月 かかるため、代替として Nitter RSS を使用することも可能です。

---

## 参考リンク

- [GitHubで人生を管理する（Zenn）](https://zenn.dev/hand_dot/articles/85c9640b7dcc66)
- [GitHub Projectsで日常のタスク管理を行う](https://zenn.dev/t4t5u0/articles/f3aeb3895fd1fb)
- [GitHub CLI ドキュメント](https://cli.github.com/manual/)
- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
