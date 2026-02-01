#!/bin/bash
# knowledge-base リポジトリの初期化スクリプト
#
# 使用方法:
#   1. GitHub で knowledge-base リポジトリを作成 (private)
#   2. このスクリプトを実行
#
# 必要条件:
#   - knowledge-base リポジトリが GitHub に存在すること
#   - git が認証済みであること

set -e

OWNER="tungstenwarawara"
REPO="knowledge-base"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK_MANAGER_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== knowledge-base リポジトリの初期化 ==="
echo ""

# 作業ディレクトリ
WORK_DIR="${1:-$HOME/knowledge-base}"

if [ -d "$WORK_DIR/.git" ]; then
    echo "✓ $WORK_DIR は既に git リポジトリです"
    cd "$WORK_DIR"
else
    echo "リポジトリをクローン中..."
    git clone "https://github.com/$OWNER/$REPO.git" "$WORK_DIR" 2>/dev/null || {
        echo "クローンに失敗しました。リポジトリを初期化します..."
        mkdir -p "$WORK_DIR"
        cd "$WORK_DIR"
        git init
        git remote add origin "https://github.com/$OWNER/$REPO.git"
    }
    cd "$WORK_DIR"
fi

# ディレクトリ構造を作成
echo "ディレクトリ構造を作成中..."
mkdir -p journal notes/topics digest resources

# テンプレートファイルをコピー
echo "テンプレートファイルをコピー中..."
if [ -f "$TASK_MANAGER_DIR/templates/knowledge-base/interests.yaml" ]; then
    cp "$TASK_MANAGER_DIR/templates/knowledge-base/interests.yaml" ./interests.yaml
fi

if [ -f "$TASK_MANAGER_DIR/templates/knowledge-base/README.md" ]; then
    cp "$TASK_MANAGER_DIR/templates/knowledge-base/README.md" ./README.md
fi

if [ -f "$TASK_MANAGER_DIR/templates/knowledge-base/journal/TEMPLATE.md" ]; then
    cp "$TASK_MANAGER_DIR/templates/knowledge-base/journal/TEMPLATE.md" ./journal/TEMPLATE.md
fi

# .gitkeep ファイルを作成
touch journal/.gitkeep notes/.gitkeep notes/topics/.gitkeep digest/.gitkeep resources/.gitkeep

# コミット
echo "変更をコミット中..."
git add -A
git commit -m "Initialize knowledge-base repository" 2>/dev/null || echo "変更なし"

# プッシュ
echo "リモートにプッシュ中..."
git branch -M main
git push -u origin main 2>/dev/null || {
    echo ""
    echo "⚠️ プッシュに失敗しました"
    echo "手動で以下を実行してください:"
    echo "  cd $WORK_DIR"
    echo "  git push -u origin main"
}

echo ""
echo "✓ knowledge-base の初期化が完了しました"
echo "  場所: $WORK_DIR"
