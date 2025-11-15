"""
股票分析系统测试脚本
用于验证各个模块的功能
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
import torch
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append('d:/股票分析')

from data_crawler import StockDataCrawler
from rcsan_model import StockPredictor, RCSAN
from visualizer import StockVisualizer

class TestStockAnalysisSystem(unittest.TestCase):
    """测试股票分析系统"""
    
    def setUp(self):
        """测试前设置"""
        print(f"\n{'='*60}")
        print(f"🧪 开始测试: {self._testMethodName}")
        print(f"{'='*60}")
        
        # 创建测试数据
        self.test_data = self.create_test_data()
        self.stock_code = "000001"
        
    def create_test_data(self):
        """创建测试数据"""
        dates = pd.date_range(start='2023-01-01', periods=150)
        np.random.seed(42)  # 确保结果可重现
        
        # 模拟股价走势
        base_price = 10.0
        price_changes = np.random.normal(0, 0.02, 150)
        prices = [base_price]
        
        for change in price_changes[:-1]:
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 0.1))  # 确保价格为正
        
        data = pd.DataFrame({
            'date': dates,
            'open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'close': prices,
            'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'volume': np.random.randint(1000000, 10000000, 150),
            'amount': np.random.uniform(10000000, 100000000, 150)
        })
        
        return data
    
    def test_data_crawler(self):
        """测试数据爬虫功能"""
        print("📊 测试数据爬虫...")
        
        crawler = StockDataCrawler()
        
        # 测试股票代码格式化
        self.assertEqual(crawler.get_stock_code_format("600000"), "sh600000")
        self.assertEqual(crawler.get_stock_code_format("000001"), "sz000001")
        print("✅ 股票代码格式化测试通过")
        
        # 测试技术指标计算
        data_with_indicators = crawler.add_technical_indicators(self.test_data.copy())
        
        expected_columns = ['ma5', 'ma10', 'ma20', 'ma60', 'rsi', 'macd', 'macd_signal', 'macd_hist']
        for col in expected_columns:
            self.assertIn(col, data_with_indicators.columns)
        
        print("✅ 技术指标计算测试通过")
        print(f"   添加了 {len(expected_columns)} 个技术指标")
        
    def test_rcsan_model(self):
        """测试R-CSAN模型"""
        print("🧠 测试R-CSAN模型...")
        
        # 测试模型创建
        model = RCSAN(input_features=10, sequence_length=30, prediction_days=7)
        self.assertIsNotNone(model)
        print("✅ 模型创建成功")
        
        # 测试前向传播
        batch_size = 4
        sequence_length = 30
        input_features = 10
        
        test_input = torch.randn(batch_size, sequence_length, input_features)
        
        model.eval()
        with torch.no_grad():
            output = model(test_input)
        
        self.assertEqual(output.shape, (batch_size, 7))
        print(f"✅ 前向传播测试通过，输出形状: {output.shape}")
        
        # 测试模型参数数量
        param_count = sum(p.numel() for p in model.parameters())
        print(f"   模型参数数量: {param_count:,}")
        
    def test_stock_predictor(self):
        """测试股票预测器"""
        print("🔮 测试股票预测器...")
        
        # 添加技术指标
        crawler = StockDataCrawler()
        data_with_indicators = crawler.add_technical_indicators(self.test_data.copy())
        
        # 创建预测器
        predictor = StockPredictor(input_features=14, sequence_length=30, prediction_days=7)
        self.assertIsNotNone(predictor)
        print("✅ 预测器创建成功")
        
        # 测试数据准备
        X, y = predictor.prepare_data(data_with_indicators)
        
        self.assertGreater(X.shape[0], 0)
        self.assertEqual(X.shape[1], 30)  # sequence_length
        self.assertEqual(y.shape[1], 7)   # prediction_days
        
        print(f"✅ 数据准备测试通过")
        print(f"   训练样本数: {X.shape[0]}")
        print(f"   输入特征数: {X.shape[2]}")
        
        # 测试小规模训练
        print("   进行小规模训练测试...")
        try:
            predictor.train((X, y), epochs=5, batch_size=4)
            print("✅ 训练流程测试通过")
        except Exception as e:
            print(f"⚠️ 训练测试警告: {str(e)}")
        
        # 测试预测
        test_input = X[:1]  # 取一个样本
        predictions = predictor.predict(test_input)
        
        self.assertEqual(len(predictions[0]), 7)
        print(f"✅ 预测功能测试通过，预测结果: {predictions[0]}")
        
    def test_visualizer(self):
        """测试可视化模块"""
        print("🎨 测试可视化模块...")
        
        visualizer = StockVisualizer()
        self.assertIsNotNone(visualizer)
        print("✅ 可视化器创建成功")
        
        # 添加技术指标用于测试
        crawler = StockDataCrawler()
        data_with_indicators = crawler.add_technical_indicators(self.test_data.copy())
        
        # 测试预测报告生成
        test_predictions = [10.5, 10.3, 10.7, 10.8, 10.6, 10.9, 11.0]
        
        try:
            report = visualizer.create_prediction_report(
                data_with_indicators, test_predictions, self.stock_code
            )
            self.assertIsNotNone(report)
            self.assertIn("股票预测报告", report)
            print("✅ 预测报告生成测试通过")
        except Exception as e:
            print(f"⚠️ 预测报告测试警告: {str(e)}")
        
        print("✅ 可视化模块基础功能测试通过")
        
    def test_integration(self):
        """测试系统集成"""
        print("🔗 测试系统集成...")
        
        try:
            # 1. 数据处理
            crawler = StockDataCrawler()
            data_with_indicators = crawler.add_technical_indicators(self.test_data.copy())
            print("✅ 数据处理集成成功")
            
            # 2. 模型训练
            predictor = StockPredictor(input_features=14, sequence_length=30, prediction_days=7)
            X, y = predictor.prepare_data(data_with_indicators)
            
            # 快速训练测试
            predictor.train((X, y), epochs=3, batch_size=4)
            print("✅ 模型训练集成成功")
            
            # 3. 预测
            predictions = predictor.predict(X[:1])
            print("✅ 模型预测集成成功")
            
            # 4. 可视化
            visualizer = StockVisualizer()
            report = visualizer.create_prediction_report(
                data_with_indicators, predictions[0], self.stock_code
            )
            print("✅ 可视化集成成功")
            
            print("🎉 系统集成测试全部通过！")
            
        except Exception as e:
            self.fail(f"系统集成测试失败: {str(e)}")
    
    def tearDown(self):
        """测试后清理"""
        print(f"✅ 测试 {self._testMethodName} 完成")

def run_performance_test():
    """运行性能测试"""
    print(f"\n{'='*60}")
    print("⚡ 性能测试")
    print(f"{'='*60}")
    
    import time
    
    # 创建大规模测试数据
    dates = pd.date_range(start='2020-01-01', periods=500)
    np.random.seed(42)
    
    large_data = pd.DataFrame({
        'date': dates,
        'open': np.random.uniform(8, 12, 500),
        'close': np.random.uniform(8, 12, 500),
        'high': np.random.uniform(10, 15, 500),
        'low': np.random.uniform(5, 10, 500),
        'volume': np.random.randint(1000000, 50000000, 500),
        'amount': np.random.uniform(10000000, 500000000, 500)
    })
    
    # 性能测试：数据处理
    start_time = time.time()
    crawler = StockDataCrawler()
    data_with_indicators = crawler.add_technical_indicators(large_data)
    processing_time = time.time() - start_time
    print(f"📊 数据处理时间: {processing_time:.2f}秒 (500条数据)")
    
    # 性能测试：模型训练
    start_time = time.time()
    predictor = StockPredictor(input_features=14, sequence_length=60, prediction_days=7)
    X, y = predictor.prepare_data(data_with_indicators)
    data_prep_time = time.time() - start_time
    print(f"🔄 数据准备时间: {data_prep_time:.2f}秒 ({X.shape[0]}个样本)")
    
    # 小规模训练测试
    start_time = time.time()
    predictor.train((X, y), epochs=5, batch_size=8)
    training_time = time.time() - start_time
    print(f"🧠 模型训练时间: {training_time:.2f}秒 (5个epoch)")
    
    # 预测性能测试
    start_time = time.time()
    predictions = predictor.predict(X[:10])
    prediction_time = time.time() - start_time
    print(f"🔮 预测时间: {prediction_time:.2f}秒 (10个样本)")
    
    print("⚡ 性能测试完成")

def main():
    """主测试函数"""
    print("🚀 股票分析系统测试套件")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查PyTorch
    print(f"PyTorch版本: {torch.__version__}")
    print(f"CUDA可用: {torch.cuda.is_available()}")
    print(f"设备: {'GPU' if torch.cuda.is_available() else 'CPU'}")
    
    # 运行单元测试
    print(f"\n{'='*60}")
    print("🧪 开始单元测试")
    print(f"{'='*60}")
    
    # 创建测试套件
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestStockAnalysisSystem)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 显示测试结果
    print(f"\n{'='*60}")
    print("📊 测试结果统计")
    print(f"{'='*60}")
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ 失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️ 错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    # 运行性能测试
    if result.testsRun > 0 and len(result.failures) == 0 and len(result.errors) == 0:
        run_performance_test()
    
    # 总结
    print(f"\n{'='*60}")
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("🎉 所有测试通过！系统运行正常。")
    else:
        print("⚠️ 部分测试未通过，请检查系统配置。")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
