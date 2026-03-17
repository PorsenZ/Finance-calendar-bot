# 经济日历技能

Forex Factory + Coindar 经济日历技能 - 自动获取并推送传统金融和币圈重要事件。

## 📊 功能

- ✅ Forex Factory 经济日历（传统金融）
- ⏳ Coindar 事件日历（币圈，需要 API Key）
- ✅ 定时推送（飞书 + Telegram）
- ✅ ai-daily-briefing 集成

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# Coindar API Key: 在 https://coindar.org/zh-cn/api 申请
```

### 3. 运行脚本

```bash
# 获取经济日历
python3 scripts/forex_factory_calendar.py

# 保存到文件
python3 scripts/forex_factory_calendar.py --output economic_calendar.md
```

## 📁 文件说明

```
fmp-economic-calendar/
├── scripts/
│   ├── forex_factory_calendar.py  # 主脚本
│   ├── send_push.py               # 推送脚本
│   └── daily_briefing_integration.py  # ai-daily-briefing 集成
├── .env.example          # 配置示例（可公开）
├── .env                  # 真实配置（禁止公开）
├── .gitignore           # Git 忽略文件
├── requirements.txt     # Python 依赖
├── README.md           # 使用说明
└── SECURITY_ISOLATION.md # 安全隔离说明
```

## ⚠️ 安全警告

**重要**: `.env` 文件包含敏感信息，已添加到 `.gitignore`，切勿手动上传到 GitHub！

详细安全说明请查看：[SECURITY_ISOLATION.md](SECURITY_ISOLATION.md)

## 📅 推送时间

- **早间推送**: 北京时间 08:00
- **晚间推送**: 北京时间 20:00

## 🔗 相关链接

- 公开仓库：https://github.com/PorsenZ/Finance-calendar-bot
- Forex Factory: https://www.forexfactory.com/calendar
- Coindar: https://coindar.org/

## 📝 License

MIT
