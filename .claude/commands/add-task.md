# Add Task / タスク追加

タスクを GitHub Issue として作成します。

## トリガー

- `{内容} をタスクに追加`
- `{内容} を追加`
- `{内容} を追加、優先度{高|中|低}`
- `新しいタスク: {内容}`
- `タスク作成`

## 必須情報

以下の情報を収集します（提供されていない場合は質問）:

1. **タイトル**: タスクの内容
2. **Pillar（領域）**: work / health / learning / relations / finance / personal
3. **Priority（優先度）**: high / medium / low

## オプション情報

- **Due Date（期限）**: YYYY-MM-DD 形式
- **Description（詳細）**: 追加の説明
- **Today**: 今日やるかどうか

## 入力のパース

| ユーザー入力 | タイトル | 優先度 | 領域 |
|-------------|---------|--------|------|
| 企画書を作成する を追加、優先度高 | 企画書を作成する | high | (質問) |
| 運動30分、健康、低 | 運動30分 | low | health |
| 明日までに請求書確認 | 請求書確認 | (質問) | (質問) |

### 優先度キーワード

| 入力 | 値 |
|------|-----|
| 高、高い、重要、urgent、high | high |
| 中、普通、medium | medium |
| 低、低い、low | low |

### 領域キーワード

| 入力 | 値 |
|------|-----|
| 仕事、work、業務 | work |
| 健康、health、運動、体 | health |
| 学習、learning、勉強、学び | learning |
| 人間関係、relations、友人、家族 | relations |
| お金、finance、金融、投資 | finance |
| 個人、personal、趣味、プライベート | personal |

## 実行コマンド

### Issue 作成

```bash
gh issue create \
  --repo tungstenwarawara/task-manager \
  --title "[Task] {TITLE}" \
  --label "type:task,pillar:{PILLAR},priority:{PRIORITY}" \
  --body "{DESCRIPTION}"
```

### 今日のタスクに追加（オプション）

```bash
gh issue edit {ISSUE_NUMBER} \
  --add-label "status:today" \
  --repo tungstenwarawara/task-manager
```

## 応答形式

```
タスクを作成しました:
- Issue: #{NUMBER} {TITLE}
- Labels: type:task, pillar:{PILLAR}, priority:{PRIORITY}
- URL: https://github.com/tungstenwarawara/task-manager/issues/{NUMBER}

今日やりますか？
```

## 対話フローの例

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

## エラーハンドリング

| 状況 | 応答 |
|------|------|
| gh が認証されていない | `gh auth login を実行してください` |
| リポジトリにアクセスできない | `リポジトリへのアクセス権限を確認してください` |
| ラベルが存在しない | `scripts/setup-labels.sh を実行してラベルを設定してください` |
