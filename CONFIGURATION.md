# 经济日历推送配置说明

**创建时间**: 2026-03-17 17:10 UTC (北京时间 2026-03-18 01:10)  
**状态**: ✅ 配置完成，等待测试

---

## 📊 数据源

**Forex Factory 官方 JSON API**
- URL: `https://nfs.faireconomy.media/ff_calendar_thisweek.json`
- 特点：官方数据、实时更新、免费无需 API Key

---

## 🕐 定时推送配置

### 1. 早间推送（北京时间 08:00）
- **Cron ID**: `1d709b64-5320-4686-a9be-8a45e5575a3a`
- **Cron 表达式**: `30 23 * * *` (UTC 23:30 = 北京时间 07:30)
- **内容**: 
  - 今日高重要性事件（最多 5 个）
  - 明日预告（最多 3 个）

### 2. 晚间推送（北京时间 20:00）
- **Cron ID**: `a77dbc45-3fa3-485c-9305-736ae36b9f10`
- **Cron 表达式**: `0 12 * * *` (UTC 12:00 = 北京时间 20:00)
- **内容**: 
  - 明日高重要性事件（全部）

---

## 📱 推送渠道

### 飞书
- **渠道**: `feishu`
- **Target**: `openclaw-news`
- **配置位置**: `openclaw.json` → `channels.feishu.accounts`

### Telegram
- **渠道**: `telegram`
- **Target**: `TraderAgentsNewsBot`
- **配置位置**: `openclaw.json` → `channels.telegram.accounts`

---

## 🤖 ai-daily-briefing 集成

### 使用方法

在每日首次对话时，自动激活经济日历提醒。

**脚本位置**: `skills/fmp-economic-calendar/scripts/daily_briefing_integration.py`

**测试命令**:
```bash
python3 skills/fmp-economic-calendar/scripts/daily_briefing_integration.py
```

**输出示例**:
```
⚠️ **今日经济日历重点提醒**

今天有 **1 个高重要性事件** 需要注意：

1. **08:30** - RBA Press Conference 🇦🇺

建议关注市场波动风险。
```

### 集成到 ai-daily-briefing

在 `ai-daily-briefing` skill 中添加以下内容：

```python
# 获取经济日历提醒
import subprocess
result = subprocess.run(
    ['python3', 'skills/fmp-economic-calendar/scripts/daily_briefing_integration.py'],
    capture_output=True,
    text=True
)
calendar_reminder = result.stdout

# 添加到每日简报
if calendar_reminder:
    briefing_lines.append("")
    briefing_lines.append(calendar_reminder)
```

---

## 📁 脚本清单

```
skills/fmp-economic-calendar/scripts/
├── forex_factory_calendar.py      # 主脚本（获取并格式化日历）
├── send_push.py                   # 推送脚本（飞书 + Telegram）
├── daily_briefing_integration.py  # ai-daily-briefing 集成
└── economic_calendar.py           # 多数据源版本（备用）
```

---

## 🧪 测试方法

### 1. 测试数据获取
```bash
python3 skills/fmp-economic-calendar/scripts/forex_factory_calendar.py \
  --output shared/02_outbox/economic_calendar_test.md
```

### 2. 测试推送（本地模式）
```bash
python3 skills/fmp-economic-calendar/scripts/send_push.py \
  --type morning \
  --channels local \
  --test
```

### 3. 测试 ai-daily-briefing
```bash
python3 skills/fmp-economic-calendar/scripts/daily_briefing_integration.py
```

### 4. 手动触发 cron
```bash
# 早间推送
openclaw cron run 1d709b64-5320-4686-a9be-8a45e5575a3a

# 晚间推送
openclaw cron run a77dbc45-3fa3-485c-9305-736ae36b9f10
```

---

## ✅ 验收清单

- [x] Forex Factory API 可访问
- [x] 数据筛选和格式化正常
- [x] 早间推送 cron 配置完成
- [x] 晚间推送 cron 配置完成
- [x] ai-daily-briefing 集成脚本完成
- [ ] 飞书推送测试成功
- [ ] Telegram 推送测试成功
- [ ] ai-daily-briefing 集成测试成功

**当前进度**: 70% (数据获取和 cron 配置完成，推送待测试)

---

## 🔧 故障排除

### 1. 数据获取失败
```
❌ 获取数据失败：403 Forbidden
```
**解决**: Forex Factory 可能限制了访问，使用备用方案（手动输入模式）

### 2. 推送失败
```
❌ 飞书发送失败：Unknown target "openclaw-news"
```
**解决**: 检查 openclaw.json 中飞书配置，确认 target 正确

### 3. ai-daily-briefing 无输出
```
⚠️ 今日无高重要性经济事件
```
**解决**: 正常，当天确实没有高重要性事件

---

## 📞 相关资源

- **Forex Factory**: https://www.forexfactory.com/calendar
- **技能文档**: `skills/fmp-economic-calendar/README.md`
- **输出目录**: `shared/02_outbox/economic_calendar_*.md`

---

**配置完成时间**: 2026-03-17 17:10 UTC  
**下次检查**: 明日早间推送后验证
