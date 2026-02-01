# Weekly Review / 週次レビュー

週次レビューを行います。

## トリガー

- `週次レビュー`
- `今週の振り返り`
- `週次レビューをしよう`
- `weekly review`
- `今週のまとめ`

## 使い方

今週の振り返りと来週の計画を行います。

## 手順

1. 今週完了したタスクを取得:
```bash
gh issue list \
  --repo tungstenwarawara/task-manager \
  --state closed \
  --search "closed:>=YYYY-MM-DD" \
  --json title,closedAt,labels
```

2. 今週の日記を確認:
```bash
ls knowledge-base/journal/YYYY/MM/
```

3. 未完了のタスクを確認:
```bash
gh issue list \
  --repo tungstenwarawara/task-manager \
  --state open \
  --json title,labels,createdAt
```

4. ユーザーに以下を質問:
   - 今週うまくいったことは？
   - 今週の課題は？
   - 来週フォーカスしたいことは？

5. 週次レビューを記録:
   - パス: `knowledge-base/journal/YYYY/MM/week-WW.md`

## テンプレート

```markdown
# Week WW Review (MM/DD - MM/DD)

## 完了したタスク
-

## 未完了のタスク
-

## 今週の振り返り

### うまくいったこと
-

### 課題・改善点
-

## 来週のフォーカス
1.
2.
3.

## Pillar別の進捗
- Work:
- Health:
- Learning:
- Relationships:
- Finance:
- Personal:

---
*Created: YYYY-MM-DD*
```

## 例

```
> 週次レビューをしよう

Claude: 今週の振り返りを始めましょう。まず今週完了したタスクを確認します...

完了したタスク:
- [Task] 企画書を作成する (pillar:work)
- [Task] 本を読む (pillar:learning)
- [Routine] 週次ミーティング (pillar:work)

今週うまくいったことは何ですか？

> 企画書を予定通り完成できた

Claude: 素晴らしいですね！今週の課題や改善点はありましたか？

> 運動の時間が取れなかった

Claude: なるほど。来週フォーカスしたいことは何ですか？

> 毎日30分の運動時間を確保する

Claude: 週次レビューを作成しました。来週も頑張りましょう！
```
