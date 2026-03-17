# 经济日历技能

## 📊 概述

使用 **Forex Factory**（传统金融）+ **Coindar**（币圈）API 获取全球重要经济事件日历，并自动推送到飞书和 Telegram。

**公开仓库**: https://github.com/PorsenZ/Finance-calendar-bot

---

## ⚠️ 安全警告

**上传到此仓库只能使用专用脚本**：

```bash
/home/ubuntu/.openclaw/workspace/skills/finance-calendar/upload-to-github.sh
```

**绝对禁止**：
- ❌ 手动 `git push` 到 Finance-calendar-bot
- ❌ 复制整个 skills 目录
- ❌ 修改脚本中的仓库 URL
- ❌ 上传 upload-to-github.sh 本身（包含敏感信息）

详见：[REPOSITORY_SECURITY_RULES.md](REPOSITORY_SECURITY_RULES.md)

---

**注意**: 此技能为公开项目，不包含任何敏感信息。API Key 请通过 .env 文件配置。

## 🎯 功能

- ✅ **Forex Factory 经济日历**: 获取 FOMC、CPI、非农、GDP 等传统金融事件
- ⏳ **Coindar 币圈事件**: 获取比特币减半、以太坊升级、ICO 等币圈事件（需要 API Key）
- ✅ **定时推送**: 每日 08:00 和 20:00（北京时间）自动推送
- ✅ **每日简报集成**: 在 ai-daily-briefing 中提醒今日重点事件
- ✅ **多渠道推送**: 飞书 + Telegram（在你的 `openclaw.json` 中配置）

## 📁 文件结构

```
finance-calendar/
├── scripts/
│   ├── forex_factory_calendar.py   # Forex Factory 数据获取（✅ 已完成）
│   ├── coindar_calendar.py         # Coindar 数据获取（⏳ 待创建）
│   ├── send_push.py                # 推送脚本（✅ 已完成）
│   └── daily_briefing_integration.py  # ai-daily-briefing 集成（✅ 已完成）
├── .env.example                    # 配置示例（可公开）
├── .env                            # 真实配置（禁止公开）
├── .gitignore                      # Git 忽略规则
├── requirements.txt                # Python 依赖
├── README.md                       # 使用说明
├── SECURITY_ISOLATION.md           # 安全隔离说明
├── REPOSITORY_SECURITY_RULES.md    # 仓库安全规则
└── SECURITY_LESSON_LEARNED.md      # 安全教训记录
```

## ⚙️ 配置

### 1. 复制配置文件

```bash
cd /home/ubuntu/.openclaw/workspace/skills/finance-calendar/
cp .env.example .env
```

### 2. 编辑 .env 文件

```bash
# .env 文件（禁止上传到 GitHub）

# Forex Factory API (无需 Key，直接访问)
FOREX_FACTORY_URL=https://nfs.faireconomy.media/ff_calendar_thisweek.json

# Coindar API (币圈事件)
# ⚠️ 审核通过后填写，切勿上传到 GitHub
COINDAR_API_KEY=your_api_key_here

# 推送配置
FEISHU_CHANNEL=feishu
FEISHU_TARGET=your_feishu_target

TELEGRAM_CHANNEL=telegram
TELEGRAM_TARGET=your_telegram_target

# 时区配置
TIMEZONE=Asia/Shanghai
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取经济日历

```bash
# 获取传统金融日历
python3 scripts/forex_factory_calendar.py

# 保存到文件
python3 scripts/forex_factory_calendar.py --output economic_calendar.md
```

### 3. 测试推送

```bash
# 测试本地模式
python3 scripts/send_push.py --type morning --channels local --test
```

## 📅 推送时间（北京时间 UTC+8）

| 时间 | 内容 | 渠道 |
|------|------|------|
| 08:00 | 早间财经日历（今日重点 + 明日预告） | 飞书 + Telegram |
| 20:00 | 晚间财经日历（明日重点） | 飞书 + Telegram |

## 🔐 安全说明

### 敏感信息保护

- ✅ `.env` 文件包含真实 API Key，**绝对不能上传**
- ✅ `upload-to-github.sh` 包含 SSH 密钥路径，**绝对不能上传**
- ✅ `.gitignore` 已配置，自动排除敏感文件
- ✅ 上传脚本会自动检查敏感文件

### 仓库隔离

| 仓库 | 用途 | 可见性 |
|------|------|--------|
| **Finance-calendar-bot** | 公开技能 | Public |
| **myOpenClaw** | 私有备份 | Private |
| **ubuntu-openClaw** | workspace | Private |

**绝对不能混淆！** 详见：[REPOSITORY_SECURITY_RULES.md](REPOSITORY_SECURITY_RULES.md)

## 📊 数据源

### 1. Forex Factory（传统金融）

- **URL**: `https://nfs.faireconomy.media/ff_calendar_thisweek.json`
- **特点**: 
  - ✅ 官方数据源，准确可靠
  - ✅ 实时更新
  - ✅ 免费无需 API Key
  - ✅ 包含高/中/低重要性标记

- **覆盖事件**:
  - 🔴 央行利率决议（FOMC、ECB、RBA 等）
  - 🔴 CPI/PPI 通胀数据
  - 🔴 非农就业、失业率
  - 🔴 GDP 数据
  - 🟡 PMI、零售销售
  - 🟡 贸易帐、工业产出

### 2. Coindar（币圈事件）⏳

- **URL**: `https://coindar.org/zh-cn/api`
- **特点**: 
  - ⏳ 需要 API Key（申请中）
  - ✅ 加密货币专属事件
  - ✅ 包含 ICO、空投、减半等

- **覆盖事件**:
  - 🔴 比特币减半
  - 🔴 以太坊升级/硬分叉
  - 🔴 重大 ICO/IDO
  - 🟡 代币解锁
  - 🟡 空投活动
  - 🟡 交易所上线

## 🧪 测试

```bash
# 测试数据获取
python3 scripts/forex_factory_calendar.py --output test_calendar.md

# 测试 ai-daily-briefing 集成
python3 scripts/daily_briefing_integration.py

# 测试推送（本地模式）
python3 scripts/send_push.py --type morning --channels local --test
```

## 🔗 相关链接

- **公开仓库**: https://github.com/PorsenZ/Finance-calendar-bot
- **Forex Factory**: https://www.forexfactory.com/calendar
- **Coindar**: https://coindar.org/
- **安全规则**: [REPOSITORY_SECURITY_RULES.md](REPOSITORY_SECURITY_RULES.md)

## 📝 License

MIT

---

**最后更新**: 2026-03-17 17:55 UTC  
**状态**: ✅ 文档已更新，反映当前 Forex Factory + Coindar 方案
