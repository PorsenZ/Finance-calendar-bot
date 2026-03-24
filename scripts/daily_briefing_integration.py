#!/usr/bin/env python3
"""
ai-daily-briefing 经济日历集成
在每日首次对话时，自动获取并展示今日重要经济事件（传统金融 + 加密货币）
"""

import json
import requests
import os
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置
FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
COINMARKETCAL_API_KEY = os.getenv("COINMARKETCAL_API_KEY", "")

# 重要性过滤（只关注高重要性）
IMPACT_FILTER = {"High"}

# 重点关注国家
COUNTRY_FILTER = {"USD", "EUR", "GBP", "JPY", "CNY", "AUD", "CAD", "NZD", "CHF"}

# 关键事件关键词
KEY_EVENTS = [
    "Interest Rate", "Rate Decision", "FOMC", "CPI", "Core CPI",
    "Non-Farm", "Unemployment", "GDP", "Retail Sales", "PMI",
    "PPI", "Trade Balance", "Industrial Production",
    "Press Conference", "Rate Statement", "Cash Rate"
]


def fetch_calendar() -> List[Dict[str, Any]]:
    """获取经济日历数据"""
    try:
        response = requests.get(FOREX_FACTORY_URL, timeout=15)
        response.raise_for_status()
        return response.json()
    except:
        return []


def filter_today_events(events: List[Dict]) -> List[Dict]:
    """筛选今日高重要性事件"""
    today = datetime.now().strftime("%Y-%m-%d")
    filtered = []
    
    for event in events:
        date_str = event.get("date", "")
        if not date_str.startswith(today):
            continue
        
        impact = event.get("impact", "")
        if impact not in IMPACT_FILTER:
            continue
        
        country = event.get("country", "")
        if country and country not in COUNTRY_FILTER:
            continue
        
        filtered.append(event)
    
    return filtered


def format_briefing_message(events: List[Dict]) -> str:
    """格式化 ai-daily-briefing 消息"""
    if not events:
        return "⚠️ 今日无高重要性经济事件"
    
    lines = []
    lines.append("⚠️ **今日经济日历重点提醒**")
    lines.append("")
    lines.append(f"今天有 **{len(events)} 个高重要性事件** 需要注意：")
    lines.append("")
    
    # 按时间排序
    sorted_events = sorted(events, key=lambda x: x.get("date", ""))
    
    for i, event in enumerate(sorted_events, 1):
        title = event.get("title", "未知事件")
        date_str = event.get("date", "")
        
        # 解析时间（简单处理）
        try:
            if len(date_str) >= 16:
                time_part = date_str[11:16]
                # 转换为北京时间（+8 小时）
                hour = int(time_part[:2]) + 8
                if hour >= 24:
                    hour -= 24
                time_beijing = f"{hour:02d}:{time_part[3:5]}"
            else:
                time_beijing = "未知时间"
        except:
            time_beijing = "未知时间"
        
        country = event.get("country", "")
        country_emoji = {
            "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵",
            "CNY": "🇨🇳", "AUD": "🇦🇺", "CAD": "🇨🇦", "NZD": "🇳🇿", "CHF": "🇨🇭"
        }.get(country, "")
        
        forecast = event.get("forecast", "")
        previous = event.get("previous", "")
        
        line = f"{i}. **{time_beijing}** - {title} {country_emoji}"
        if forecast or previous:
            details = []
            if forecast:
                details.append(f"预期：{forecast}")
            if previous:
                details.append(f"前值：{previous}")
            line += f" ({', '.join(details)})"
        
        lines.append(line)
    
    lines.append("")
    lines.append("建议关注市场波动风险。")
    
    return "\n".join(lines)


def get_crypto_events() -> List[Dict]:
    """获取加密货币事件（调用 CoinMarketCal 脚本）"""
    if not COINMARKETCAL_API_KEY:
        return []
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "coinmarketcal_calendar.py")
        
        # 运行脚本获取今日事件
        result = subprocess.run(
            ["python3", script_path, "--days", "1", "--high-only", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            events = json.loads(result.stdout)
            return events
        return []
    except Exception as e:
        print(f"⚠️ 获取加密货币事件失败：{e}")
        return []

def main():
    """主函数"""
    print("=" * 60)
    print("📊 每日经济日历提醒（传统金融 + 加密货币）")
    print("=" * 60)
    print("")
    
    # 获取传统金融数据
    print("📈 获取传统金融事件...")
    raw_events = fetch_calendar()
    traditional_events = filter_today_events(raw_events) if raw_events else []
    print(f"✅ 获取到 {len(traditional_events)} 个传统金融事件")
    
    # 获取加密货币数据
    print("🪙 获取加密货币事件...")
    crypto_events = get_crypto_events()
    print(f"✅ 获取到 {len(crypto_events)} 个加密货币事件")
    
    print("")
    
    # 格式化消息
    if traditional_events or crypto_events:
        message = format_briefing_message(traditional_events + crypto_events)
        print(message)
    else:
        print("⚠️ 今日无高重要性经济事件")
    
    print("")
    print("=" * 60)


if __name__ == "__main__":
    main()
