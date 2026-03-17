# 经济日历技能 - 升级版（传统金融 + 币圈）

**创建时间**: 2026-03-17 17:15 UTC (北京时间 2026-03-18 01:15)  
**状态**: ⏳ 等待 Coindar API Key

---

## 📊 数据源

### 1. 传统金融
- **Forex Factory**: `https://nfs.faireconomy.media/ff_calendar_thisweek.json`
- 特点：官方数据、实时更新、免费无需 API Key
- 覆盖：GDP、CPI、利率决议、非农就业等

### 2. 币圈事件 (待集成)
- **Coindar**: `https://coindar.org/zh-cn/api`
- 特点：加密货币事件、ICO、空投、减半、硬分叉等
- 状态: ⏳ 等待 API Key 审核

---

## 🎯 覆盖事件类型

### 传统金融
- 🔴 央行利率决议 (FOMC、ECB、RBA 等)
- 🔴 CPI/PPI 通胀数据
- 🔴 非农就业、失业率
- 🔴 GDP 数据
- 🟡 PMI、零售销售
- 🟡 贸易帐、工业产出

### 币圈事件
- 🔴 比特币减半
- 🔴 以太坊升级/硬分叉
- 🔴 重大 ICO/IDO
- 🟡 代币解锁
- 🟡 空投活动
- 🟡 交易所上线
- 🟡 项目发布会

---

## 📁 脚本清单

```
skills/fmp-economic-calendar/scripts/
├── forex_factory_calendar.py       # 传统金融日历 (✅ 已完成)
├── coindar_calendar.py             # 币圈日历 (⏳ 等待 API Key)
├── merged_calendar.py              # 合并两个数据源 (待创建)
├── send_push.py                    # 推送脚本 (✅ 已完成)
└── daily_briefing_integration.py   # ai-daily-briefing 集成 (✅ 已完成)
```

---

## 🚀 使用方法

### 1. 仅传统金融
```bash
python3 skills/fmp-economic-calendar/scripts/forex_factory_calendar.py \
  --output shared/02_outbox/economic_calendar.md
```

### 2. 仅币圈 (需要 API Key)
```bash
python3 skills/fmp-economic-calendar/scripts/coindar_calendar.py \
  --api-key YOUR_COINDAR_KEY \
  --output shared/02_outbox/crypto_calendar.md
```

### 3. 合并模式 (需要 API Key)
```bash
python3 skills/fmp-economic-calendar/scripts/merged_calendar.py \
  --coindar-key YOUR_COINDAR_KEY \
  --output shared/02_outbox/merged_calendar.md
```

---

## 📅 推送时间（北京时间 UTC+8）

| 时间 | 内容 | 渠道 |
|------|------|------|
| 08:00 | 传统金融 + 币圈今日重点 | 飞书 + Telegram |
| 20:00 | 明日事件提醒 | 飞书 + Telegram |

---

## ⏳ 下一步

1. **填写 Coindar API 申请**:
   - URL: `https://github.com/win4r/OpenClaw`
   - 等待审核（通常 12 小时内）

2. **获取 API Key 后**:
   - 更新环境变量 `COINDAR_API_KEY`
   - 测试 Coindar API 连接
   - 创建合并脚本
   - 更新推送模板

3. **验证推送**:
   - 测试飞书推送
   - 测试 Telegram 推送
   - 验证 ai-daily-briefing 集成

---

## 📝 Coindar API 端点（预期）

根据搜索结果，Coindar API 可能包含以下端点：

```
GET /api/events
参数:
- from: 开始日期 (YYYY-MM-DD)
- to: 结束日期
- coins: 币种列表 (可选，如 BTC,ETH)
- tags: 事件类型 (可选，如 halving,airdrop,ico)

响应示例:
[
  {
    "id": "12345",
    "coin": "BTC",
    "title": "Bitcoin Halving",
    "date": "2026-03-20",
    "time": "12:00",
    "tag": "halving",
    "impact": "high"
  }
]
```

---

## 🔧 配置

### 环境变量
```bash
export COINDAR_API_KEY="your_api_key_here"
```

### openclaw.json
无需修改，使用现有推送配置

---

## 📞 相关资源

- **Coindar API 申请**: https://coindar.org/zh-cn/api
- **Coindar 官网**: https://coindar.org/
- **Forex Factory**: https://www.forexfactory.com/calendar
- **技能文档**: `skills/fmp-economic-calendar/README.md`

---

**更新时间**: 2026-03-17 17:15 UTC  
**下次更新**: 获取 Coindar API Key 后
