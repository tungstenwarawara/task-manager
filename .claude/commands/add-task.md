# Add Task

タスクを追加します。

## 使い方

ユーザーが追加したいタスクの情報を収集し、GitHub Issue として作成します。

## 手順

1. タスクの内容を確認
2. 以下の情報を収集（不明な場合は聞く）:
   - タイトル
   - Pillar（領域）: Work / Health / Learning / Relationships / Finance / Personal
   - Priority（優先度）: High / Medium / Low
   - Due Date（期限）: オプション
   - 詳細説明: オプション

3. gh CLI でIssue を作成:
```bash
gh issue create \
  --repo tungstenwarawara/task-manager \
  --title "[Task] タスク名" \
  --label "type:task,pillar:work,priority:medium" \
  --body "説明"
```

4. 作成したIssueをGitHub Projectに追加:
```bash
gh project item-add PROJECT_NUMBER --owner tungstenwarawara --url ISSUE_URL
```

## 例

```
> 明日までに企画書を作成する、優先度高

gh issue create \
  --repo tungstenwarawara/task-manager \
  --title "[Task] 企画書を作成する" \
  --label "type:task,pillar:work,priority:high" \
  --body "期限: 明日"
```
