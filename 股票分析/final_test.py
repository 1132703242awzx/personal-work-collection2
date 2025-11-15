"""
最终测试改进的可视化功能
"""

from data_crawler import StockDataCrawler
from visualizer import StockVisualizer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def final_test():
    """最终测试"""
    print("🎯 最终测试改进的可视化功能")
    print("=" * 50)
    
    # 测试获取不同股票的名称
    crawler = StockDataCrawler()
    test_codes = ['000001', '600519', '600111', '601318', '300750']
    
    print('📝 测试股票名称获取功能:')
    for code in test_codes:
        name = crawler.get_stock_name(code)
        print(f'  {code}: {name}')
    
    print("\n📊 生成改进的可视化图表...")
    
    # 创建测试数据（模拟贵州茅台）
    dates = pd.date_range(start='2024-07-01', periods=30)
    np.random.seed(42)
    
    # 模拟茅台股价（基于1800元左右）
    base_price = 1800.0
    price_changes = np.random.normal(0, 0.01, 30)
    prices = [base_price]
    
    for change in price_changes[:-1]:
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1000.0))
    
    test_data = pd.DataFrame({
        'date': dates,
        'open': [p * (1 + np.random.normal(0, 0.003)) for p in prices],
        'close': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.008))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.008))) for p in prices],
        'volume': np.random.randint(100000, 1000000, 30),
        'amount': np.random.uniform(200000000, 2000000000, 30),
        'ma5': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
        'ma20': [p * (1 + np.random.normal(0, 0.001)) for p in prices],
        'rsi': np.random.uniform(30, 70, 30)
    })
    
    visualizer = StockVisualizer()
    stock_name = crawler.get_stock_name('600519')
    
    # 生成预测数据
    predictions = [1820, 1835, 1828, 1845, 1852, 1848, 1860]
    last_date = pd.to_datetime(test_data['date'].iloc[-1])
    prediction_dates = pd.date_range(start=last_date + timedelta(days=1), periods=7)
    
    # 1. 测试概览图
    print("📈 生成股票概览图（带名称和日期）...")
    try:
        visualizer.plot_stock_overview(
            test_data, '600519', stock_name,
            'd:/股票分析/茅台_概览图_最终版.png'
        )
        print("✅ 概览图生成成功")
    except Exception as e:
        print(f"❌ 概览图生成失败: {e}")
    
    # 2. 测试交互式图表
    print("🌐 生成交互式K线图（带名称和日期）...")
    try:
        visualizer.plot_interactive_kline(
            test_data, '600519', stock_name,
            'd:/股票分析/茅台_交互图_最终版.html'
        )
        print("✅ 交互式图表生成成功")
    except Exception as e:
        print(f"❌ 交互式图表生成失败: {e}")
    
    # 3. 测试预测图
    print("🔮 生成预测结果图（带名称和具体日期）...")
    try:
        visualizer.plot_prediction_results(
            test_data, predictions, prediction_dates,
            '600519', stock_name,
            'd:/股票分析/茅台_预测图_最终版.png'
        )
        print("✅ 预测图生成成功")
    except Exception as e:
        print(f"❌ 预测图生成失败: {e}")
    
    print("\n🎉 所有改进测试完成!")
    print(f"📊 股票信息: 600519 ({stock_name})")
    print(f"📅 预测日期范围: {prediction_dates[0].strftime('%Y-%m-%d')} 至 {prediction_dates[-1].strftime('%Y-%m-%d')}")
    
    print("\n✨ 改进内容总结:")
    print("1. ✅ 图表标题显示股票代码和名称")
    print("2. ✅ 图表副标题显示数据时间范围")
    print("3. ✅ X轴显示具体的日期")
    print("4. ✅ 预测图显示具体的预测日期")
    print("5. ✅ 交互式图表格式化日期显示")
    
    print("\n📁 生成的文件:")
    import os
    files = [
        'd:/股票分析/茅台_概览图_最终版.png',
        'd:/股票分析/茅台_交互图_最终版.html',
        'd:/股票分析/茅台_预测图_最终版.png'
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")

if __name__ == "__main__":
    final_test()
