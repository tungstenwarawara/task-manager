# Complete Task / タスク完了

タスクを完了にします。

## トリガー

- `#{番号} を完了`
- `#{番号} 完了`
- `#{番号} をクローズ`
- `#{番号} done`

## 実行手順

### 1. Issue の情報を取得

```bash
gh issue view {NUMBER} \
  --repo tungstenwarawara/task-manager \
  --json number,title,state,labels
```

### 2. Issue をクローズ

```bash
gh issue close {NUMBER} --repo tungstenwarawara/task-manager
```

### 3. ステータスラベルを削除（オプション）

```bash
gh issue edit {NUMBER} \
  --remove-label "status:today,status:this-week" \
  --repo tungstenwarawara/task-manager
```

### 4. 残りのタスク数を取得

```bash
gh issue list \
  --repo tungstenwarawara/task-manager \
  --state open \
  --label "status:today" \
  --json number | jq 'length'
```

## 応答形式

```
#{NUMBER}「{TITLE}」を完了にしました。お疲れ様です!

今日の残りタスク: {COUNT}件
```

## エラーハンドリング

| 状況 | 応答 |
|------|------|
| Issue が存在しない | `#{NUMBER} は見つかりませんでした` |
| 既にクローズ済み | `#{NUMBER} は既に完了しています` |
| 権限がない | `権限がありません。gh auth status を確認してください` |

## 例

```
User: #15 を完了

Claude: [gh issue view 15 を実行して情報取得]
        [gh issue close 15 を実行]

#15「本を30分読む」を完了にしました。お疲れ様です!

今日の残りタスク: 2件
- #12 企画書のレビュー
- #18 請求書の確認
```
