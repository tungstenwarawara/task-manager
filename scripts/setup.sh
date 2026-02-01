#!/bin/bash
# セットアップスクリプト - GitHub CLI を使用
# 使用方法: ./scripts/setup.sh

set -e

echo "=== Life Task Manager セットアップ ==="
echo ""

# gh CLI の確認
if ! command -v gh &> /dev/null; then
    echo "❌ gh CLI がインストールされていません"
    echo "インストール方法: https://cli.github.com/"
    echo ""
    echo "macOS: brew install gh"
    echo "Ubuntu: sudo apt install gh"
    echo "Windows: winget install GitHub.cli"
    exit 1
fi

# 認証確認
if ! gh auth status &> /dev/null; then
    echo "❌ gh CLI が認証されていません"
    echo "実行してください: gh auth login"
    exit 1
fi

echo "✓ gh CLI が利用可能です"
echo ""

OWNER="tungstenwarawara"
TASK_REPO="task-manager"
KB_REPO="knowledge-base"

# ============================
# Step 1: ラベルの設定
# ============================
echo "=== Step 1: ラベルの設定 ==="

setup_labels() {
    local repo="$OWNER/$TASK_REPO"

    echo "Pillar ラベルを作成中..."
    gh label create "pillar:work" --color "0052CC" --description "仕事" --repo "$repo" 2>/dev/null || gh label edit "pillar:work" --color "0052CC" --description "仕事" --repo "$repo"
    gh label create "pillar:health" --color "2EA44F" --description "健康" --repo "$repo" 2>/dev/null || gh label edit "pillar:health" --color "2EA44F" --description "健康" --repo "$repo"
    gh label create "pillar:learning" --color "7057FF" --description "学習" --repo "$repo" 2>/dev/null || gh label edit "pillar:learning" --color "7057FF" --description "学習" --repo "$repo"
    gh label create "pillar:relations" --color "E99695" --description "人間関係" --repo "$repo" 2>/dev/null || gh label edit "pillar:relations" --color "E99695" --description "人間関係" --repo "$repo"
    gh label create "pillar:finance" --color "FBCA04" --description "お金" --repo "$repo" 2>/dev/null || gh label edit "pillar:finance" --color "FBCA04" --description "お金" --repo "$repo"
    gh label create "pillar:personal" --color "006B75" --description "個人" --repo "$repo" 2>/dev/null || gh label edit "pillar:personal" --color "006B75" --description "個人" --repo "$repo"

    echo "Type ラベルを作成中..."
    gh label create "type:task" --color "1D76DB" --description "単発タスク" --repo "$repo" 2>/dev/null || gh label edit "type:task" --color "1D76DB" --description "単発タスク" --repo "$repo"
    gh label create "type:project" --color "5319E7" --description "プロジェクト" --repo "$repo" 2>/dev/null || gh label edit "type:project" --color "5319E7" --description "プロジェクト" --repo "$repo"
    gh label create "type:routine" --color "0E8A16" --description "定期タスク" --repo "$repo" 2>/dev/null || gh label edit "type:routine" --color "0E8A16" --description "定期タスク" --repo "$repo"
    gh label create "type:idea" --color "D4C5F9" --description "アイデア" --repo "$repo" 2>/dev/null || gh label edit "type:idea" --color "D4C5F9" --description "アイデア" --repo "$repo"

    echo "Priority ラベルを作成中..."
    gh label create "priority:high" --color "B60205" --description "優先度: 高" --repo "$repo" 2>/dev/null || gh label edit "priority:high" --color "B60205" --description "優先度: 高" --repo "$repo"
    gh label create "priority:medium" --color "FBCA04" --description "優先度: 中" --repo "$repo" 2>/dev/null || gh label edit "priority:medium" --color "FBCA04" --description "優先度: 中" --repo "$repo"
    gh label create "priority:low" --color "0E8A16" --description "優先度: 低" --repo "$repo" 2>/dev/null || gh label edit "priority:low" --color "0E8A16" --description "優先度: 低" --repo "$repo"

    echo "Status ラベルを作成中..."
    gh label create "status:today" --color "FF6B6B" --description "今日やる" --repo "$repo" 2>/dev/null || gh label edit "status:today" --color "FF6B6B" --description "今日やる" --repo "$repo"
    gh label create "status:this-week" --color "4ECDC4" --description "今週やる" --repo "$repo" 2>/dev/null || gh label edit "status:this-week" --color "4ECDC4" --description "今週やる" --repo "$repo"
    gh label create "status:blocked" --color "D93F0B" --description "ブロック中" --repo "$repo" 2>/dev/null || gh label edit "status:blocked" --color "D93F0B" --description "ブロック中" --repo "$repo"

    echo "✓ ラベル設定完了"
}

setup_labels

# ============================
# Step 2: knowledge-base リポジトリの作成
# ============================
echo ""
echo "=== Step 2: knowledge-base リポジトリの作成 ==="

create_knowledge_base() {
    # リポジトリが存在するか確認
    if gh repo view "$OWNER/$KB_REPO" &> /dev/null; then
        echo "✓ $KB_REPO リポジトリは既に存在します"
    else
        echo "knowledge-base リポジトリを作成中..."
        gh repo create "$KB_REPO" --private --description "Knowledge base for Life Task Manager"
        echo "✓ $KB_REPO リポジトリを作成しました"
    fi

    # テンプレートファイルを取得してプッシュ
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    gh repo clone "$OWNER/$KB_REPO" . 2>/dev/null || git init

    # ディレクトリ構造を作成
    mkdir -p journal notes/topics digest resources

    # interests.yaml をコピー
    if [ -f "$OLDPWD/templates/knowledge-base/interests.yaml" ]; then
        cp "$OLDPWD/templates/knowledge-base/interests.yaml" ./interests.yaml
    fi

    # README を作成
    if [ -f "$OLDPWD/templates/knowledge-base/README.md" ]; then
        cp "$OLDPWD/templates/knowledge-base/README.md" ./README.md
    fi

    # .gitkeep ファイルを作成
    touch journal/.gitkeep notes/.gitkeep notes/topics/.gitkeep digest/.gitkeep resources/.gitkeep

    # 日記テンプレートをコピー
    if [ -f "$OLDPWD/templates/knowledge-base/journal/TEMPLATE.md" ]; then
        cp "$OLDPWD/templates/knowledge-base/journal/TEMPLATE.md" ./journal/TEMPLATE.md
    fi

    git add -A
    git commit -m "Initialize knowledge-base repository" 2>/dev/null || echo "Nothing to commit"

    # リモートが設定されていなければ追加
    if ! git remote | grep -q origin; then
        git remote add origin "https://github.com/$OWNER/$KB_REPO.git"
    fi

    git branch -M main
    git push -u origin main 2>/dev/null || echo "Push failed or already up to date"

    cd "$OLDPWD"
    rm -rf "$TEMP_DIR"

    echo "✓ knowledge-base リポジトリのセットアップ完了"
}

create_knowledge_base

# ============================
# Step 3: GitHub Project の作成
# ============================
echo ""
echo "=== Step 3: GitHub Project の作成 ==="

create_project() {
    # ユーザーレベルのプロジェクトを作成
    PROJECT_ID=$(gh project list --owner "$OWNER" --format json | jq -r '.projects[] | select(.title == "Life Dashboard") | .number' 2>/dev/null)

    if [ -n "$PROJECT_ID" ] && [ "$PROJECT_ID" != "null" ]; then
        echo "✓ Life Dashboard プロジェクトは既に存在します (ID: $PROJECT_ID)"
    else
        echo "Life Dashboard プロジェクトを作成中..."
        gh project create --owner "$OWNER" --title "Life Dashboard" 2>/dev/null || echo "プロジェクト作成をスキップ（手動で作成してください）"
        echo "✓ プロジェクト作成完了"
    fi

    echo ""
    echo "カスタムフィールドは手動で追加してください:"
    echo "  1. https://github.com/users/$OWNER/projects/ にアクセス"
    echo "  2. Life Dashboard プロジェクトを開く"
    echo "  3. 以下のフィールドを追加:"
    echo "     - Status (Single select): Inbox, Today, This Week, Scheduled, Done, Archived"
    echo "     - Pillar (Single select): Work, Health, Learning, Relationships, Finance, Personal"
    echo "     - Priority (Single select): High, Medium, Low"
    echo "     - Energy (Single select): High Focus, Low Focus, Routine"
    echo "     - Due Date (Date)"
    echo "     - Recurrence (Single select): Daily, Weekly, Monthly, None"
}

create_project

# ============================
# Step 4: Secrets の確認
# ============================
echo ""
echo "=== Step 4: GitHub Secrets の設定 ==="
echo ""
echo "以下の Secrets を手動で設定してください:"
echo "  Settings > Secrets and variables > Actions"
echo ""
echo "  - ANTHROPIC_API_KEY: Claude API キー (必須)"
echo "    取得: https://console.anthropic.com/"
echo ""
echo "  - YOUTUBE_API_KEY: YouTube Data API キー (オプション)"
echo "    取得: https://console.cloud.google.com/"
echo ""

# ============================
# 完了
# ============================
echo ""
echo "=== セットアップ完了 ==="
echo ""
echo "次のステップ:"
echo "  1. GitHub Project のカスタムフィールドを設定"
echo "  2. ANTHROPIC_API_KEY を Secrets に追加"
echo "  3. Claude Code を起動してタスク管理を開始"
echo ""
echo "使用例:"
echo "  > 今日のタスクを見せて"
echo "  > 企画書を作成する をタスクに追加、優先度高"
echo "  > 日記を書きたい"
