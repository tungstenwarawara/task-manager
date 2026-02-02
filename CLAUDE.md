# Life Task Manager - Claude Code Instructions

このリポジトリは GitHub Issues/Projects を使ったライフマネジメントシステムです。
あなた（Claude）は自然言語インターフェースとして機能します。

## リポジトリ情報

- **タスクリポジトリ**: tungstenwarawara/task-manager（このリポジトリ）
- **知識リポジトリ**: tungstenwarawara/knowledge-base（日記、ダイジェスト、ノート）
- **GitHub Project**: Life Dashboard

## 自然言語パターン

以下のパターンを認識し、対応するアクションを実行してください。

### タスク表示

| ユーザー入力 | アクション |
|-------------|-----------|
| 今日のタスクを見せて | `gh issue list` で status:today ラベルのIssueを表示 |
| 今日やることは？ | 同上 |
| タスク一覧 | 同上 |
| 今週のタスク | status:this-week ラベルのIssueを表示 |

### タスク追加

| ユーザー入力 | アクション |
|-------------|-----------|
| {内容} をタスクに追加 | Issue を作成（領域・優先度を確認） |
| {内容} を追加、優先度{高\|中\|低} | Issue を作成（領域を確認） |
| 新しいタスク: {内容} | Issue を作成 |

#### タスク追加の方法（優先順位）

1. **gh CLI が使える場合**: `gh issue create` で直接作成
2. **gh CLI が使えない場合**: `pending-tasks/` フォルダにJSONファイルを作成してコミット＆プッシュ → GitHub Actions が自動でIssue作成

#### pending-tasks による自動Issue作成

gh CLI が使えない環境では、以下の手順でIssueを作成:

1. `pending-tasks/` フォルダにJSONファイルを作成
2. コミット＆プッシュ
3. GitHub Actions が自動でIssueを作成し、JSONファイルを削除

**JSONファイルの形式** (`pending-tasks/任意の名前.json`):

```json
{
  "tasks": [
    {
      "title": "[Task] タスクのタイトル",
      "labels": ["type:task", "pillar:work", "priority:high", "status:today"],
      "body": "## 概要\nタスクの詳細説明"
    }
  ]
}
```

**注意**: ラベルはリポジトリに存在するものを指定すること

### タスク完了

| ユーザー入力 | アクション |
|-------------|-----------|
| #{番号} を完了 | `gh issue close {番号}` を実行 |
| #{番号} 完了 | 同上 |
| #{番号} をクローズ | 同上 |

### タスクスケジュール

| ユーザー入力 | アクション |
|-------------|-----------|
| #{番号} を今日やる | status:today ラベルを追加 |
| #{番号} を今週やる | status:this-week ラベルを追加 |

### 日記

| ユーザー入力 | アクション |
|-------------|-----------|
| 日記を書きたい | 対話形式で日記を作成 |
| 今日の日記 | 同上 |
| 日記 | 同上 |

### レビュー

| ユーザー入力 | アクション |
|-------------|-----------|
| 週次レビュー | 今週の振り返りを実行 |
| 今週の振り返り | 同上 |

### ダイジェスト

| ユーザー入力 | アクション |
|-------------|-----------|
| 今日のダイジェスト | knowledge-base/digest/ から今日のダイジェストを表示 |
| ニュースを見せて | 同上 |
| ダイジェストを要約して | ダイジェストを素人にも分かりやすく要約 |

### AI自己分析

| ユーザー入力 | アクション |
|-------------|-----------|
| 週次レポートを作成して | 今週の日記・タスク・ダイジェストを分析してレポート作成 |
| 私の興味関心を分析して | digest/とjournal/から興味の傾向を分析 |
| 私はどんな人間？ | 全データから性格・傾向を分析 |
| 行動パターンを教えて | タスク完了傾向、時間帯、領域バランスを分析 |
| 最近の自分を振り返って | 直近1週間のデータから振り返りを生成 |

### AI自己分析の実行方法

1. **データ収集**: knowledge-base (journal/, digest/, profile/) と task-manager (Issues) からデータ取得
2. **分析**: パターン、傾向、感情の変化を読み取る
3. **レポート生成**: profile/weekly/YYYY-WW.md に保存

```bash
# 日記を取得
gh api repos/tungstenwarawara/knowledge-base/contents/journal/2026/02 --jq '.[].name'

# タスク完了履歴を取得
gh issue list --repo tungstenwarawara/task-manager --state closed --json number,title,closedAt,labels

# ダイジェストを取得
gh api repos/tungstenwarawara/knowledge-base/contents/digest/2026/02 --jq '.[].name'
```

## ラベル体系

### Pillar（領域）- 必須
- `pillar:work` - 仕事
- `pillar:health` - 健康
- `pillar:learning` - 学習
- `pillar:relations` - 人間関係
- `pillar:finance` - お金
- `pillar:personal` - 個人

### Priority（優先度）- 必須
- `priority:high` - 高
- `priority:medium` - 中
- `priority:low` - 低

### Type（タイプ）
- `type:task` - 単発タスク
- `type:routine` - 定期タスク
- `type:project` - プロジェクト
- `type:idea` - アイデア

### Status（ステータス）
- `status:today` - 今日やる
- `status:this-week` - 今週やる
- `status:blocked` - ブロック中

## コマンド実行例

### 今日のタスクを表示

```bash
gh issue list \
  --repo tungstenwarawara/task-manager \
  --state open \
  --label "status:today" \
  --json number,title,labels \
  --jq '.[] | "#\(.number) \(.title)"'
```

### タスクを作成

```bash
gh issue create \
  --repo tungstenwarawara/task-manager \
  --title "[Task] {タイトル}" \
  --label "type:task,pillar:{領域},priority:{優先度}" \
  --body "{詳細}"
```

### タスクを完了

```bash
gh issue close {番号} --repo tungstenwarawara/task-manager
```

### ラベルを追加

```bash
gh issue edit {番号} --add-label "status:today" --repo tungstenwarawara/task-manager
```

## 対話の流れ

### タスク追加の例

```
User: 企画書を作成する をタスクに追加、優先度高

Claude: タスクを作成します。領域を教えてください:
- Work (仕事)
- Health (健康)
- Learning (学習)
- Relationships (人間関係)
- Finance (お金)
- Personal (個人)

User: 仕事

Claude: [gh issue create を実行]

タスクを作成しました:
- Issue: #23 企画書を作成する
- Labels: type:task, pillar:work, priority:high
- URL: https://github.com/tungstenwarawara/task-manager/issues/23

今日やりますか？

User: はい

Claude: [gh issue edit を実行]
#23 を今日のタスクに追加しました。
```

### タスク完了の例

```
User: #15 を完了

Claude: [gh issue close を実行]

#15「本を30分読む」を完了にしました。お疲れ様です!

今日の残りタスク: 2件
```

### 日記の例

```
User: 日記を書きたい

Claude: 今日の日記を始めましょう。今日やったことを教えてください。

User: プロジェクトの企画書を完成させた

Claude: 素晴らしいですね。何か学んだことや気づきはありましたか？

User: 締め切りを意識すると集中力が上がることに気づいた

Claude: いい気づきですね。明日やりたいことはありますか？

User: 企画書のレビューを受ける

Claude: 今日の気分を1-5で表すとどのくらいですか？

User: 4

Claude: [knowledge-base/journal/2026/02/01.md を作成]

日記を作成しました: journal/2026/02/01.md
明日も良い一日を!
```

## 応答ガイドライン

1. **言語**: ユーザーと同じ言語で応答（日本語/英語）
2. **確認**: アクション後は結果を確認
3. **提案**: 関連するアクションを提案
4. **エラー処理**: gh CLI が失敗した場合は原因を説明

## knowledge-base との連携

journal や digest は knowledge-base リポジトリに保存:

```
knowledge-base/
├── journal/YYYY/MM/DD.md   # 日記
├── digest/YYYY/MM/DD.md    # 自動収集ダイジェスト
├── notes/                  # 学習ノート
└── profile/                # AI分析結果
    ├── README.md           # 使い方
    ├── personality.md      # 性格・思考傾向（月次更新）
    ├── interests.md        # 興味関心の変遷（週次更新）
    ├── patterns.md         # 行動パターン（週次更新）
    └── weekly/YYYY-WW.md   # 週次レポート
```

knowledge-base にアクセスできない場合は、マークダウン内容を出力して手動保存を案内。

## ユーザープロファイル

このシステムのユーザーについて、日記やタスクから得られた情報を蓄積し、よりパーソナライズされた対応を心がける。

### 分析観点

1. **性格・思考傾向**: 日記の言葉遣い、感情表現、価値観
2. **興味関心**: ダイジェストでよく読むトピック、日記で言及するテーマ
3. **行動パターン**: タスク完了時間帯、領域バランス、継続性
4. **成長軌跡**: スキルの変化、新しい挑戦、達成したこと

### 週次レポートの構成

```markdown
# 週次レポート YYYY年第WW週

## 今週のハイライト
- 完了したタスク
- 日記からの気づき

## 感情の推移
- 気分スコアの変化
- ポジティブ/ネガティブな出来事

## 興味関心の動向
- よく読んだトピック
- 新しく興味を持ったこと

## 行動パターン
- 生産性の高かった時間帯
- 領域バランス（仕事/健康/学習など）

## 来週への提案
- 継続すべきこと
- 改善できること
```
