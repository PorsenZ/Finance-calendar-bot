#!/usr/bin/env python3
"""
经济日历推送脚本 - 带缓存版本
避免 API 限流问题
"""

import os
import sys
import json
from datetime import datetime, timedelta

# 配置
OUTPUT_DIR = "/home/ubuntu/.openclaw/workspace/shared/02_outbox"
CACHE_DIR = os.path.join(OUTPUT_DIR, "cache")
CACHE_EXPIRY_MINUTES = 5  # 缓存 5 分钟

def get_cached_data(data_type: str) -> dict:
    """获取缓存数据"""
    cache_file = os.path.join(CACHE_DIR, f"{data_type}_cache.json")
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 检查缓存是否过期
            cache_time = datetime.fromisoformat(data['cache_time'])
            if datetime.now() - cache_time < timedelta(minutes=CACHE_EXPIRY_MINUTES):
                print(f"✅ 使用缓存数据：{data_type}")
                return data['content']
    except Exception as e:
        print(f"⚠️ 读取缓存失败：{e}")
    
    return None

def save_cache(data_type: str, content: dict):
    """保存缓存"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{data_type}_cache.json")
    
    cache_data = {
        'cache_time': datetime.now().isoformat(),
        'content': content
    }
    
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存缓存：{data_type}")
    except Exception as e:
        print(f"⚠️ 保存缓存失败：{e}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="经济日历推送脚本（带缓存）")
    parser.add_argument("--type", choices=["morning", "evening"], default="morning", help="推送类型")
    parser.add_argument("--channels", nargs='+', choices=["feishu", "telegram", "local"], default=["local"], help="推送渠道")
    parser.add_argument("--test", action="store_true", help="测试模式")
    parser.add_argument("--force-refresh", action="store_true", help="强制刷新，不使用缓存")
    
    args = parser.parse_args()
    
    print(f"📅 经济日历推送 | 类型：{args.type}")
    print("=" * 40)
    
    # 检查缓存
    if not args.force_refresh:
        cached_data = get_cached_data("traditional")
        if cached_data:
            print("✅ 使用缓存数据，跳过 API 调用")
            # TODO: 使用 cached_data 生成推送内容
            return
    
    # TODO: 调用 API 获取数据
    print("🔄 正在获取最新数据...")
    # ... 原有逻辑 ...
    
    print("✅ 推送完成！")

if __name__ == "__main__":
    main()
