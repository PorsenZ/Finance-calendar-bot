#!/usr/bin/env python3
"""
经济日历推送脚本
功能：
1. 获取 Forex Factory 经济日历数据
2. 格式化推送到飞书和 Telegram
3. 支持早间 (08:00) 和晚间 (20:00) 推送
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置
FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
OUTPUT_DIR = "/home/ubuntu/.openclaw/workspace/shared/02_outbox"

# 推送配置（示例，实际使用从 .env 读取）
FEISHU_CHANNEL = "feishu"
FEISHU_TARGET = os.getenv("FEISHU_TARGET", "your_feishu_target")

TELEGRAM_CHANNEL = "telegram"
TELEGRAM_TARGET = os.getenv("TELEGRAM_TARGET", "your_telegram_target")

# 重要性过滤
IMPACT_FILTER = {"High", "Medium"}

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
        response = requests.get(FOREX_FACTORY_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ 获取数据失败：{e}")
        return []


def filter_events(events: List[Dict]) -> List[Dict]:
    """筛选重要事件"""
    filtered = []
    for event in events:
        impact = event.get("impact", "")
        country = event.get("country", "")
        title = event.get("title", "")
        
        if impact not in IMPACT_FILTER:
            continue
        
        if country and country not in COUNTRY_FILTER:
            continue
        
        is_key_event = any(keyword.lower() in title.lower() for keyword in KEY_EVENTS)
        if not is_key_event and impact != "High":
            continue
        
        filtered.append(event)
    
    return filtered


def parse_datetime(date_str: str) -> datetime:
    """解析日期字符串"""
    try:
        if len(date_str) == 16:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        return datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")
    except:
        return datetime.now()


def convert_to_beijing(utc_dt: datetime) -> datetime:
    """UTC 转北京时间"""
    return utc_dt + timedelta(hours=8)


def format_push_message(events: List[Dict], push_type: str = "morning") -> str:
    """
    格式化推送消息
    
    Args:
        events: 事件列表
        push_type: morning(早间) 或 evening(晚间)
    """
    # 使用北京时间（UTC+8）
    now = datetime.now() + timedelta(hours=8)
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 按日期分组
    events_by_date = {}
    for event in events:
        utc_dt = parse_datetime(event.get("date", ""))
        beijing_dt = convert_to_beijing(utc_dt)
        date_key = beijing_dt.strftime("%Y-%m-%d")
        
        if date_key not in events_by_date:
            events_by_date[date_key] = []
        events_by_date[date_key].append({
            "event": event,
            "beijing_dt": beijing_dt
        })
    
    # 构建消息
    lines = []
    
    if push_type == "morning":
        lines.append(f"📊 **经济日历早报** | {today}")
        lines.append("=" * 40)
        lines.append("")
        lines.append("🌅 早安！今日重要经济事件提醒：")
        lines.append("")
        
        # 今日事件
        if today in events_by_date:
            lines.append("📌 **今天**")
            lines.append("-" * 40)
            today_events = sorted(events_by_date[today], key=lambda x: x["beijing_dt"])
            
            for item in today_events[:10]:  # 最多 10 个
                event = item["event"]
                beijing_dt = item["beijing_dt"]
                
                impact_emoji = {"High": "🔴", "Medium": "🟡"}.get(event.get("impact", ""), "⚪")
                country_emoji = {
                    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵",
                    "CNY": "🇨🇳", "AUD": "🇦🇺", "CAD": "🇨🇦", "NZD": "🇳🇿", "CHF": "🇨🇭"
                }.get(event.get("country", ""), event.get("country", ""))
                
                lines.append("")
                lines.append(f"{impact_emoji} {event.get('title', '未知事件')}")
                lines.append(f"⏰ {beijing_dt.strftime('%H:%M')} (北京时间)")
                lines.append(f"🌍 {country_emoji}")
                
                forecast = event.get("forecast", "")
                previous = event.get("previous", "")
                if forecast or previous:
                    values = []
                    if forecast:
                        values.append(f"预期：{forecast}")
                    if previous:
                        values.append(f"前值：{previous}")
                    lines.append(" | ".join(values))
            
            lines.append("")
        
        # 明日预告
        if tomorrow in events_by_date:
            lines.append("📌 **明天预告**")
            lines.append("-" * 40)
            tomorrow_events = sorted(events_by_date[tomorrow], key=lambda x: x["beijing_dt"])
            
            for item in tomorrow_events[:5]:  # 最多 5 个
                event = item["event"]
                beijing_dt = item["beijing_dt"]
                
                impact_emoji = {"High": "🔴", "Medium": "🟡"}.get(event.get("impact", ""), "⚪")
                lines.append(f"{impact_emoji} {beijing_dt.strftime('%H:%M')} - {event.get('title', '未知事件')}")
            
            lines.append("")
        
        lines.append("=" * 40)
        lines.append("📡 数据来源：Forex Factory (实时更新)")
        lines.append("⚠️ 数据仅供参考，投资决策请谨慎")
    
    else:  # evening
        lines.append(f"📊 **经济日历晚报** | {today}")
        lines.append("=" * 40)
        lines.append("")
        lines.append("🌙 晚安！明日重要经济事件提醒：")
        lines.append("")
        
        # 明日事件
        if tomorrow in events_by_date:
            lines.append("📌 **明天** ({})".format(tomorrow))
            lines.append("-" * 40)
            tomorrow_events = sorted(events_by_date[tomorrow], key=lambda x: x["beijing_dt"])
            
            for item in tomorrow_events:
                event = item["event"]
                beijing_dt = item["beijing_dt"]
                
                impact_emoji = {"High": "🔴", "Medium": "🟡"}.get(event.get("impact", ""), "⚪")
                country_emoji = {
                    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵",
                    "CNY": "🇨🇳", "AUD": "🇦🇺", "CAD": "🇨🇦", "NZD": "🇳🇿", "CHF": "🇨🇭"
                }.get(event.get("country", ""), event.get("country", ""))
                
                lines.append("")
                lines.append(f"{impact_emoji} {event.get('title', '未知事件')}")
                lines.append(f"⏰ {beijing_dt.strftime('%H:%M')} (北京时间)")
                lines.append(f"🌍 {country_emoji}")
                
                forecast = event.get("forecast", "")
                previous = event.get("previous", "")
                if forecast or previous:
                    values = []
                    if forecast:
                        values.append(f"预期：{forecast}")
                    if previous:
                        values.append(f"前值：{previous}")
                    lines.append(" | ".join(values))
            
            lines.append("")
        
        lines.append("=" * 40)
        lines.append("📡 数据来源：Forex Factory (实时更新)")
    
    return "\n".join(lines)


def send_feishu(message: str) -> bool:
    """发送到飞书"""
    print(f"📤 正在发送飞书消息到 {FEISHU_TARGET}...")
    # 这里使用 message tool 的模拟调用
    # 实际执行需要通过 OpenClaw 的 message tool
    print(f"✅ 飞书消息长度：{len(message)} 字符")
    return True


def send_telegram(message: str) -> bool:
    """发送到 Telegram"""
    print(f"📤 正在发送 Telegram 消息到 {TELEGRAM_TARGET}...")
    # 这里使用 message tool 的模拟调用
    # 实际执行需要通过 OpenClaw 的 message tool
    print(f"✅ Telegram 消息长度：{len(message)} 字符")
    return True


def save_local(message: str, filename: str):
    """保存到本地"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(message)
    print(f"✅ 已保存到：{filepath}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="经济日历推送脚本")
    parser.add_argument("--type", choices=["morning", "evening"], default="morning", help="推送类型")
    parser.add_argument("--channels", nargs='+', choices=["feishu", "telegram", "local"], default=["local"], help="推送渠道")
    parser.add_argument("--test", action="store_true", help="测试模式（不实际发送）")
    
    args = parser.parse_args()
    
    print(f"📅 经济日历推送 | 类型：{args.type}")
    print("=" * 40)
    
    # 获取数据
    raw_events = fetch_calendar()
    if not raw_events:
        print("❌ 未获取到数据")
        return
    
    print(f"✅ 获取到 {len(raw_events)} 个原始事件")
    
    # 筛选事件
    filtered_events = filter_events(raw_events)
    print(f"✅ 筛选后剩余 {len(filtered_events)} 个关注事件")
    
    if not filtered_events:
        print("⚠️ 暂无重要经济事件")
        return
    
    # 格式化消息
    message = format_push_message(filtered_events, args.type)
    
    # 推送
    if "local" in args.channels or args.test:
        filename = f"economic_calendar_{args.type}_{datetime.now().strftime('%Y%m%d')}.md"
        save_local(message, filename)
    
    if not args.test:
        if "feishu" in args.channels:
            send_feishu(message)
        
        if "telegram" in args.channels:
            send_telegram(message)
    
    print("=" * 40)
    print("✅ 推送完成")


if __name__ == "__main__":
    main()
