#!/usr/bin/env python3
"""
FMP 经济日历数据获取脚本
获取 Financial Modeling Prep 的经济日历数据
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置
# 注意：此脚本已废弃，使用 forex_factory_calendar.py 替代
FMP_API_KEY = os.getenv("FMP_API_KEY", "")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

# 重要性级别权重
IMPORTANCE_WEIGHTS = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

# 关键事件关键词（高优先级）
KEY_EVENTS = [
    "FOMC", "Federal Open Market Committee", "Interest Rate Decision",
    "CPI", "Consumer Price Index", "Core CPI", "Inflation",
    "Non-Farm Payrolls", "NFP", "Unemployment Rate", "Initial Jobless Claims",
    "GDP", "Gross Domestic Product", "Advance GDP", "Final GDP",
    "Retail Sales", "Core Retail Sales",
    "ISM", "PMI", "Manufacturing PMI", "Services PMI",
    "Fed Chair", "Powell", "ECB", "PBOC", "BOJ",
    "Central Bank", "Rate Decision", "Monetary Policy",
    "Producer Price Index", "PPI",
    "Consumer Confidence", "Consumer Sentiment",
    "Housing Starts", "Building Permits",
    "Trade Balance", "Current Account"
]


def fetch_economic_calendar(from_date: str, to_date: str) -> List[Dict[str, Any]]:
    """
    获取经济日历数据
    
    Args:
        from_date: 开始日期 YYYY-MM-DD
        to_date: 结束日期 YYYY-MM-DD
    
    Returns:
        经济事件列表
    """
    url = f"{FMP_BASE_URL}/economic_calendar"
    params = {
        "from": from_date,
        "to": to_date,
        "apikey": FMP_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 检查是否是错误响应
        if isinstance(data, dict) and "Error Message" in data:
            print(f"❌ API 错误：{data['Error Message']}")
            return []
        
        if isinstance(data, list):
            return data
        else:
            print(f"⚠️ 意外的响应格式：{type(data)}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        return []


def filter_key_events(events: List[Dict[str, Any]], min_importance: str = "Medium") -> List[Dict[str, Any]]:
    """
    筛选关键事件
    
    Args:
        events: 原始事件列表
        min_importance: 最小重要性级别 (Low/Medium/High)
    
    Returns:
        筛选后的事件列表
    """
    min_weight = IMPORTANCE_WEIGHTS.get(min_importance, 1)
    filtered = []
    
    for event in events:
        importance = event.get("importance", "Low")
        event_weight = IMPORTANCE_WEIGHTS.get(importance, 1)
        
        # 按重要性筛选
        if event_weight >= min_weight:
            filtered.append(event)
            continue
        
        # 按关键词筛选（即使重要性低，如果是关键事件也保留）
        event_name = event.get("name", "").upper()
        if any(keyword.upper() in event_name for keyword in KEY_EVENTS):
            filtered.append(event)
    
    return filtered


def sort_events_by_importance(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    按重要性和时间排序事件
    
    Args:
        events: 事件列表
    
    Returns:
        排序后的事件列表
    """
    def sort_key(event):
        importance = event.get("importance", "Low")
        weight = IMPORTANCE_WEIGHTS.get(importance, 1)
        date = event.get("date", "9999-99-99")
        time = event.get("time", "23:59")
        # 重要性降序，时间升序
        return (-weight, date, time)
    
    return sorted(events, key=sort_key)


def utc_to_beijing(utc_date: str, utc_time: str = "00:00") -> str:
    """
    UTC 时间转换为北京时间
    
    Args:
        utc_date: UTC 日期 YYYY-MM-DD
        utc_time: UTC 时间 HH:MM
    
    Returns:
        北京时间字符串
    """
    try:
        utc_dt = datetime.strptime(f"{utc_date} {utc_time}", "%Y-%m-%d %H:%M")
        beijing_dt = utc_dt + timedelta(hours=8)
        return beijing_dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return f"{utc_date} {utc_time}"


def format_event_for_push(event: Dict[str, Any]) -> str:
    """
    格式化单个事件为推送文本
    
    Args:
        event: 事件字典
    
    Returns:
        格式化后的字符串
    """
    name = event.get("name", "未知事件")
    date = event.get("date", "")
    time = event.get("time", "")
    country = event.get("country", "")
    importance = event.get("importance", "")
    actual = event.get("actual")
    consensus = event.get("consensus")
    previous = event.get("previous")
    
    # 转换为北京时间
    beijing_time = utc_to_beijing(date, time)
    
    # 构建文本
    parts = [f"📅 {name}"]
    parts.append(f"⏰ {beijing_time} (北京时间)")
    
    if country:
        country_emoji = {"US": "🇺🇸", "CN": "🇨🇳", "EU": "🇪🇺", "UK": "🇬🇧", "JP": "🇯🇵"}.get(country, country)
        parts.append(f"🌍 {country_emoji}")
    
    if importance:
        importance_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(importance, "")
        parts.append(f"📊 重要性：{importance_emoji} {importance}")
    
    # 数值信息
    values = []
    if actual is not None:
        values.append(f"实际：{actual}")
    if consensus is not None:
        values.append(f"预期：{consensus}")
    if previous is not None:
        values.append(f"前值：{previous}")
    
    if values:
        parts.append(" | ".join(values))
    
    return "\n".join(parts)


def format_daily_briefing(events: List[Dict[str, Any]], date: str = None) -> str:
    """
    格式化每日经济日历简报
    
    Args:
        events: 事件列表
        date: 日期（默认为今天）
    
    Returns:
        格式化后的简报文本
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"📊 **经济日历简报** | {date}",
        "=" * 40,
        ""
    ]
    
    if not events:
        lines.append("⚠️ 今日无重要经济事件")
        return "\n".join(lines)
    
    # 按日期分组
    events_by_date = {}
    for event in events:
        event_date = event.get("date", date)
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append(event)
    
    for event_date in sorted(events_by_date.keys()):
        date_events = events_by_date[event_date]
        beijing_date = utc_to_beijing(event_date).split()[0]
        
        # 判断是今天、明天还是其他日期
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        if beijing_date == today:
            date_label = "📌 **今天**"
        elif beijing_date == tomorrow:
            date_label = "📌 **明天**"
        else:
            date_label = f"📌 **{beijing_date}**"
        
        lines.append(date_label)
        lines.append("-" * 30)
        
        for event in sort_events_by_importance(date_events):
            lines.append("")
            lines.append(format_event_for_push(event))
        
        lines.append("")
    
    lines.append("=" * 40)
    lines.append("数据来源：Financial Modeling Prep")
    
    return "\n".join(lines)


def save_to_file(content: str, filepath: str):
    """保存内容到文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已保存到：{filepath}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FMP 经济日历数据获取")
    parser.add_argument("--from-date", type=str, help="开始日期 YYYY-MM-DD")
    parser.add_argument("--to-date", type=str, help="结束日期 YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=7, help="获取天数（默认 7 天）")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    parser.add_argument("--min-importance", choices=["Low", "Medium", "High"], default="Medium", help="最小重要性")
    
    args = parser.parse_args()
    
    # 计算日期范围
    if args.from_date:
        from_date = args.from_date
    else:
        from_date = datetime.now().strftime("%Y-%m-%d")
    
    if args.to_date:
        to_date = args.to_date
    else:
        to_date = (datetime.now() + timedelta(days=args.days)).strftime("%Y-%m-%d")
    
    print(f"📅 获取经济日历：{from_date} 至 {to_date}")
    
    # 获取数据
    events = fetch_economic_calendar(from_date, to_date)
    
    if not events:
        print("⚠️ 未获取到数据")
        sys.exit(1)
    
    print(f"✅ 获取到 {len(events)} 个事件")
    
    # 筛选关键事件
    filtered_events = filter_key_events(events, args.min_importance)
    print(f"🎯 筛选后关键事件：{len(filtered_events)} 个")
    
    # 输出
    if args.format == "json":
        output = json.dumps(filtered_events, ensure_ascii=False, indent=2)
    else:
        output = format_daily_briefing(filtered_events, from_date)
    
    if args.output:
        save_to_file(output, args.output)
    else:
        print("\n" + "=" * 40 + "\n")
        print(output)


if __name__ == "__main__":
    main()
