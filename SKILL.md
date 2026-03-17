# 经济日历技能

## 概述
使用 **Forex Factory**（传统金融）+ **Coindar**（币圈）API 获取全球重要经济事件日历，包括：
- FOMC 议息会议
- CPI/PPI 通胀数据
- 非农就业报告
- GDP 数据
- 央行利率决议
- 比特币减半、以太坊升级等币圈事件

## API 配置
- **API Provider**: Financial Modeling Prep
- **API Key**: `K3qZCeQFuSzvgWCxdMklKAenHqtzcJBZ`
- **环境变量**: `FMP_API_KEY`
- **基础 URL**: `https://financialmodelingprep.com/api/v3/`

## API 端点

### 经济日历
```
GET /api/v3/economic_calendar
参数:
- from: YYYY-MM-DD (开始日期)
- to: YYYY-MM-DD (结束日期)
- apikey: YOUR_API_KEY

响应示例:
[
  {
    "symbol": "CPI",
    "actual": 3.2,
    "previous": 3.1,
    "change": 0.1,
    "changePercentage": 3.23,
    "name": "Consumer Price Index (YoY)",
    "date": "2026-03-20",
    "time": "13:30",
    "country": "US",
    "consensus": 3.0,
    "revised": null,
    "importance": "High",
    "currency": "USD"
  }
]
```

## 重要性级别
- **High**: 市场重大影响事件（FOMC、CPI、非农、GDP）
- **Medium**: 中等影响事件（零售销售、工业产出）
- **Low**: 轻微影响事件

## 脚本功能

### 1. fetch_calendar.py
获取指定日期范围的经济日历数据

### 2. filter_events.py
筛选高重要性事件（FOMC、CPI、非农等）

### 3. format_briefing.py
格式化为飞书/Telegram 推送格式

### 4. daily_reminder.py
每日简报集成（ai-daily-briefing）

## 推送时间
- **早间推送**: 北京时间 08:00（今日日历 + 明日预告）
- **晚间推送**: 北京时间 20:00（明日日历重点提醒）

## 推送渠道
- **飞书**: openclaw-news
- **Telegram**: 1909055980 (newsbot)

## 重点关注事件关键词
```python
KEY_EVENTS = [
    "FOMC", "Federal Open Market Committee", "Interest Rate Decision",
    "CPI", "Consumer Price Index", "Inflation",
    "Non-Farm Payrolls", "NFP", "Unemployment Rate",
    "GDP", "Gross Domestic Product",
    "Retail Sales", "ISM", "PMI",
    "Fed Chair Powell", "ECB", "PBOC",
    "Central Bank", "Rate Decision"
]
```

## 时区处理
- FMP API 返回时间：UTC
- 输出时间：北京时间 (UTC+8)
- 转换公式：`beijing_time = utc_time + 8 hours`

## 验证流程
1. API 调用成功验证
2. 数据完整性检查（至少包含今日事件）
3. 时间转换验证
4. 推送前格式检查
