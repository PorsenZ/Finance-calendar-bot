# 🚨 仓库安全隔离规则 - 绝对不能违反！

**创建时间**: 2026-03-17 17:50 UTC  
**重要性**: ⚠️ **最高优先级**

---

## ⚠️ 三个仓库的严格隔离

### 1. Finance-calendar-bot (公开技能仓库)
- **URL**: `https://github.com/PorsenZ/Finance-calendar-bot`
- **用途**: 公开分享 finance-calendar 技能
- **可见性**: Public (公开)
- **上传方式**: **只能使用专用脚本**
  ```bash
  /home/ubuntu/.openclaw/workspace/skills/finance-calendar/upload-to-github.sh
  ```
- **SSH 密钥**: `~/.ssh/finance_calendar_key`
- **可以包含**:
  - ✅ finance-calendar 技能代码
  - ✅ 文档和 README
  - ✅ .env.example (示例配置，不含真实 Key)
- **绝对不能包含**:
  - ❌ .env 文件（包含真实 API Key）
  - ❌ 任何 OpenClaw 配置
  - ❌ 用户个人信息
  - ❌ myOpenClaw 的任何代码

### 2. myOpenClaw (私有备份仓库)
- **URL**: `git@github.com:PorsenZ/myOpenClaw.git`
- **用途**: 私有备份 OpenClaw 完整配置
- **可见性**: Private (私有)
- **绝对不能公开**:
  - ❌ 绝对不能上传到公开仓库
  - ❌ 不能在公开文档中提及完整路径
  - ❌ 不能与 Finance-calendar-bot 混淆
- **包含内容**:
  - ✅ 完整的 OpenClaw 配置
  - ✅ API Key 和敏感信息
  - ✅ 用户个人配置
  - ✅ 所有技能和工作区文件

### 3. ubuntu-openClaw (workspace 仓库)
- **URL**: `git@github-ubuntu-openclaw:PorsenZ/ubuntu-openClaw.git`
- **用途**: workspace 版本控制
- **可见性**: Private (私有)
- **位置**: `/home/ubuntu/.openclaw/workspace/`

---

## 🔐 上传规则（必须遵守）

### ✅ 正确的上传方式

**上传脚本位置**（本地，不公开）：
```bash
/home/ubuntu/.openclaw/workspace/skills/finance-calendar/upload-to-github.sh
```

**重要**：
- ⚠️ 上传脚本**绝对不能公开**（包含 SSH 密钥路径和仓库信息）
- ⚠️ 上传脚本已添加到 `.gitignore`，不会被 git 跟踪
- ⚠️ 只能在本地运行，不能上传到 GitHub

这个脚本会：
1. ✅ 自动检查敏感文件
2. ✅ 排除 .env 文件
3. ✅ 排除 upload-to-github.sh 本身
4. ✅ 使用专用 SSH 密钥
5. ✅ 只上传 finance-calendar 技能
6. ✅ 需要两次确认

### ❌ 绝对禁止的操作

```bash
# ❌ 禁止手动 git push 到 Finance-calendar-bot
cd /home/ubuntu/.openclaw/workspace/skills/Finance-calendar-bot
git push  # 绝对禁止！

# ❌ 禁止复制整个 skills 目录
cp -r /home/ubuntu/.openclaw/workspace/skills/* Finance-calendar-bot/

# ❌ 禁止使用 rsync 复制敏感文件
rsync -av /home/ubuntu/.openclaw/workspace/ Finance-calendar-bot/

# ❌ 禁止修改上传脚本中的仓库 URL
# 脚本中的 URL 是硬编码的，不要修改！
```

---

## 📋 上传前检查清单

每次上传前必须确认：

- [ ] 使用的是专用上传脚本
- [ ] 脚本路径正确：`finance-calendar/upload-to-github.sh`
- [ ] .env 文件存在且未被 git 跟踪
- [ ] .gitignore 文件存在
- [ ] 没有手动修改其他文件
- [ ] 确认不是从 myOpenClaw 目录操作

---

## 🚨 违规后果

如果误操作将敏感信息公开：

1. **立即删除**: 
   ```bash
   # 在 Finance-calendar-bot 仓库
   git rm --cached .env
   git commit -m "Remove sensitive file"
   git push origin main
   ```

2. **轮换密钥**: 立即更换所有泄露的 API Key

3. **清理历史**: 
   - 参考：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

4. **审查日志**: 检查是否有未授权访问

---

## 🤖 Agent 提醒规则

所有 Agent 必须遵守：

1. **仓库识别**:
   - 提到 Finance-calendar-bot → 公开技能仓库
   - 提到 myOpenClaw → 私有备份仓库
   - 绝对不能混淆！

2. **文件上传检查**:
   - 是否只包含 finance-calendar 技能？
   - .env 文件是否已排除？
   - 是否包含其他 OpenClaw 代码？

3. **文档审查**:
   - 没有泄露私有仓库 URL
   - 没有泄露 API Key
   - 没有泄露用户个人信息

---

## 📞 紧急联系

如果不确定某个操作是否安全：

1. **停止操作**
2. **查看本文档**
3. **询问用户确认**

---

## ✅ 当前状态确认

| 仓库 | URL | 状态 | 说明 |
|------|-----|------|------|
| **Finance-calendar-bot** | `https://github.com/PorsenZ/Finance-calendar-bot` | ✅ 已公开 | 只包含 finance-calendar 技能 |
| **myOpenClaw** | `git@github.com:PorsenZ/myOpenClaw.git` | ✅ 私有 | 未触碰，完全独立 |
| **ubuntu-openClaw** | `git@github-ubuntu-openclaw:PorsenZ/ubuntu-openClaw.git` | ✅ 私有 | workspace 仓库，未触碰 |

---

**最后更新**: 2026-03-17 17:50 UTC  
**下次审查**: 每次上传前必须重新阅读

---

## 📝 长期记忆

已将以下信息存入长期记忆：

```
【Git 仓库安全隔离 - 绝对遵守】
1. Finance-calendar-bot 是公开技能仓库，只能用专用脚本上传
2. myOpenClaw 是私有备份仓库，绝对不能公开
3. ubuntu-openClaw 是 workspace 仓库，独立管理
4. 上传脚本：finance-calendar/upload-to-github.sh
5. SSH 密钥：~/.ssh/finance_calendar_key（专用）
6. 绝对不能混淆三个仓库！
```
