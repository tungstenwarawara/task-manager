#!/bin/bash
# Setup labels for task-manager repository
# Usage: ./setup-labels.sh [owner/repo]

REPO="${1:-tungstenwarawara/task-manager}"

echo "Setting up labels for $REPO..."

# Delete default labels (optional - uncomment if needed)
# gh label delete "bug" --repo "$REPO" --yes 2>/dev/null
# gh label delete "documentation" --repo "$REPO" --yes 2>/dev/null
# gh label delete "duplicate" --repo "$REPO" --yes 2>/dev/null
# gh label delete "enhancement" --repo "$REPO" --yes 2>/dev/null
# gh label delete "good first issue" --repo "$REPO" --yes 2>/dev/null
# gh label delete "help wanted" --repo "$REPO" --yes 2>/dev/null
# gh label delete "invalid" --repo "$REPO" --yes 2>/dev/null
# gh label delete "question" --repo "$REPO" --yes 2>/dev/null
# gh label delete "wontfix" --repo "$REPO" --yes 2>/dev/null

# Pillar labels (領域)
gh label create "pillar:work" --color "0052CC" --description "仕事" --repo "$REPO" 2>/dev/null || gh label edit "pillar:work" --color "0052CC" --description "仕事" --repo "$REPO"
gh label create "pillar:health" --color "2EA44F" --description "健康" --repo "$REPO" 2>/dev/null || gh label edit "pillar:health" --color "2EA44F" --description "健康" --repo "$REPO"
gh label create "pillar:learning" --color "7057FF" --description "学習" --repo "$REPO" 2>/dev/null || gh label edit "pillar:learning" --color "7057FF" --description "学習" --repo "$REPO"
gh label create "pillar:relations" --color "E99695" --description "人間関係" --repo "$REPO" 2>/dev/null || gh label edit "pillar:relations" --color "E99695" --description "人間関係" --repo "$REPO"
gh label create "pillar:finance" --color "FBCA04" --description "お金" --repo "$REPO" 2>/dev/null || gh label edit "pillar:finance" --color "FBCA04" --description "お金" --repo "$REPO"
gh label create "pillar:personal" --color "006B75" --description "個人" --repo "$REPO" 2>/dev/null || gh label edit "pillar:personal" --color "006B75" --description "個人" --repo "$REPO"

# Type labels (タイプ)
gh label create "type:task" --color "1D76DB" --description "単発タスク" --repo "$REPO" 2>/dev/null || gh label edit "type:task" --color "1D76DB" --description "単発タスク" --repo "$REPO"
gh label create "type:project" --color "5319E7" --description "プロジェクト（複数タスクの親）" --repo "$REPO" 2>/dev/null || gh label edit "type:project" --color "5319E7" --description "プロジェクト（複数タスクの親）" --repo "$REPO"
gh label create "type:routine" --color "0E8A16" --description "定期タスク" --repo "$REPO" 2>/dev/null || gh label edit "type:routine" --color "0E8A16" --description "定期タスク" --repo "$REPO"
gh label create "type:idea" --color "D4C5F9" --description "アイデア・いつかやる" --repo "$REPO" 2>/dev/null || gh label edit "type:idea" --color "D4C5F9" --description "アイデア・いつかやる" --repo "$REPO"

# Priority labels (優先度)
gh label create "priority:high" --color "B60205" --description "優先度: 高" --repo "$REPO" 2>/dev/null || gh label edit "priority:high" --color "B60205" --description "優先度: 高" --repo "$REPO"
gh label create "priority:medium" --color "FBCA04" --description "優先度: 中" --repo "$REPO" 2>/dev/null || gh label edit "priority:medium" --color "FBCA04" --description "優先度: 中" --repo "$REPO"
gh label create "priority:low" --color "0E8A16" --description "優先度: 低" --repo "$REPO" 2>/dev/null || gh label edit "priority:low" --color "0E8A16" --description "優先度: 低" --repo "$REPO"

# Status labels (ステータス) - for quick filtering
gh label create "status:today" --color "FF6B6B" --description "今日やる" --repo "$REPO" 2>/dev/null || gh label edit "status:today" --color "FF6B6B" --description "今日やる" --repo "$REPO"
gh label create "status:this-week" --color "4ECDC4" --description "今週やる" --repo "$REPO" 2>/dev/null || gh label edit "status:this-week" --color "4ECDC4" --description "今週やる" --repo "$REPO"
gh label create "status:blocked" --color "D93F0B" --description "ブロック中" --repo "$REPO" 2>/dev/null || gh label edit "status:blocked" --color "D93F0B" --description "ブロック中" --repo "$REPO"

echo "Labels setup complete!"
gh label list --repo "$REPO"
