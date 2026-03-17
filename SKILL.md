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
- **数据源 1**: Forex Factory（无需 API Key，直接访问）
- **数据源 2**: Coindar（需要 API Key，审核中）
- **环境变量**: 通过 .env 文件配置

## 使用说明

详见：[README.md](README.md)

## 安全说明

- .env 文件包含真实 API Key，绝对不能公开
- 上传脚本包含 SSH 密钥路径，绝对不能公开
- 详见：[REPOSITORY_SECURITY_RULES.md](REPOSITORY_SECURITY_RULES.md)
