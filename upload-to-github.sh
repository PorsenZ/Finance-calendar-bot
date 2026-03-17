#!/bin/bash
# 上传经济日历技能到公开仓库
# ⚠️ 使用前请仔细阅读 SECURITY_ISOLATION.md

set -e

echo "🔒 经济日历技能上传脚本"
echo "================================"
echo ""

# 配置
SKILL_DIR="/home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar"
PUBLIC_REPO_DIR="/home/ubuntu/.openclaw/workspace/skills/Finance-calendar-bot"
# 使用 SSH 方式（Finance-calendar-bot 专用密钥）
PUBLIC_REPO_URL="git@github.com:PorsenZ/Finance-calendar-bot.git"
# 配置使用专用 SSH 密钥
export GIT_SSH_COMMAND="ssh -i ~/.ssh/finance_calendar_key -o IdentitiesOnly=yes"

echo "📂 源目录：$SKILL_DIR"
echo "📂 目标目录：$PUBLIC_REPO_DIR"
echo "🔗 仓库地址：$PUBLIC_REPO_URL"
echo ""

# 检查
echo "🔍 检查步骤..."

# 1. 检查源目录
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：技能目录不存在"
    exit 1
fi
echo "✅ 技能目录存在"

# 2. 检查 .env 文件（不应该被 git 跟踪）
cd "$SKILL_DIR"
if git ls-files --error-unmatch .env 2>/dev/null; then
    echo "❌ 错误：.env 文件已被 git 跟踪！"
    exit 1
fi
echo "✅ .env 文件未被 git 跟踪"

# 3. 检查.gitignore
if [ ! -f ".gitignore" ]; then
    echo "❌ 错误：缺少.gitignore 文件"
    exit 1
fi
echo "✅ .gitignore 文件存在"

# 4. 检查敏感文件
echo ""
echo "🔍 检查敏感文件..."
SENSITIVE_FILES=(".env" ".env.local" "openclaw.json" "*.bak")
for file in "${SENSITIVE_FILES[@]}"; do
    if git ls-files --error-unmatch "$file" 2>/dev/null; then
        echo "❌ 错误：敏感文件 $file 将被上传！"
        exit 1
    fi
done
echo "✅ 没有敏感文件会被上传"

# 5. 确认操作
echo ""
echo "⚠️  即将执行的操作："
echo "   1. 克隆/更新公开仓库"
echo "   2. 复制技能文件（排除敏感文件）"
echo "   3. 提交并推送到 GitHub"
echo ""
read -p "确认继续？(y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ 操作已取消"
    exit 0
fi

# 执行上传
echo ""
echo "🚀 开始上传..."

# 克隆或更新仓库
if [ ! -d "$PUBLIC_REPO_DIR" ]; then
    echo "📥 克隆公开仓库..."
    cd /home/ubuntu/.openclaw/workspace/skills/
    git clone "$PUBLIC_REPO_URL" Finance-calendar-bot
else
    echo "📥 更新公开仓库..."
    cd "$PUBLIC_REPO_DIR"
    git pull origin main
fi

# 复制文件
echo "📋 复制技能文件..."
cd "$SKILL_DIR"
rsync -av --exclude='.env' --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' ./ "$PUBLIC_REPO_DIR/"

# 提交
echo "📝 提交更改..."
cd "$PUBLIC_REPO_DIR"
git add .
git status

# 最终确认
echo ""
echo "⚠️  以下文件将被提交："
git status --short
echo ""
read -p "确认提交？(y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ 操作已取消"
    exit 0
fi

git commit -m "Update economic calendar skill"
git push origin main

echo ""
echo "✅ 上传完成！"
echo "🔗 查看：https://github.com/PorsenZ/Finance-calendar-bot"
