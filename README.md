# 经济日历技能

## 📊 概述

使用 Forex Factory + Coindar API 获取全球重要经济事件日历（传统金融 + 币圈），并自动推送到飞书和 Telegram。

**公开仓库**: https://github.com/PorsenZ/Finance-calendar-bot  
**注意**: 此技能为公开项目，不包含任何敏感信息。API Key 请通过 .env 文件配置。

## 🎯 功能

- **经济日历查询**: 获取 FOMC、CPI、非农、GDP 等重要经济事件
- **定时推送**: 每日 08:00 和 20:00（北京时间）自动推送
- **每日简报集成**: 在 ai-daily-briefing 中提醒今日重点事件
- **多渠推送**: 飞书 (openclaw-news) + Telegram (1909055980)

## 📁 文件结构

```
skills/fmp-economic-calendar/
├── SKILL.md                    # 技能文档
├── INTEGRATION_PLAN.md         # 集成计划
├── README.md                   # 本文件
└── scripts/
    ├── fetch_calendar.py       # FMP API 数据获取脚本
    ├── manual_calendar.py      # 手动输入脚本（临时方案）
    └── send_push.py            # 推送脚本（待创建）
```

## ⚙️ 配置

### 环境变量
```bash
export FMP_API_KEY="K3qZCeQFuSzvgWCxdMklKAenHqtzcJBZ"
```

### API 端点
- **基础 URL**: `https://financialmodelingprep.com/api/v3/`
- **经济日历**: `/economic_calendar`
- **参数**: `from`, `to`, `apikey`

## 🚀 使用方法

### 1. 获取经济日历数据
```bash
# 获取未来 7 天数据
python3 skills/fmp-economic-calendar/scripts/fetch_calendar.py --days 7

# 获取指定日期范围
python3 skills/fmp-economic-calendar/scripts/fetch_calendar.py --from-date 2026-03-17 --to-date 2026-03-24

# 保存为 JSON
python3 skills/fmp-economic-calendar/scripts/fetch_calendar.py --days 7 --output shared/02_outbox/economic_calendar.json --format json

# 保存为文本简报
python3 skills/fmp-economic-calendar/scripts/fetch_calendar.py --days 7 --output shared/02_outbox/economic_calendar_briefing.md
```

### 2. 手动输入模式（API 升级前）
```bash
# 生成今日简报
python3 skills/fmp-economic-calendar/scripts/manual_calendar.py --date 2026-03-17

# 保存到文件
python3 skills/fmp-economic-calendar/scripts/manual_calendar.py --output shared/02_outbox/economic_calendar_manual.md
```

### 3. 推送到飞书和 Telegram
```bash
# 待创建 send_push.py 脚本
python3 skills/fmp-economic-calendar/scripts/send_push.py --input shared/02_outbox/economic_calendar_briefing.md
```

## 📅 推送时间（北京时间 UTC+8）

| 时间 | 内容 | 渠道 |
|------|------|------|
| 08:00 | 今日经济日历重点 + 明日预告 | 飞书 + Telegram |
| 20:00 | 明日经济日历重点提醒 | 飞书 + Telegram |

## 🔴 重点关注事件

### 最高优先级
- FOMC 议息会议（美联储利率决议）
- CPI 数据（美国消费者物价指数）
- 非农就业（Non-Farm Payrolls）
- GDP 数据
- 央行利率决议（美联储、欧央行、中国人民银行）

### 高优先级
- 零售销售（Retail Sales）
- ISM/PMI（制造业/服务业 PMI）
- PPI（生产者物价指数）
- 消费者信心指数
- 初请失业金人数

## ⚠️ 当前状态

### ✅ 已完成
- [x] 技能文档创建
- [x] 数据获取脚本创建
- [x] 手动输入脚本创建
- [x] 推送格式模板设计

### ⏳ 进行中
- [ ] FMP API Key 升级（当前为旧账户，无法访问经济日历 API）
- [ ] 推送脚本创建
- [ ] cron 定时任务配置
- [ ] ai-daily-briefing 集成

### 📋 下一步
1. **升级 FMP 账户** - 访问 https://site.financialmodelingprep.com/register 注册新账户
2. **更新 API Key** - 将新 API Key 更新到环境变量
3. **测试 API 连接** - 运行 `fetch_calendar.py` 验证
4. **配置定时任务** - 设置 cron 任务（08:00 + 20:00）
5. **集成推送流程** - 与 news-aggregator-skill 合并

## 📝 示例输出

```
📊 经济日历简报 | 2026-03-17
========================================

📌 今天
------------------------------

🔴 FOMC 议息会议
⏰ 2026-03-17 22:00 (北京时间)
🌍 🇺🇸
📊 重要性：🔴 High

🔴 美国 CPI (YoY)
⏰ 2026-03-17 20:30 (北京时间)
🌍 🇺🇸
📊 重要性：🔴 High
实际：3.2 | 预期：3.0 | 前值：3.1

========================================
数据来源：Financial Modeling Prep
```

## 🔧 故障排除

### API Key 无效
```
Error Message: Invalid API KEY
```
**解决**: 检查环境变量 `FMP_API_KEY` 是否正确设置

### 旧版 API 端点错误
```
Error Message: Legacy Endpoint : This endpoint is only available for legacy users
```
**解决**: 需要升级 FMP 账户或注册新账户获取新版 API Key

### 时区错误
**解决**: 脚本自动将 UTC 时间转换为北京时间（UTC+8），检查系统时区设置

## 📚 相关文档

- [集成计划](INTEGRATION_PLAN.md) - 详细集成方案
- [技能文档](SKILL.md) - API 配置和使用说明
- [FMP 官方文档](https://site.financialmodelingprep.com/developer/docs)

## 📞 联系

如有问题，请查阅文档或联系管理员。
