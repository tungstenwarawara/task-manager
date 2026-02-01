# Today / 今日のタスク

今日のタスクを確認・管理します。

## トリガー

- `今日のタスクを見せて`
- `今日やることは？`
- `タスク一覧`
- `today`
- `今日のタスク`

## 使い方

今日やるべきタスクの一覧表示と管理を行います。

## 手順

1. 今日のタスクを取得:
```bash
gh issue list \
  --repo tungstenwarawara/task-manager \
  --state open \
  --label "status:today" \
  --json number,title,labels
```

2. 期限が今日のタスクを取得:
```bash
gh issue list \
  --repo tungstenwarawara/task-manager \
  --state open \
  --search "due:YYYY-MM-DD" \
  --json number,title,labels
```

3. 今日のダイジェストを確認（あれば）:
```bash
cat knowledge-base/digest/YYYY/MM/DD.md
```

4. タスク一覧を整形して表示

## 表示例

```
# 今日のタスク (2026-02-01)

## やること
- [ ] #12 企画書のレビュー (pillar:work, priority:high)
- [ ] #15 本を30分読む (pillar:learning, priority:medium)

## 期限が今日
- [ ] #18 請求書の確認 (pillar:finance, priority:high)

## ルーティン
- [ ] 運動30分 (pillar:health)
- [ ] 日記を書く (pillar:personal)

---
今日のダイジェストを見る: /digest
```

## 操作

- タスクを今日に追加: `#番号 を今日やる`
- タスクを完了: `#番号 を完了`
- 新しいタスクを追加: `/add-task`

## 例

```
> 今日のタスクを見せて

Claude: 今日のタスク一覧です:

## やること (3件)
1. #12 企画書のレビュー (Work, High)
2. #15 本を30分読む (Learning, Medium)
3. #18 請求書の確認 (Finance, High)

## 完了済み (1件)
- #10 メール返信 ✓

何かタスクを追加または更新しますか？

> #15 を完了

Claude: #15「本を30分読む」を完了にしました。お疲れ様です！
```
