#!/usr/bin/env python3
"""
ai-daily-briefing 经济日历集成
在每日首次对话时，自动获取并展示今日重要经济事件
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置
FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

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


def main():
    """主函数"""
    # 获取数据
    raw_events = fetch_calendar()
    if not raw_events:
        print("⚠️ 无法获取经济日历数据")
        return
    
    # 筛选今日事件
    today_events = filter_today_events(raw_events)
    
    if not today_events:
        print("⚠️ 今日无高重要性经济事件")
        return
    
    # 格式化消息
    message = format_briefing_message(today_events)
    print(message)


if __name__ == "__main__":
    main()
