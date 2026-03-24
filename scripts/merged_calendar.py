#!/usr/bin/env python3
"""
经济日历合并脚本 - 传统金融 + 加密货币
整合 Forex Factory 和 CoinMarketCal 数据
"""

import os
import sys
from datetime import datetime

# 脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/home/ubuntu/.openclaw/workspace/shared/02_outbox")

def run_script(script_name: str, args: str = "") -> bool:
    """运行子脚本"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在：{script_path}")
        return False
    
    cmd = f"python3 {script_path} {args}"
    print(f"🚀 执行：{cmd}")
    exit_code = os.system(cmd)
    return exit_code == 0

def merge_reports(traditional_file: str, crypto_file: str, output_file: str):
    """合并两个报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("📊 综合经济日历（传统金融 + 加密货币）")
    lines.append("=" * 60)
    lines.append(f"🕐 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (北京时间)")
    lines.append("")
    
    # 读取传统金融报告
    if os.path.exists(traditional_file):
        with open(traditional_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines.append("📈 传统金融事件")
            lines.append("-" * 60)
            # 跳过标题行
            for line in content.split('\n')[6:]:  # 跳过前 6 行标题
                if line.strip() and not line.startswith('='):
                    lines.append(line)
            lines.append("")
    
    # 读取加密货币报告
    if os.path.exists(crypto_file):
        with open(crypto_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines.append("🪙 加密货币事件")
            lines.append("-" * 60)
            # 跳过标题行
            for line in content.split('\n')[6:]:  # 跳过前 6 行标题
                if line.strip() and not line.startswith('='):
                    lines.append(line)
            lines.append("")
    
    # 保存合并报告
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ 已保存到：{output_file}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="经济日历合并脚本")
    parser.add_argument("--days", type=int, default=7, help="获取未来多少天的事件")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--crypto-only", action="store_true", help="只获取加密货币事件")
    parser.add_argument("--traditional-only", action="store_true", help="只获取传统金融事件")
    
    args = parser.parse_args()
    
    timestamp = datetime.now().strftime('%Y%m%d')
    
    # 文件路径
    traditional_file = os.path.join(OUTPUT_DIR, f"traditional_events_{timestamp}.md")
    crypto_file = os.path.join(OUTPUT_DIR, f"crypto_events_{timestamp}.md")
    output_file = args.output or os.path.join(OUTPUT_DIR, f"merged_calendar_{timestamp}.md")
    
    print("=" * 60)
    print("📊 经济日历合并脚本")
    print("=" * 60)
    print("")
    
    # 获取传统金融数据
    if not args.crypto_only:
        print("📈 获取传统金融事件...")
        success = run_script("forex_factory_calendar.py", f"--days {args.days} --output {traditional_file}")
        if not success:
            print("⚠️ 传统金融数据获取失败，继续获取加密货币数据...")
    
    print("")
    
    # 获取加密货币数据
    if not args.traditional_only:
        print("🪙 获取加密货币事件...")
        success = run_script("coinmarketcal_calendar.py", f"--days {args.days} --high-only --output {crypto_file}")
        if not success:
            print("⚠️ 加密货币数据获取失败")
    
    print("")
    
    # 合并报告
    if not args.crypto_only and not args.traditional_only:
        print("📋 合并报告...")
        merge_reports(traditional_file, crypto_file, output_file)
    
    print("")
    print("=" * 60)
    print("✅ 完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
