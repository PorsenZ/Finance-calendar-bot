---
name: finance-calendar
description: "Economic calendar skill that fetches real-time financial events from Forex Factory (traditional finance) and Coindar (crypto). Automatically pushes daily briefings to Feishu and Telegram at 08:00 and 20:00 Beijing time. Integrates with ai-daily-briefing for morning reminders."
---

# Economic Calendar Skill (Forex Factory + Coindar)

Fetch real-time economic events, generate briefings, and push to Feishu + Telegram.

---

## 🎯 When to Use

Use this skill when the user:
- Asks about upcoming economic events (FOMC, CPI, Non-Farm, GDP, etc.)
- Wants daily financial calendar briefings
- Needs crypto events (Bitcoin halving, Ethereum upgrades, ICOs)
- Says: "经济日历", "财经日历", "FOMC", "CPI 数据", "非农"

---

## 🔄 Workflow (3 Steps)

### Step 1: Fetch Economic Calendar

```bash
# Fetch traditional finance events (Forex Factory)
python3 scripts/forex_factory_calendar.py

# Save to file
python3 scripts/forex_factory_calendar.py --output shared/02_outbox/economic_calendar.md

# Fetch crypto events (Coindar, requires API Key)
python3 scripts/coindar_calendar.py --api-key YOUR_KEY

# Merge both sources
python3 scripts/merged_calendar.py --output shared/02_outbox/merged_calendar.md
```

### Step 2: Generate Briefing

The script automatically formats events with:
- Event name (Chinese translation)
- Beijing time (UTC+8 conversion)
- Country flag emoji
- Importance level (🔴 High, 🟡 Medium, 🟢 Low)
- Forecast, previous, actual values

### Step 3: Push to Channels

```bash
# Morning briefing (08:00 Beijing time)
python3 scripts/send_push.py --type morning --channels feishu,telegram

# Evening briefing (20:00 Beijing time)
python3 scripts/send_push.py --type evening --channels feishu,telegram

# Test locally
python3 scripts/send_push.py --type morning --channels local --test
```

---

## 📅 Scheduled Pushes (Cron)

| Time (Beijing) | Content | Channels |
|----------------|---------|----------|
| 08:00 | Morning briefing (today's events + tomorrow preview) | Feishu + Telegram |
| 20:00 | Evening briefing (tomorrow's key events) | Feishu + Telegram |

---

## 🤖 ai-daily-briefing Integration

Automatically triggered in the first conversation of each day:

```python
# In ai-daily-briefing workflow
python3 scripts/daily_briefing_integration.py
```

**Output example**:
```
⚠️ **今日经济日历重点提醒**

今天有 **2 个高重要性事件** 需要注意：

1. **20:30** - 美国 CPI (YoY) 🇺🇸 (预期：3.0%, 前值：3.1%)
2. **22:00** - FOMC 议息会议 🇺🇸

建议关注市场波动风险。
```

---

## 📊 Data Sources

### 1. Forex Factory (Traditional Finance) ✅

- **URL**: `https://nfs.faireconomy.media/ff_calendar_thisweek.json`
- **Auth**: None required (free public API)
- **Coverage**:
  - 🔴 Central bank rate decisions (FOMC, ECB, RBA, etc.)
  - 🔴 CPI/PPI inflation data
  - 🔴 Non-Farm Payrolls, Unemployment
  - 🔴 GDP reports
  - 🟡 PMI, Retail Sales
  - 🟡 Trade Balance, Industrial Production

### 2. Coindar (Crypto Events) ⏳

- **URL**: `https://coindar.org/zh-cn/api`
- **Auth**: API Key required (apply at coindar.org)
- **Coverage**:
  - 🔴 Bitcoin halving
  - 🔴 Ethereum upgrades/hard forks
  - 🔴 Major ICOs/IDOs
  - 🟡 Token unlocks
  - 🟡 Airdrops
  - 🟡 Exchange listings

---

## ⚙️ Configuration

### 1. Copy config template

```bash
cd /home/ubuntu/.openclaw/workspace/skills/finance-calendar/
cp .env.example .env
```

### 2. Edit .env file

```bash
# .env (NEVER commit to Git!)

# Forex Factory (no key needed)
FOREX_FACTORY_URL=https://nfs.faireconomy.media/ff_calendar_thisweek.json

# Coindar (apply for API key)
COINDAR_API_KEY=your_api_key_here

# Push channels
FEISHU_CHANNEL=feishu
FEISHU_TARGET=your_feishu_target

TELEGRAM_CHANNEL=telegram
TELEGRAM_TARGET=your_telegram_id

# Timezone
TIMEZONE=Asia/Shanghai
```

---

## 🧪 Testing

```bash
# Test data fetch
python3 scripts/forex_factory_calendar.py --output test_calendar.md

# Test ai-daily-briefing integration
python3 scripts/daily_briefing_integration.py

# Test push (local mode)
python3 scripts/send_push.py --type morning --channels local --test
```

---

## 🔒 Security Rules

### NEVER Upload

- ❌ `.env` file (contains real API keys)
- ❌ `upload-to-github.sh` (contains SSH key paths)
- ❌ Any file with real credentials

### ALWAYS Check

- ✅ `.gitignore` includes all sensitive patterns
- ✅ Upload script excludes sensitive files
- ✅ Use only the dedicated upload script

**See**: [REPOSITORY_SECURITY_RULES.md](REPOSITORY_SECURITY_RULES.md)

---

## 📁 File Structure

```
finance-calendar/
├── scripts/
│   ├── forex_factory_calendar.py   # Main script (Forex Factory)
│   ├── coindar_calendar.py         # Coindar integration
│   ├── send_push.py                # Push to Feishu + Telegram
│   └── daily_briefing_integration.py  # ai-daily-briefing hook
├── .env.example                    # Config template (public)
├── .env                            # Real config (NEVER commit)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
└── SKILL.md                        # This file
```

---

## 🔗 Related Links

- **Public Repo**: https://github.com/PorsenZ/Finance-calendar-bot
- **Forex Factory**: https://www.forexfactory.com/calendar
- **Coindar**: https://coindar.org/
- **Security Rules**: [REPOSITORY_SECURITY_RULES.md](REPOSITORY_SECURITY_RULES.md)

---

**Last Updated**: 2026-03-17 18:07 UTC  
**Status**: ✅ Ready for use (Forex Factory), ⏳ Coindar pending API key
