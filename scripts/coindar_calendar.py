#!/usr/bin/env python3
"""
Coindar API 集成脚本
获取加密货币事件日历数据
API 文档：https://coindar.org/zh-cn/api
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置
COINDAR_API_KEY = os.getenv("COINDAR_API_KEY", "")
COINDAR_BASE_URL = "https://coindar.org/api/v2"

# 重要性映射
IMPORTANCE_MAP = {
    "true": "High",
    "false": "Medium"
}


def get_coins() -> List[Dict[str, Any]]:
    """获取所有加密货币列表"""
    url = f"{COINDAR_BASE_URL}/coins"
    params = {"access_token": COINDAR_API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 获取币种列表失败：{e}")
        return []


def get_tags() -> List[Dict[str, Any]]:
    """获取所有事件标签"""
    url = f"{COINDAR_BASE_URL}/tags"
    params = {"access_token": COINDAR_API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 获取标签失败：{e}")
        return []


def get_events(days: int = 7, page_size: int = 100) -> List[Dict[str, Any]]:
    """
    获取加密货币事件
    
    Args:
        days: 获取未来多少天的事件
        page_size: 每页数量 (1-100)
    
    Returns:
        事件列表
    """
    url = f"{COINDAR_BASE_URL}/events"
    
    # 计算日期范围
    today = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    
    params = {
        "access_token": COINDAR_API_KEY,
        "page": 1,
        "page_size": page_size,
        "filter_date_start": today,
        "filter_date_end": end_date,
        "sort_by": "date_start",
        "order_by": "0"  # 升序
    }
    
    try:
        print(f"📡 正在获取 Coindar 数据（未来{days}天）...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        events = response.json()
        
        if isinstance(events, list):
            print(f"✅ 获取到 {len(events)} 个加密货币事件")
            return events
        else:
            print(f"⚠️ 未获取到数据：{events}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API 请求失败：{e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        return []


def parse_date(date_str: str) -> datetime:
    """
    解析 Coindar 日期字符串
    格式："2018-7-11 06:00" 或 "2018-7-11"
    
    Args:
        date_str: 日期字符串
    
    Returns:
        datetime 对象
    """
    try:
        # 尝试带时间的格式
        if ' ' in date_str:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        # 尝试只有日期的格式
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return datetime.now()


def format_event(event: Dict[str, Any], coins: List[Dict]) -> Dict[str, Any]:
    """
    格式化单个事件
    
    Args:
        event: 原始事件字典
        coins: 币种列表
    
    Returns:
        格式化后的事件字典
    """
    # 获取币种信息
    coin_id = event.get("coin_id", "")
    coin_info = next((c for c in coins if c.get("id") == coin_id), {})
    
    coin_name = coin_info.get("name", "Unknown")
    coin_symbol = coin_info.get("symbol", "")
    
    # 解析日期
    date_start = event.get("date_start", "")
    date_end = event.get("date_end", "")
    
    start_dt = parse_date(date_start)
    beijing_dt = start_dt  # Coindar 返回的已经是本地时间
    
    # 重要性
    important = event.get("important", "false")
    importance = IMPORTANCE_MAP.get(str(important).lower(), "Medium")
    importance_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(importance, "⚪")
    
    # 事件信息
    caption = event.get("caption", "未知事件")
    source = event.get("source", "")
    source_reliable = event.get("source_reliable", "false")
    
    return {
        "title": caption,
        "coin_name": coin_name,
        "coin_symbol": coin_symbol,
        "date": beijing_dt.strftime("%Y-%m-%d"),
        "time": beijing_dt.strftime("%H:%M") if len(date_start) > 10 else "",
        "importance": importance,
        "importance_emoji": importance_emoji,
        "source": source,
        "source_reliable": source_reliable,
        "date_end": date_end
    }


def filter_high_importance(events: List[Dict]) -> List[Dict]:
    """筛选高重要性事件"""
    return [e for e in events if e.get("importance") == "High"]


def generate_briefing(events: List[Dict], target_date: str = None) -> str:
    """
    生成简报
    
    Args:
        events: 事件列表
        target_date: 目标日期
    
    Returns:
        格式化简报
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"🪙 **加密货币事件日历** | {target_date}",
        "=" * 50,
        f"📡 数据来源：Coindar",
        f"🕐 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)",
        ""
    ]
    
    if not events:
        lines.append("⚠️ 近期无重要加密货币事件")
        return "\n".join(lines)
    
    # 按日期分组
    events_by_date = {}
    for event in events:
        date = event.get("date", "unknown")
        if date not in events_by_date:
            events_by_date[date] = []
        events_by_date[date].append(event)
    
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    for date in sorted(events_by_date.keys()):
        date_events = events_by_date[date]
        
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
        
        # 按重要性排序
        sorted_events = sorted(date_events, key=lambda x: {"High": 0, "Medium": 1, "Low": 2}.get(x.get("importance", "Low"), 2))
        
        for event in sorted_events[:10]:  # 每天最多显示 10 个
            coin_symbol = event.get("coin_symbol", "")
            coin_name = event.get("coin_name", "")
            title = event.get("title", "")
            time = event.get("time", "")
            importance_emoji = event.get("importance_emoji", "")
            
            lines.append("")
            lines.append(f"{importance_emoji} **{coin_symbol}** - {title}")
            
            if time:
                lines.append(f"   ⏰ {time} (北京时间)")
            
            source = event.get("source", "")
            if source:
                lines.append(f"   🔗 {source}")
            
            lines.append("")
    
    lines.append("=" * 50)
    lines.append("⚠️ 数据仅供参考，投资需谨慎")
    
    return "\n".join(lines)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Coindar 加密货币事件获取")
    parser.add_argument("--days", type=int, default=7, help="获取未来多少天的事件")
    parser.add_argument("--page-size", type=int, default=100, help="每页数量 (1-100)")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    parser.add_argument("--high-only", action="store_true", help="只显示高重要性事件")
    
    args = parser.parse_args()
    
    if not COINDAR_API_KEY:
        print("❌ 错误：COINDAR_API_KEY 未配置，请在 .env 文件中设置")
        return
    
    # 获取币种列表
    coins = get_coins()
    if not coins:
        print("⚠️ 无法获取币种列表，使用默认数据")
        coins = []
    
    # 获取事件
    raw_events = get_events(days=args.days, page_size=args.page_size)
    
    if not raw_events:
        print("⚠️ 未获取到事件数据")
        return
    
    # 格式化事件
    formatted_events = [format_event(e, coins) for e in raw_events]
    
    # 筛选高重要性
    if args.high_only:
        formatted_events = filter_high_importance(formatted_events)
        print(f"🎯 筛选后剩余 {len(formatted_events)} 个高重要性事件")
    
    # 生成输出
    if args.format == "json":
        output = json.dumps(formatted_events, ensure_ascii=False, indent=2)
    else:
        output = generate_briefing(formatted_events)
    
    # 输出
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 已保存到：{args.output}")
    else:
        print("\n" + "=" * 50 + "\n")
        print(output)


if __name__ == "__main__":
    main()
