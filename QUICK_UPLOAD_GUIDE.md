# 🚀 Finance-calendar-bot 上传指南

## ⚡ 快速上传（唯一正确方式）

```bash
/home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/upload-to-github.sh
```

**就这么简单！** 脚本会自动：
- ✅ 检查敏感文件
- ✅ 排除 .env 文件
- ✅ 使用专用 SSH 密钥
- ✅ 需要你的确认

---

## 📁 仓库说明

| 仓库 | 用途 | 上传方式 |
|------|------|---------|
| **Finance-calendar-bot** | 公开技能 | `upload-to-github.sh` |
| **myOpenClaw** | 私有备份 | 不要用这个脚本！ |
| **ubuntu-openClaw** | workspace | 独立管理 |

---

## 🔐 SSH 密钥

- **位置**: `~/.ssh/finance_calendar_key`
- **用途**: 仅用于 Finance-calendar-bot
- **不能用于**: myOpenClaw 或其他仓库

---

## ❌ 绝对禁止

```bash
# ❌ 不要手动 git push
cd Finance-calendar-bot && git push  # 禁止！

# ❌ 不要复制整个 skills 目录
cp -r ../skills/* Finance-calendar-bot/  # 禁止！

# ❌ 不要修改脚本中的仓库 URL
# 脚本已硬编码，不要改动！
```

---

## ✅ 上传流程

1. **修改技能文件**
   ```bash
   cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/
   # 修改你的文件...
   ```

2. **运行上传脚本**
   ```bash
   ./upload-to-github.sh
   ```

3. **确认两次**
   - 第一次：确认操作
   - 第二次：确认提交的文件列表

4. **完成**
   - 查看：https://github.com/PorsenZ/Finance-calendar-bot

---

## 📞 有问题？

1. 查看：`REPOSITORY_SECURITY_RULES.md`
2. 查看：`UPLOAD_GUIDE.md`
3. 询问用户确认

---

**记住**: 只能用这个脚本上传，其他任何方式都可能导致敏感信息泄露！
