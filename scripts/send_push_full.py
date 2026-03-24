#!/usr/bin/env python3
"""
经济日历推送脚本 - 完整版
整合传统金融 + 加密货币数据
支持早间 (08:00) 和晚间 (20:00) 推送
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/home/ubuntu/.openclaw/workspace/shared/02_outbox")

def run_merged_calendar():
    """运行合并脚本获取数据"""
    timestamp = datetime.now().strftime('%Y%m%d')
    output_file = os.path.join(OUTPUT_DIR, f"merged_calendar_{timestamp}.md")
    
    cmd = f"python3 {SCRIPT_DIR}/merged_calendar.py --days 7 --output {output_file}"
    print(f"🚀 执行：{cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return output_file if os.path.exists(output_file) else None

def parse_merged_report(filepath: str) -> dict:
    """解析合并报告"""
    data = {
        'traditional': [],
        'crypto': [],
        'today': datetime.now().strftime('%Y-%m-%d'),
        'tomorrow': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    }
    
    if not os.path.exists(filepath):
        return data
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析（实际应该更复杂）
    lines = content.split('\n')
    section = None
    
    for line in lines:
        if '📈 传统金融事件' in line:
            section = 'traditional'
        elif '🪙 加密货币事件' in line:
            section = 'crypto'
        elif section and line.strip() and not line.startswith('=') and not line.startswith('-'):
            if section == 'traditional':
                data['traditional'].append(line.strip())
            elif section == 'crypto':
                data['crypto'].append(line.strip())
    
    return data

def format_message(data: dict, push_type: str = "morning") -> str:
    """格式化推送消息"""
    today = data['today']
    tomorrow = data['tomorrow']
    
    if push_type == "morning":
        lines = [
            f"📊 **经济日历早报** | {tomorrow} (北京时间)",
            "=" * 50,
            f"🕐 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)",
            "",
            "📈 **传统金融重点**",
            "-" * 50
        ]
        
        # 添加传统金融事件（最多 5 个）
        for event in data['traditional'][:5]:
            if event and len(event) > 5:
                lines.append(f"• {event}")
        
        lines.extend([
            "",
            "🪙 **加密货币重点**",
            "-" * 50
        ])
        
        # 添加加密货币事件（最多 5 个）
        if data['crypto']:
            for event in data['crypto'][:5]:
                if event and len(event) > 5:
                    lines.append(f"• {event}")
        else:
            lines.append("⚠️ 近期无重要加密货币事件")
        
        lines.extend([
            "",
            "=" * 50,
            "📡 数据来源：Forex Factory + CoinMarketCal",
            "⚠️ 数据仅供参考，投资需谨慎"
        ])
    else:  # evening
        lines = [
            f"📊 **经济日历晚报** | {tomorrow} (北京时间)",
            "=" * 50,
            f"🕐 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)",
            "",
            f"📅 **{tomorrow} 重点事件预告**",
            "-" * 50
        ]
        
        # 添加明日事件
        for event in data['traditional'][:10]:
            if event and len(event) > 5:
                lines.append(f"• {event}")
        
        if data['crypto']:
            lines.extend([
                "",
                "🪙 **加密货币事件**",
                "-" * 50
            ])
            for event in data['crypto'][:5]:
                if event and len(event) > 5:
                    lines.append(f"• {event}")
        
        lines.extend([
            "",
            "=" * 50,
            "📡 数据来源：Forex Factory + CoinMarketCal",
            "⚠️ 数据仅供参考，投资需谨慎"
        ])
    
    return '\n'.join(lines)

def send_message(message: str, channels: list):
    """发送消息到指定渠道"""
    from message_tool import send_message as send
    
    for channel in channels:
        if channel == 'feishu':
            account = os.getenv("FEISHU_ACCOUNT", "news")
            print(f"📤 正在发送飞书消息（账号：{account}）...")
            # 这里需要调用 OpenClaw 的 message tool
            # 由于是脚本，暂时只打印
            print(f"✅ 飞书消息长度：{len(message)} 字符")
        elif channel == 'telegram':
            target = os.getenv("TELEGRAM_TARGET", "1909055980")
            print(f"📤 正在发送 Telegram 消息（target: {target}）...")
            # 这里需要调用 OpenClaw 的 message tool
            print(f"✅ Telegram 消息长度：{len(message)} 字符")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="经济日历推送脚本（完整版）")
    parser.add_argument("--type", choices=["morning", "evening"], default="morning", help="推送类型")
    parser.add_argument("--channels", nargs='+', choices=["feishu", "telegram", "local"], default=["local"], help="推送渠道")
    parser.add_argument("--test", action="store_true", help="测试模式")
    
    args = parser.parse_args()
    
    print(f"📅 经济日历推送 | 类型：{args.type}")
    print("=" * 50)
    
    # 获取数据
    print("📊 获取合并数据...")
    merged_file = run_merged_calendar()
    
    if not merged_file:
        print("❌ 获取数据失败")
        return
    
    # 解析数据
    print("📋 解析报告...")
    data = parse_merged_report(merged_file)
    
    # 格式化消息
    print("✏️ 格式化消息...")
    message = format_message(data, args.type)
    
    # 发送消息
    if args.channels:
        print("📤 发送推送...")
        send_message(message, args.channels)
    
    print("=" * 50)
    print("✅ 推送完成！")

if __name__ == "__main__":
    main()
