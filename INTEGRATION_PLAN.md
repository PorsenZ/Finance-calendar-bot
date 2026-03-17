# FMP 经济日历集成计划

## 当前状态

### ✅ 已完成
1. **技能文档**: `skills/fmp-economic-calendar/SKILL.md`
2. **数据获取脚本**: `skills/fmp-economic-calendar/scripts/fetch_calendar.py`
3. **API Key 配置**: `K3qZCeQFuSzvgWCxdMklKAenHqtzcJBZ`

### ⚠️ 当前问题
**API Key 是旧账户**，无法访问新版经济日历 API 端点：
- 错误信息：`Legacy Endpoint : This endpoint is only available for legacy users who have valid subscriptions prior August 31, 2025`
- 需要：升级 FMP 账户或注册新账户获取新版 API Key

### 🔧 解决方案

#### 方案 A：升级 FMP 账户（推荐）
1. 访问：https://site.financialmodelingprep.com/developer/docs
2. 注册新账户或升级现有账户
3. 获取新版 API Key（支持 v3/economic_calendar）
4. 更新环境变量 `FMP_API_KEY`

#### 方案 B：使用替代数据源
1. **Investing.com 经济日历** (需要 web scraping)
2. **TradingEconomics API** (免费 2000 次/月)
3. **Alpha Vantage** (免费 500 次/天，有经济数据)

#### 方案 C：临时方案 - 手动输入
1. 使用 `skills/fmp-economic-calendar/scripts/manual_calendar.py` 手动输入今日重点事件
2. 保持推送流程正常运行
3. 等 API 升级后自动切换

---

## 集成架构

```
┌─────────────────────────────────────────────────────────┐
│                   每日简报流程                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ FMP API      │───▶│ 数据获取脚本 │───▶│ 格式转换 │ │
│  │ (经济日历)   │    │ fetch_cal.py │    │ format   │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│                                              │          │
│                                              ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ 飞书推送     │◀───│ 消息发送     │◀───│ 简报合并 │ │
│  │ openclaw-news│    │ message tool │    │          │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│                                              ▲          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ Telegram     │───▶│ news-bot     │───▶│          │ │
│  │ 1909055980   │    │              │    │          │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 推送时间表（北京时间 UTC+8）

| 时间 | 内容 | 渠道 |
|------|------|------|
| 08:00 | 今日经济日历重点 + 明日预告 | 飞书 + Telegram |
| 20:00 | 明日经济日历重点提醒 | 飞书 + Telegram |
| 每日首次对话 | ai-daily-briefing 集成提醒 | 当前会话 |

---

## 重点关注事件

### 🔴 最高优先级（必须推送）
- **FOMC 议息会议** - 美联储利率决议
- **CPI 数据** - 美国消费者物价指数
- **非农就业** - Non-Farm Payrolls
- **GDP 数据** - 国内生产总值
- **央行利率决议** - 美联储、欧央行、中国人民银行等

### 🟡 高优先级（建议推送）
- **零售销售** - Retail Sales
- **ISM/PMI** - 制造业/服务业 PMI
- **PPI** - 生产者物价指数
- **消费者信心** - Consumer Confidence
- **初请失业金** - Initial Jobless Claims

### 🟢 中优先级（可选推送）
- **新屋开工** - Housing Starts
- **营建许可** - Building Permits
- **贸易帐** - Trade Balance
- **工业产出** - Industrial Production

---

## 推送模板

### 早间推送模板（08:00）
```
📊 经济日历简报 | 2026-03-17

📌 今天
━━━━━━━━━━━━━━━━━━
🔴 FOMC 议息会议
⏰ 2026-03-17 22:00 (北京时间)
🌍 🇺🇸
📊 重要性：🔴 High

🔴 美国 CPI (YoY)
⏰ 2026-03-17 20:30 (北京时间)
🌍 🇺🇸
📊 重要性：🔴 High
实际：3.2 | 预期：3.0 | 前值：3.1

📌 明天
━━━━━━━━━━━━━━━━━━
🟡 美国零售销售 (MoM)
⏰ 2026-03-18 20:30 (北京时间)
🌍 🇺🇸
📊 重要性：🟡 Medium

═══════════════════════════
数据来源：Financial Modeling Prep
```

### ai-daily-briefing 集成模板
```
⚠️ **今日经济日历重点提醒**

今天有 **2 个高重要性事件** 需要注意：

1. **20:30** - 美国 CPI 数据（预期 3.0%，前值 3.1%）
2. **22:00** - FOMC 议息会议利率决议

建议关注市场波动风险。
```

---

## 下一步行动

### 立即可做
1. ✅ 技能框架已创建
2. ✅ 数据获取脚本已创建
3. ⏳ 等待 API Key 升级

### API 升级后
1. 测试 API 连接
2. 配置 cron 定时任务（08:00 + 20:00）
3. 集成到 news-aggregator-skill
4. 集成到 ai-daily-briefing

### 配置 cron 任务
```bash
# 编辑 crontab
crontab -e

# 添加任务（北京时间）
0 0 * * * cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/scripts && python3 fetch_calendar.py --days 1 --output /home/ubuntu/.openclaw/workspace/shared/02_outbox/economic_calendar_today.json
0 12 * * * cd /home/ubuntu/.openclaw/workspace/skills/fmp-economic-calendar/scripts && python3 fetch_calendar.py --days 2 --from-date $(date -d "tomorrow" +%Y-%m-%d) --output /home/ubuntu/.openclaw/workspace/shared/02_outbox/economic_calendar_tomorrow.json
```

---

## 测试清单

- [ ] API Key 升级并验证
- [ ] 获取经济日历数据成功
- [ ] 数据格式验证
- [ ] 时间转换（UTC→北京时间）验证
- [ ] 飞书推送测试
- [ ] Telegram 推送测试
- [ ] ai-daily-briefing 集成测试
- [ ] cron 定时任务配置
- [ ] 错误处理和告警

---

## 联系人

如需帮助，请查阅：
- FMP 官方文档：https://site.financialmodelingprep.com/developer/docs
- 技能文档：`skills/fmp-economic-calendar/SKILL.md`
