# 🔒 安全隔离说明 - 至关重要！

**创建时间**: 2026-03-17 17:25 UTC (北京时间 2026-03-18 01:25)

---

## ⚠️ 重要警告

本技能包含两个完全独立的 Git 仓库，**绝对不能混淆**：

### 1. 公开仓库 - Finance-calendar-bot
- **URL**: `https://github.com/PorsenZ/Finance-calendar-bot`
- **用途**: 公开分享经济日历技能
- **可见性**: 公开 (Public)
- **可以上传**: 
  - ✅ fmp-economic-calendar 技能代码
  - ✅ 文档和 README
  - ✅ .env.example (示例配置，不含真实 Key)
- **禁止上传**:
  - ❌ .env 文件 (包含真实 API Key)
  - ❌ 任何包含敏感信息的文件
  - ❌ 其他 OpenClaw 代码
  - ❌ 用户个人信息

### 2. 私有备份仓库 - myOpenClaw
- **URL**: `git@github.com:PorsenZ/myOpenClaw.git`
- **用途**: 私有备份 OpenClaw 完整配置
- **可见性**: 私有 (Private)
- **可以包含**:
  - ✅ 完整的 OpenClaw 配置
  - ✅ API Key 和敏感信息
  - ✅ 用户个人配置
  - ✅ 所有技能和工作区文件
- **禁止公开**:
  - ❌ 绝对不能公开此仓库
  - ❌ 不能在任何公开文档中提及完整路径

---

## 🔐 敏感信息保护

### .env 文件管理

1. **创建 .env.example** (可公开):
   ```bash
   # API 配置示例
   COINDAR_API_KEY=
   FOREX_FACTORY_URL=https://nfs.faireconomy.media/ff_calendar_thisweek.json
   ```

2. **创建 .env** (禁止公开):
   ```bash
   # .env 已添加到 .gitignore，切勿手动上传！
   COINDAR_API_KEY=你的真实 API_KEY
   ```

3. **Git 配置**:
   ```bash
   # .gitignore 已包含：
   .env
   .env.local
   .env.*.local
   ```

---

## 📦 上传到公开仓库的步骤

### 准备阶段
```bash
# 1. 确认只包含 fmp-economic-calendar 技能
cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/

# 2. 检查没有敏感文件
ls -la .env  # 应该存在，但不会被 git 跟踪
git status   # 确保 .env 不在暂存区
```

### 上传流程
```bash
# 1. 克隆公开仓库（如果还没有）
cd /home/ubuntu/.openclaw/workspace/skills/
git clone git@github.com:PorsenZ/Finance-calendar-bot.git

# 2. 复制技能文件（不包括 .env）
cp -r fmp-economic-calendar/* Finance-calendar-bot/

# 3. 进入公开仓库
cd Finance-calendar-bot

# 4. 检查文件
git status
# 应该看到：
# - 所有技能文件 ✅
# - .env.example ✅
# - .gitignore ✅
# - .env 不应该出现！❌

# 5. 提交并推送
git add .
git commit -m "Add economic calendar skill"
git push origin main
```

---

## 🤖 Agent 提醒规则

所有 Agent 必须遵守以下规则：

### 1. 仓库识别
```
当提到 GitHub 仓库时，必须明确区分：
- Finance-calendar-bot → 公开技能仓库
- myOpenClaw → 私有备份仓库
```

### 2. 文件上传检查
```
上传前必须检查：
- [ ] 是否只包含 fmp-economic-calendar 技能？
- [ ] .env 文件是否已排除？
- [ ] 是否包含其他 OpenClaw 代码？
- [ ] 是否包含用户个人信息？
```

### 3. 文档审查
```
所有公开文档必须检查：
- [ ] 没有泄露私有仓库 URL
- [ ] 没有泄露 API Key
- [ ] 没有泄露用户个人信息
- [ ] 使用的是正确的公开仓库 URL
```

---

## 📝 长期记忆更新

需要将以下信息存入长期记忆：

```
【安全隔离规则】
1. Finance-calendar-bot (https://github.com/PorsenZ/Finance-calendar-bot) 是公开技能仓库
2. myOpenClaw (git@github.com:PorsenZ/myOpenClaw.git) 是私有备份仓库，绝对不能公开
3. 上传公开仓库前必须排除 .env 文件和所有敏感信息
4. 只允许上传 fmp-economic-calendar 技能，不能上传其他 OpenClaw 代码
5. 所有 Agent 必须严格遵守这两个仓库的隔离规则
```

---

## ✅ 检查清单

上传前必须完成：

- [ ] 确认使用的是 Finance-calendar-bot 仓库
- [ ] 确认 .env 文件已添加到 .gitignore
- [ ] 确认没有包含其他 OpenClaw 技能
- [ ] 确认没有泄露私有仓库 URL
- [ ] 确认文档中使用的是公开仓库 URL
- [ ] 运行 `git status` 检查没有敏感文件
- [ ] 人工审查所有要上传的文件

---

## 🚨 违规后果

如果混淆仓库或泄露敏感信息：

1. **立即撤销**: 立即删除公开仓库中的敏感文件
2. **轮换密钥**: 立即更换所有泄露的 API Key
3. **审查日志**: 检查是否有未授权访问
4. **更新规则**: 加强安全检查和 Agent 培训

---

**最后更新**: 2026-03-17 17:25 UTC  
**下次审查**: 每次上传公开仓库前
