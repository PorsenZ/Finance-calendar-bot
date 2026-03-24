#!/usr/bin/env python3
"""
CoinMarketCal API 集成脚本
获取加密货币事件日历数据
API 文档：https://coinmarketcal.com/en/doc
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置（从.env 文件读取）
COINMARKETCAL_API_KEY = os.getenv("COINMARKETCAL_API_KEY")
if not COINMARKETCAL_API_KEY:
    print("❌ 错误：COINMARKETCAL_API_KEY 未配置，请在 .env 文件中设置")
    exit(1)
# 正确的 API 端点（根据官方文档）
COINMARKETCAL_BASE_URL = "https://developers.coinmarketcal.com/v1"

# 重要性级别
IMPACT_MAP = {
    "major": "High",
    "important": "Medium",
    "normal": "Low"
}

# 事件类型映射
EVENT_TYPE_MAP = {
    "halving": "减半",
    "hard_fork": "硬分叉",
    "soft_fork": "软分叉",
    "airdrop": "空投",
    "listing": "上线交易所",
    "delisting": "下架",
    "partnership": "合作",
    "product_launch": "产品发布",
    "conference": "会议",
    "update": "更新",
    "other": "其他"
}


def fetch_events(days: int = 7, limit: int = 50) -> List[Dict[str, Any]]:
    """
    获取 CoinMarketCal 事件
    API 文档：https://coinmarketcal.com/en/doc
    
    Args:
        days: 获取未来多少天的事件
        limit: 最多返回多少条记录
    
    Returns:
        事件列表
    """
    # 正确的 API 端点
    url = f"{COINMARKETCAL_BASE_URL}/events"
    
    # 计算日期范围
    today = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    
    params = {
        "dateRangeStart": today,
        "dateRangeEnd": end_date,
        "max": min(limit, 75),  # 最多 75 个
        "page": 1
    }
    
    # 正确的认证头（根据官方文档）
    headers = {
        "x-api-key": COINMARKETCAL_API_KEY,
        "Accept": "application/json"
    }
    
    try:
        print(f"📡 正在获取 CoinMarketCal 数据（未来{days}天）...")
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # CoinMarketCal 返回格式：{"body": [...], "status": {...}}
        if "body" in data and isinstance(data["body"], list):
            events = data["body"]
            print(f"✅ 获取到 {len(events)} 个加密货币事件")
            return events
        else:
            print(f"⚠️ 未获取到数据：{data}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API 请求失败：{e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        return []


def format_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    格式化单个事件
    
    Args:
        event: 原始事件字典
    
    Returns:
        格式化后的事件字典
    """
    # CoinMarketCal 返回格式
    title_obj = event.get("title", {})
    title = title_obj.get("en", str(title_obj)) if isinstance(title_obj, dict) else str(title_obj)
    
    coins = event.get("coins", [])
    coin_name = coins[0].get("name", "Unknown") if coins else "Unknown"
    coin_code = coins[0].get("symbol", "") if coins else ""
    
    # 事件日期
    event_date = event.get("date_event", "")
    displayed_date = event.get("displayed_date", "")
    if event_date:
        try:
            event_dt = datetime.strptime(event_date[:19], "%Y-%m-%dT%H:%M:%S")
            beijing_date = event_dt.strftime("%Y-%m-%d")
        except:
            beijing_date = displayed_date or event_date
    else:
        beijing_date = displayed_date or "未知日期"
    
    # 事件类型（从 categories 获取）
    categories = event.get("categories", [])
    event_type = categories[0].get("name", "") if categories else ""
    event_type_cn = EVENT_TYPE_MAP.get(event_type.lower(), event_type)
    
    # 重要性（CoinMarketCal 使用 is_popular, influential_score 等）
    is_popular = event.get("is_popular", False)
    influential_score = event.get("influential_score", 0)
    
    if is_popular or influential_score > 50:
        importance = "High"
    elif influential_score > 20:
        importance = "Medium"
    else:
        importance = "Low"
    
    importance_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(importance, "⚪")
    
    # 描述（使用标题作为描述）
    description = title
    
    # 证明链接
    proof = event.get("proof", "")
    proof_urls = [proof] if proof else []
    
    return {
        "title": title,
        "coin_name": coin_name,
        "coin_code": coin_code,
        "date": beijing_date,
        "event_type": event_type,
        "event_type_cn": event_type_cn,
        "importance": importance,
        "importance_emoji": importance_emoji,
        "description": description[:200] if description else "",
        "proof_urls": proof_urls[:3] if proof_urls else []
    }


def filter_high_importance(events: List[Dict]) -> List[Dict]:
    """
    筛选高重要性事件
    
    Args:
        events: 事件列表
    
    Returns:
        高重要性事件列表
    """
    return [e for e in events if e.get("importance") in ["High", "Medium"]]


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
        f"📡 数据来源：CoinMarketCal",
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
            lines.append("")
            coin_code = event.get("coin_code", "")
            coin_name = event.get("coin_name", "")
            title = event.get("title", "")
            event_type_cn = event.get("event_type_cn", "")
            importance_emoji = event.get("importance_emoji", "")
            
            lines.append(f"{importance_emoji} **{coin_code}** - {title}")
            lines.append(f"   类型：{event_type_cn}")
            
            description = event.get("description", "")
            if description:
                lines.append(f"   说明：{description[:100]}...")
            
            proof_urls = event.get("proof_urls", [])
            if proof_urls:
                lines.append(f"   链接：{proof_urls[0]}")
            
            lines.append("")
    
    lines.append("=" * 50)
    lines.append("⚠️ 数据仅供参考，投资需谨慎")
    
    return "\n".join(lines)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CoinMarketCal 加密货币事件获取")
    parser.add_argument("--days", type=int, default=7, help="获取未来多少天的事件")
    parser.add_argument("--limit", type=int, default=50, help="最多返回多少条记录")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    parser.add_argument("--high-only", action="store_true", help="只显示高重要性事件")
    
    args = parser.parse_args()
    
    # 获取数据
    raw_events = fetch_events(days=args.days, limit=args.limit)
    
    if not raw_events:
        print("⚠️ 未获取到数据")
        return
    
    # 格式化事件
    formatted_events = [format_event(e) for e in raw_events]
    
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
