"""
测试改进后的可视化功能
"""

import sys
sys.path.append('d:/股票分析')

from visualizer import StockVisualizer
from data_crawler import StockDataCrawler
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_improved_visualization():
    """测试改进的可视化功能"""
    print("🧪 测试改进的可视化功能...")
    
    # 创建测试数据
    dates = pd.date_range(start='2024-07-01', periods=50)
    np.random.seed(42)
    
    # 生成模拟股价数据
    base_price = 30.0
    price_changes = np.random.normal(0, 0.02, 50)
    prices = [base_price]
    
    for change in price_changes[:-1]:
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1.0))
    
    test_data = pd.DataFrame({
        'date': dates,
        'open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
        'close': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'volume': np.random.randint(1000000, 10000000, 50),
        'amount': np.random.uniform(30000000, 300000000, 50),
        'ma5': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
        'ma20': [p * (1 + np.random.normal(0, 0.001)) for p in prices],
        'rsi': np.random.uniform(25, 75, 50)
    })
    
    # 获取股票名称（使用平安银行作为示例）
    print("📋 测试获取股票名称...")
    crawler = StockDataCrawler()
    stock_name = crawler.get_stock_name('000001')
    print(f"✅ 获取到股票名称: {stock_name}")
    
    # 创建可视化器
    visualizer = StockVisualizer()
    
    # 测试1: 股票概览图
    print("\n📊 测试股票概览图（带股票名称和日期）...")
    try:
        visualizer.plot_stock_overview(
            test_data, 
            '000001', 
            stock_name,
            'd:/股票分析/test_overview_improved.png'
        )
        print("✅ 股票概览图生成成功")
    except Exception as e:
        print(f"❌ 股票概览图生成失败: {e}")
    
    # 测试2: 交互式K线图
    print("\n📈 测试交互式K线图（带股票名称和日期）...")
    try:
        visualizer.plot_interactive_kline(
            test_data,
            '000001',
            stock_name,
            'd:/股票分析/test_interactive_improved.html'
        )
        print("✅ 交互式K线图生成成功")
    except Exception as e:
        print(f"❌ 交互式K线图生成失败: {e}")
    
    # 测试3: 预测结果图
    print("\n🔮 测试预测结果图（带股票名称和具体日期）...")
    try:
        # 生成模拟预测数据
        predictions = [31.2, 31.8, 31.5, 32.1, 31.9, 32.5, 32.8]
        last_date = pd.to_datetime(test_data['date'].iloc[-1])
        prediction_dates = pd.date_range(start=last_date + timedelta(days=1), periods=7)
        
        visualizer.plot_prediction_results(
            test_data.tail(20),  # 最近20天的历史数据
            predictions,
            prediction_dates,
            '000001',
            stock_name,
            'd:/股票分析/test_prediction_improved.png'
        )
        print("✅ 预测结果图生成成功")
        print(f"   预测日期范围: {prediction_dates[0].strftime('%Y-%m-%d')} 至 {prediction_dates[-1].strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"❌ 预测结果图生成失败: {e}")
    
    print("\n🎉 所有可视化测试完成！")
    print("\n📁 生成的文件:")
    import os
    files = [
        'd:/股票分析/test_overview_improved.png',
        'd:/股票分析/test_interactive_improved.html', 
        'd:/股票分析/test_prediction_improved.png'
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (未生成)")

if __name__ == "__main__":
    test_improved_visualization()
