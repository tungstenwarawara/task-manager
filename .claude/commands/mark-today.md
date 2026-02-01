# Mark for Today / 今日やるにマーク

タスクを今日やるタスクとしてマークします。

## トリガー

- `#{番号} を今日やる`
- `#{番号} を今日に追加`
- `#{番号} today`

## 実行手順

### 1. ラベルを追加

```bash
gh issue edit {NUMBER} \
  --add-label "status:today" \
  --repo tungstenwarawara/task-manager
```

### 2. 今週ラベルがあれば削除

```bash
gh issue edit {NUMBER} \
  --remove-label "status:this-week" \
  --repo tungstenwarawara/task-manager
```

## 応答形式

```
#{NUMBER}「{TITLE}」を今日のタスクに追加しました。

今日のタスク: {COUNT}件
```

## 派生コマンド: 今週やる

### トリガー

- `#{番号} を今週やる`
- `#{番号} を今週に追加`

### 実行

```bash
gh issue edit {NUMBER} \
  --add-label "status:this-week" \
  --remove-label "status:today" \
  --repo tungstenwarawara/task-manager
```

## 例

```
User: #20 を今日やる

Claude: [gh issue edit 20 --add-label "status:today" を実行]

#20「ドキュメント更新」を今日のタスクに追加しました。

今日のタスク: 4件
```
