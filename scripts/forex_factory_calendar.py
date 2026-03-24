#!/usr/bin/env python3
"""
经济日历数据获取脚本 - Forex Factory 官方数据源
数据来源：https://nfs.faireconomy.media/ff_calendar_thisweek.json
特点：
- 官方数据源，准确可靠
- 实时更新
- 免费无需 API Key
- 包含高/中/低重要性标记
"""

import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 加载 .env 配置
load_dotenv()

# 配置
FOREX_FACTORY_URL = os.getenv("FOREX_FACTORY_URL", "https://nfs.faireconomy.media/ff_calendar_thisweek.json")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/home/ubuntu/.openclaw/workspace/shared/02_outbox")

# 重要性过滤
IMPACT_FILTER = {"High", "Medium"}  # 只关注高/中重要性事件

# 重点关注国家
COUNTRY_FILTER = {"USD", "EUR", "GBP", "JPY", "CNY", "AUD", "CAD", "NZD", "CHF"}

# 关键事件关键词
KEY_EVENTS = [
    "Interest Rate", "Rate Decision", "FOMC", "CPI", "Core CPI",
    "Non-Farm", "Unemployment", "GDP", "Retail Sales", "PMI",
    "PPI", "Trade Balance", "Industrial Production",
    "Press Conference", "Rate Statement", "Cash Rate"
]


def fetch_forex_factory_calendar() -> List[Dict[str, Any]]:
    """
    获取 Forex Factory 经济日历数据
    
    Returns:
        原始事件列表
    """
    try:
        print(f"📡 正在获取 Forex Factory 数据...")
        response = requests.get(FOREX_FACTORY_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ 获取到 {len(data)} 个原始事件")
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ API 请求失败：{e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        return []


def filter_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    筛选重要事件
    
    Args:
        events: 原始事件列表
    
    Returns:
        筛选后的事件列表
    """
    filtered = []
    
    for event in events:
        impact = event.get("impact", "")
        country = event.get("country", "")
        title = event.get("title", "")
        
        # 按重要性筛选
        if impact not in IMPACT_FILTER:
            continue
        
        # 按国家筛选
        if country and country not in COUNTRY_FILTER:
            continue
        
        # 按关键词筛选（确保关键事件不被遗漏）
        is_key_event = any(keyword.lower() in title.lower() for keyword in KEY_EVENTS)
        if not is_key_event and impact != "High":
            continue
        
        filtered.append(event)
    
    print(f"✅ 筛选后剩余 {len(filtered)} 个关注事件")
    return filtered


def parse_datetime(date_str: str) -> datetime:
    """
    解析 Forex Factory 日期字符串（带时区）
    格式："2026-03-18T08:30:00-04:00" 或 "2026-03-18T08:30-04:00"
    
    Args:
        date_str: 日期字符串
    
    Returns:
        datetime 对象（UTC 时间）
    """
    try:
        from datetime import timedelta
        
        # 处理时区格式 "2026-03-18T08:30:00-04:00"
        if 'T' in date_str and ('+' in date_str or date_str.count('-') > 2):
            # 有秒数：2026-03-18T08:30:00-04:00
            if len(date_str) >= 25:
                dt_part = date_str[:19]  # "2026-03-18T08:30:00"
                tz_part = date_str[19:]  # "-04:00"
                utc_dt = datetime.strptime(dt_part, "%Y-%m-%dT%H:%M:%S")
                # 解析时区偏移并转换为 UTC
                tz_sign = 1 if tz_part[0] == '+' else -1
                tz_hours = int(tz_part[1:3])
                tz_mins = int(tz_part[4:6])
                utc_dt = utc_dt - timedelta(hours=tz_sign*tz_hours, minutes=tz_sign*tz_mins)
                return utc_dt
            # 没有秒数：2026-03-18T08:30-04:00
            elif len(date_str) >= 22:
                dt_part = date_str[:16]  # "2026-03-18T08:30"
                tz_part = date_str[16:]  # "-04:00"
                utc_dt = datetime.strptime(dt_part, "%Y-%m-%dT%H:%M")
                tz_sign = 1 if tz_part[0] == '+' else -1
                tz_hours = int(tz_part[1:3])
                tz_mins = int(tz_part[4:6])
                utc_dt = utc_dt - timedelta(hours=tz_sign*tz_hours, minutes=tz_sign*tz_mins)
                return utc_dt
        
        # 没有时区信息，直接解析
        if len(date_str) >= 19:
            return datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")
        elif len(date_str) >= 16:
            return datetime.strptime(date_str[:16], "%Y-%m-%dT%H:%M")
        
        return datetime.now()
    except Exception as e:
        print(f"⚠️ 日期解析失败：{date_str}, 错误：{e}")
        return datetime.now()


def convert_to_beijing(utc_dt: datetime) -> datetime:
    """
    UTC 时间转换为北京时间
    
    Args:
        utc_dt: UTC 时间
    
    Returns:
        北京时间
    """
    return utc_dt + timedelta(hours=8)


def format_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    格式化单个事件
    
    Args:
        event: 原始事件字典
    
    Returns:
        格式化后的事件字典
    """
    # 解析日期
    utc_dt = parse_datetime(event.get("date", ""))
    beijing_dt = convert_to_beijing(utc_dt)
    
    # 重要性标记
    impact = event.get("impact", "")
    impact_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(impact, "⚪")
    
    # 国家标记
    country = event.get("country", "")
    country_emoji = {
        "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵",
        "CNY": "🇨🇳", "AUD": "🇦🇺", "CAD": "🇨🇦", "NZD": "🇳🇿", "CHF": "🇨🇭"
    }.get(country, country)
    
    return {
        "title": event.get("title", "未知事件"),
        "country": country,
        "country_emoji": country_emoji,
        "impact": impact,
        "impact_emoji": impact_emoji,
        "datetime_utc": utc_dt,
        "datetime_beijing": beijing_dt,
        "date_beijing": beijing_dt.strftime("%Y-%m-%d"),
        "time_beijing": beijing_dt.strftime("%H:%M"),
        "forecast": event.get("forecast", ""),
        "previous": event.get("previous", ""),
        "actual": event.get("actual", "")
    }


def sort_events_by_datetime(events: List[Dict]) -> List[Dict]:
    """
    按时间排序事件
    
    Args:
        events: 事件列表
    
    Returns:
        排序后的事件列表
    """
    return sorted(events, key=lambda x: x["datetime_beijing"])


def group_events_by_date(events: List[Dict]) -> Dict[str, List[Dict]]:
    """
    按日期分组事件
    
    Args:
        events: 事件列表
    
    Returns:
        按日期分组的字典
    """
    grouped = {}
    for event in events:
        date = event["date_beijing"]
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(event)
    return grouped


def generate_briefing(events: List[Dict], target_date: str = None) -> str:
    """
    生成简报文本
    
    Args:
        events: 事件列表
        target_date: 目标日期
    
    Returns:
        格式化简报
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"📊 **经济日历简报** | {target_date}",
        "=" * 50,
        f"📡 数据来源：Forex Factory (实时更新)",
        f"🕐 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)",
        ""
    ]
    
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 按日期分组
    grouped = group_events_by_date(events)
    
    if not grouped:
        lines.append("⚠️ 暂无重要经济事件")
        return "\n".join(lines)
    
    for date in sorted(grouped.keys()):
        date_events = grouped[date]
        
        # 判断日期标签
        if date == today:
            date_label = f"📌 **今天** ({date})"
        elif date == tomorrow:
            date_label = f"📌 **明天** ({date})"
        else:
            date_label = f"📌 **{date}**"
        
        lines.append("")
        lines.append(date_label)
        lines.append("-" * 50)
        
        # 按时间排序
        sorted_events = sort_events_by_datetime(date_events)
        
        for event in sorted_events:
            lines.append("")
            lines.append(f"{event['impact_emoji']} {event['title']}")
            lines.append(f"⏰ {event['time_beijing']} (北京时间)")
            lines.append(f"🌍 {event['country_emoji']}")
            lines.append(f"📊 重要性：{event['impact_emoji']} {event['impact']}")
            
            # 数值信息
            values = []
            if event.get("actual"):
                values.append(f"实际：{event['actual']}")
            if event.get("forecast"):
                values.append(f"预期：{event['forecast']}")
            if event.get("previous"):
                values.append(f"前值：{event['previous']}")
            
            if values:
                lines.append(" | ".join(values))
        
        lines.append("")
    
    lines.append("=" * 50)
    lines.append("⚠️ 数据仅供参考，投资决策请谨慎")
    
    return "\n".join(lines)


def save_to_file(content: str, filepath: str):
    """保存内容到文件"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已保存到：{filepath}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Forex Factory 经济日历数据获取")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--date", type=str, help="目标日期 YYYY-MM-DD")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    parser.add_argument("--days", type=int, default=7, help="获取天数（默认 7 天）")
    
    args = parser.parse_args()
    
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")
    
    # 获取数据
    raw_events = fetch_forex_factory_calendar()
    
    if not raw_events:
        print("⚠️ 未获取到数据")
        return
    
    # 筛选事件
    filtered_events = filter_events(raw_events)
    
    if not filtered_events:
        print("⚠️ 暂无重要经济事件")
        return
    
    # 格式化事件
    formatted_events = [format_event(e) for e in filtered_events]
    
    # 过滤日期范围
    end_date = datetime.now() + timedelta(days=args.days)
    filtered_events = [
        e for e in formatted_events
        if e["datetime_beijing"] <= end_date
    ]
    
    # 生成输出
    if args.format == "json":
        # 转换为可序列化格式
        json_events = []
        for e in filtered_events:
            event_copy = e.copy()
            event_copy["datetime_utc"] = e["datetime_utc"].isoformat()
            event_copy["datetime_beijing"] = e["datetime_beijing"].isoformat()
            json_events.append(event_copy)
        output = json.dumps(json_events, ensure_ascii=False, indent=2)
    else:
        output = generate_briefing(filtered_events, target_date)
    
    # 输出
    if args.output:
        save_to_file(output, args.output)
    else:
        print("\n" + "=" * 50 + "\n")
        print(output)


if __name__ == "__main__":
    main()
