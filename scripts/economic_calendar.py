#!/usr/bin/env python3
"""
经济日历数据获取脚本 - 多数据源版本
支持：
1. Alpha Vantage API（经济指标数据）
2. 手动输入模式（临时方案）
3. 爬虫模式（Investing.com，待实现）
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 配置
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

# 输出目录
OUTPUT_DIR = "/home/ubuntu/.openclaw/workspace/shared/02_outbox"

# 手动输入的经济日历数据（需要定期更新）
MANUAL_CALENDAR = [
    {
        "name": "FOMC 议息会议",
        "date": "2026-03-19",
        "time": "14:00",
        "country": "US",
        "importance": "High",
        "actual": None,
        "consensus": None,
        "previous": "5.25-5.50%",
        "note": "美联储 3 月利率决议"
    },
    {
        "name": "美国 CPI (YoY)",
        "date": "2026-03-18",
        "time": "12:30",
        "country": "US",
        "importance": "High",
        "actual": None,
        "consensus": "3.0%",
        "previous": "3.1%",
        "note": "2 月消费者物价指数年率"
    },
    {
        "name": "美国非农就业人口",
        "date": "2026-03-21",
        "time": "12:30",
        "country": "US",
        "importance": "High",
        "actual": None,
        "consensus": "200K",
        "previous": "275K",
        "note": "2 月非农就业人口变动"
    },
    {
        "name": "中国 LPR 报价",
        "date": "2026-03-20",
        "time": "01:15",
        "country": "CN",
        "importance": "High",
        "actual": None,
        "consensus": "3.45%",
        "previous": "3.45%",
        "note": "中国 1 年期贷款市场报价利率"
    },
    {
        "name": "欧央行利率决议",
        "date": "2026-03-21",
        "time": "12:15",
        "country": "EU",
        "importance": "High",
        "actual": None,
        "consensus": "4.00%",
        "previous": "4.00%",
        "note": "欧洲央行主要再融资利率"
    },
]


def fetch_alpha_vantage(function: str, params: dict = None) -> dict:
    """
    调用 Alpha Vantage API
    
    Args:
        function: API 函数名（CPI, FEDERAL_FUNDS_RATE, 等）
        params: 额外参数
    
    Returns:
        API 响应数据
    """
    import time
    time.sleep(1)  # 遵守 1 秒 1 次的限制
    
    url = ALPHA_VANTAGE_URL
    query_params = {
        "function": function,
        "apikey": ALPHA_VANTAGE_KEY
    }
    if params:
        query_params.update(params)
    
    try:
        response = requests.get(url, params=query_params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ API 请求失败：{e}")
        return {}


def get_economic_indicators() -> Dict[str, Any]:
    """
    获取主要经济指标数据
    
    Returns:
        包含各项指标数据的字典
    """
    indicators = {}
    
    # CPI 数据
    print("📊 获取 CPI 数据...")
    cpi_data = fetch_alpha_vantage("CPI")
    if "data" in cpi_data and len(cpi_data["data"]) > 0:
        indicators["CPI"] = {
            "latest": cpi_data["data"][0],
            "previous": cpi_data["data"][1] if len(cpi_data["data"]) > 1 else None
        }
    
    # 联邦基金利率
    print("📊 获取联邦基金利率...")
    ff_data = fetch_alpha_vantage("FEDERAL_FUNDS_RATE")
    if "data" in ff_data and len(ff_data["data"]) > 0:
        indicators["FEDERAL_FUNDS_RATE"] = {
            "latest": ff_data["data"][0],
            "previous": ff_data["data"][1] if len(ff_data["data"]) > 1 else None
        }
    
    # 失业率
    print("📊 获取失业率数据...")
    unemp_data = fetch_alpha_vantage("UNEMPLOYMENT")
    if "data" in unemp_data and len(unemp_data["data"]) > 0:
        indicators["UNEMPLOYMENT"] = {
            "latest": unemp_data["data"][0],
            "previous": unemp_data["data"][1] if len(unemp_data["data"]) > 1 else None
        }
    
    # 非农就业
    print("📊 获取非农就业数据...")
    nfp_data = fetch_alpha_vantage("NONFARM_PAYROLL")
    if "data" in nfp_data and len(nfp_data["data"]) > 0:
        indicators["NONFARM_PAYROLL"] = {
            "latest": nfp_data["data"][0],
            "previous": nfp_data["data"][1] if len(nfp_data["data"]) > 1 else None
        }
    
    return indicators


def update_manual_calendar_with_api_data(manual_events: List[Dict], indicators: Dict) -> List[Dict]:
    """
    用 API 数据更新手动日历
    
    Args:
        manual_events: 手动输入的事件
        indicators: API 获取的指标数据
    
    Returns:
        更新后的事件列表
    """
    updated = []
    
    for event in manual_events:
        event_copy = event.copy()
        event_name = event.get("name", "").upper()
        
        # 根据事件名称匹配 API 数据
        if "CPI" in event_name and "CPI" in indicators:
            cpi = indicators["CPI"]
            if cpi.get("latest"):
                event_copy["previous"] = f"{cpi['latest']['value']}"
        
        if "非农" in event_name and "NONFARM_PAYROLL" in indicators:
            nfp = indicators["NONFARM_PAYROLL"]
            if nfp.get("latest"):
                event_copy["previous"] = f"{nfp['latest']['value']}K"
        
        if "利率" in event_name and "FEDERAL_FUNDS_RATE" in indicators:
            ff = indicators["FEDERAL_FUNDS_RATE"]
            if ff.get("latest"):
                event_copy["previous"] = f"{ff['latest']['value']}%"
        
        updated.append(event_copy)
    
    return updated


def utc_to_beijing(utc_date: str, utc_time: str) -> str:
    """UTC 时间转北京时间"""
    try:
        utc_dt = datetime.strptime(f"{utc_date} {utc_time}", "%Y-%m-%d %H:%M")
        beijing_dt = utc_dt + timedelta(hours=8)
        return beijing_dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return f"{utc_date} {utc_time}"


def format_event(event: Dict) -> str:
    """格式化单个事件"""
    lines = []
    importance_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(event.get("importance", ""), "⚪")
    country_emoji = {"US": "🇺🇸", "CN": "🇨🇳", "EU": "🇪🇺", "UK": "🇬🇧", "JP": "🇯🇵"}.get(event.get("country", ""), event.get("country", ""))
    
    beijing_time = utc_to_beijing(event["date"], event["time"])
    
    lines.append(f"{importance_emoji} {event['name']}")
    lines.append(f"⏰ {beijing_time} (北京时间)")
    lines.append(f"🌍 {country_emoji}")
    lines.append(f"📊 重要性：{importance_emoji} {event.get('importance', 'Unknown')}")
    
    values = []
    if event.get("actual"):
        values.append(f"实际：{event['actual']}")
    if event.get("consensus"):
        values.append(f"预期：{event['consensus']}")
    if event.get("previous"):
        values.append(f"前值：{event['previous']}")
    
    if values:
        lines.append(" | ".join(values))
    
    if event.get("note"):
        lines.append(f"📝 {event['note']}")
    
    return "\n".join(lines)


def generate_briefing(events: List[Dict], target_date: str = None) -> str:
    """生成简报"""
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"📊 **经济日历简报** | {target_date}",
        "=" * 40,
        ""
    ]
    
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 按日期分组
    events_by_date = {}
    for event in events:
        event_date = event.get("date", today)
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append(event)
    
    for event_date in sorted(events_by_date.keys()):
        date_events = events_by_date[event_date]
        beijing_date = utc_to_beijing(event_date, "00:00").split()[0]
        
        # 判断日期标签
        if beijing_date == today:
            date_label = "📌 **今天**"
        elif beijing_date == tomorrow:
            date_label = "📌 **明天**"
        else:
            date_label = f"📌 **{beijing_date}**"
        
        lines.append(date_label)
        lines.append("-" * 30)
        
        # 按重要性排序
        importance_order = {"High": 0, "Medium": 1, "Low": 2}
        sorted_events = sorted(date_events, key=lambda x: importance_order.get(x.get("importance", "Low"), 2))
        
        for event in sorted_events:
            lines.append("")
            lines.append(format_event(event))
        
        lines.append("")
    
    lines.append("=" * 40)
    lines.append("📊 数据来源：Alpha Vantage API + 手动输入")
    
    return "\n".join(lines)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="经济日历数据获取（多数据源）")
    parser.add_argument("--mode", choices=["api", "manual", "hybrid"], default="hybrid", help="数据模式")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--date", type=str, help="目标日期 YYYY-MM-DD")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")
    
    if args.mode == "api":
        print("🔄 从 Alpha Vantage API 获取经济指标数据...")
        indicators = get_economic_indicators()
        print(f"✅ 获取到 {len(indicators)} 个指标")
        output = json.dumps(indicators, ensure_ascii=False, indent=2)
    
    elif args.mode == "manual":
        print("📝 使用手动输入模式...")
        briefing = generate_briefing(MANUAL_CALENDAR, target_date)
        output = briefing if args.format == "text" else json.dumps(MANUAL_CALENDAR, ensure_ascii=False, indent=2)
    
    else:  # hybrid
        print("🔄 混合模式：获取 API 数据 + 手动日历...")
        indicators = get_economic_indicators()
        print(f"✅ 获取到 {len(indicators)} 个指标")
        updated_events = update_manual_calendar_with_api_data(MANUAL_CALENDAR, indicators)
        briefing = generate_briefing(updated_events, target_date)
        output = briefing if args.format == "text" else json.dumps(updated_events, ensure_ascii=False, indent=2)
    
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 已保存到：{args.output}")
    else:
        print("\n" + "=" * 40 + "\n")
        print(output)


if __name__ == "__main__":
    main()
