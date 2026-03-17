# 📤 上传到 GitHub - 完整指南

**创建时间**: 2026-03-17 17:30 UTC (北京时间 2026-03-18 01:30)

---

## ⚠️ 重要提醒

**两个仓库绝对不能混淆**：

1. **Finance-calendar-bot** (公开)
   - URL: `https://github.com/PorsenZ/Finance-calendar-bot`
   - 用途：公开分享经济日历技能
   - 可见性：Public

2. **myOpenClaw** (私有)
   - URL: `git@github.com:PorsenZ/myOpenClaw.git`
   - 用途：私有备份 OpenClaw 配置
   - 可见性：Private

---

## 📋 上传前检查清单

- [ ] 确认只包含 fmp-economic-calendar 技能
- [ ] .env 文件已添加到 .gitignore
- [ ] 没有包含其他 OpenClaw 代码
- [ ] 没有泄露私有仓库 URL
- [ ] 文档中使用的是公开仓库 URL
- [ ] 已运行安全检查脚本

---

## 🚀 上传方法

### 方法 1：使用上传脚本（推荐）

```bash
# 1. 进入技能目录
cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/

# 2. 运行上传脚本
./upload-to-github.sh

# 3. 按提示操作
# - 脚本会自动检查敏感文件
# - 会显示将要提交的文件列表
# - 需要两次确认
```

### 方法 2：手动上传

```bash
# 1. 克隆公开仓库
cd /home/ubuntu/.openclaw/workspace/skills/
git clone git@github.com:PorsenZ/Finance-calendar-bot.git

# 2. 复制技能文件（排除敏感文件）
rsync -av --exclude='.env' --exclude='.git' \
  fmp-economic-calendar/ Finance-calendar-bot/

# 3. 进入公开仓库
cd Finance-calendar-bot

# 4. 检查文件
git status
# 应该看到：
# ✅ 所有技能文件
# ✅ .env.example
# ✅ .gitignore
# ❌ .env 不应该出现！

# 5. 提交并推送
git add .
git commit -m "Add economic calendar skill"
git push origin main
```

---

## 🔒 安全检查

### 自动检查

上传脚本会自动检查：

```bash
# 检查 .env 是否被 git 跟踪
git ls-files --error-unmatch .env

# 检查敏感文件
for file in .env .env.local openclaw.json *.bak; do
  git ls-files --error-unmatch "$file"
done
```

### 手动检查

```bash
# 1. 查看将要提交的文件
git status

# 2. 查看 .gitignore 内容
cat .gitignore
# 应该包含：.env

# 3. 确认没有敏感文件
ls -la | grep -E "\.env$|openclaw\.json"
```

---

## 📁 上传的文件列表

### ✅ 可以上传

```
fmp-economic-calendar/
├── scripts/
│   ├── forex_factory_calendar.py
│   ├── send_push.py
│   ├── daily_briefing_integration.py
│   └── economic_calendar.py
├── .env.example          # 示例配置（不含真实 Key）
├── .gitignore           # Git 忽略规则
├── requirements.txt     # Python 依赖
├── README.md           # 使用说明
├── README_SIMPLE.md    # 简化版说明
├── SECURITY_ISOLATION.md # 安全隔离说明
├── CONFIGURATION.md    # 配置说明
└── UPGRADED_VERSION.md # 升级版说明
```

### ❌ 禁止上传

```
.env                    # 真实 API Key
.git/                   # Git 目录
__pycache__/            # Python 缓存
*.pyc                   # 编译文件
openclaw.json           # OpenClaw 配置
../other-skills/        # 其他技能
```

---

## ✅ 上传后验证

### 1. 检查 GitHub 仓库

访问：https://github.com/PorsenZ/Finance-calendar-bot

确认：
- [ ] 文件列表正确
- [ ] 没有 .env 文件
- [ ] README 显示正常
- [ ] 使用的是公开仓库 URL

### 2. 测试克隆

```bash
# 在新目录测试克隆
cd /tmp
git clone https://github.com/PorsenZ/Finance-calendar-bot.git
cd Finance-calendar-bot

# 检查文件
ls -la
# 不应该看到 .env 文件

# 测试运行
pip install -r requirements.txt
python3 scripts/forex_factory_calendar.py
```

---

## 🔄 后续更新

### 更新流程

```bash
# 1. 在源目录修改技能
cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/
# ... 修改文件 ...

# 2. 运行上传脚本
./upload-to-github.sh

# 3. 验证更新
# 访问 GitHub 查看更新
```

### 更新 Coindar API Key

如果 Coindar API Key 更新了：

```bash
# 1. 只更新本地 .env 文件
cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/
vim .env  # 更新 COINDAR_API_KEY

# 2. 不要提交 .env 文件！
# .env 已在.gitignore 中

# 3. 如果更新了其他文件，运行上传脚本
./upload-to-github.sh
```

---

## 📞 相关资源

- **公开仓库**: https://github.com/PorsenZ/Finance-calendar-bot
- **私有备份**: git@github.com:PorsenZ/myOpenClaw.git
- **安全说明**: `SECURITY_ISOLATION.md`
- **上传脚本**: `upload-to-github.sh`

---

## 🚨 紧急处理

如果不小心上传了敏感文件：

```bash
# 1. 立即删除公开仓库中的文件
cd /home/ubuntu/.openclaw/workspace/skills/Finance-calendar-bot
git rm --cached .env
git commit -m "Remove sensitive file"
git push origin main

# 2. 轮换 API Key
# 立即更换所有泄露的 API Key

# 3. 检查 Git 历史
git log --all --full-history -- .env

# 4. 如果需要清理 Git 历史
# 参考：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

---

**最后更新**: 2026-03-17 17:30 UTC  
**下次审查**: 每次上传前
