"""
股票分析与预测系统
基于残差通道-空间注意力网络（R-CSAN）的股票预测系统
支持从东方财富和新浪财经获取股票数据，并预测未来7天的股价走势
"""

import os
import sys
import pandas as pd
import numpy as np
import torch
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 导入自定义模块
from data_crawler import StockDataCrawler
from rcsan_model import StockPredictor
from visualizer import StockVisualizer

class StockAnalysisSystem:
    """股票分析系统主类"""
    
    def __init__(self):
        self.crawler = StockDataCrawler()
        self.predictor = None
        self.visualizer = StockVisualizer()
        self.current_data = None
        self.current_stock_code = None
        self.current_stock_name = None
        
        print("=" * 60)
        print("🚀 股票分析与预测系统")
        print("🧠 基于残差通道-空间注意力网络（R-CSAN）")
        print("📊 支持东方财富 & 新浪财经数据")
        print("=" * 60)
    
    def get_stock_data(self, stock_code, days=200):
        """获取股票数据"""
        print(f"\n📈 正在获取股票 {stock_code} 的数据...")
        
        # 获取股票名称
        print("🔍 正在获取股票名称...")
        self.current_stock_name = self.crawler.get_stock_name(stock_code)
        print(f"📝 股票名称: {self.current_stock_name}")
        
        # 获取原始数据
        raw_data = self.crawler.get_stock_data(stock_code, days)
        
        if raw_data is None or len(raw_data) == 0:
            print("❌ 数据获取失败！")
            return False
        
        # 添加技术指标
        print("🔧 正在计算技术指标...")
        self.current_data = self.crawler.add_technical_indicators(raw_data)
        self.current_stock_code = stock_code
        
        print(f"✅ 成功获取 {len(self.current_data)} 条数据")
        print(f"📅 数据时间范围: {self.current_data['date'].min()} 至 {self.current_data['date'].max()}")
        
        return True
    
    def train_model(self, epochs=100, batch_size=32):
        """训练预测模型"""
        if self.current_data is None:
            print("❌ 请先获取股票数据！")
            return False
        
        print(f"\n🧠 开始训练R-CSAN模型...")
        
        # 创建预测器
        available_features = [col for col in [
            'open', 'high', 'low', 'close', 'volume', 'amount',
            'ma5', 'ma10', 'ma20', 'ma60', 'rsi', 'macd', 'macd_signal', 'macd_hist'
        ] if col in self.current_data.columns]
        
        self.predictor = StockPredictor(
            input_features=len(available_features),
            sequence_length=60,
            prediction_days=7
        )
        
        # 准备训练数据
        print("🔄 正在准备训练数据...")
        train_data = self.predictor.prepare_data(self.current_data)
        
        if train_data[0].shape[0] < 10:
            print("❌ 数据量不足，无法训练模型！")
            return False
        
        # 开始训练
        print(f"🎯 开始训练，数据量: {train_data[0].shape[0]} 样本")
        self.predictor.train(train_data, epochs=epochs, batch_size=batch_size)
        
        # 保存模型
        model_path = f"d:/股票分析/model_{self.current_stock_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pth"
        self.predictor.save_model(model_path)
        
        print("✅ 模型训练完成并已保存！")
        return True
    
    def predict_future(self, days=7):
        """预测未来股价"""
        if self.predictor is None:
            print("❌ 请先训练模型！")
            return None
        
        if self.current_data is None or len(self.current_data) < 60:
            print("❌ 数据不足，无法进行预测！")
            return None
        
        print(f"\n🔮 正在预测未来 {days} 天的股价...")
        
        # 准备输入数据（最近60天的数据）
        feature_columns = [col for col in [
            'open', 'high', 'low', 'close', 'volume', 'amount',
            'ma5', 'ma10', 'ma20', 'ma60', 'rsi', 'macd', 'macd_signal', 'macd_hist'
        ] if col in self.current_data.columns]
        
        recent_data = self.current_data[feature_columns].tail(60).fillna(method='bfill').fillna(method='ffill')
        
        # 数据标准化
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(recent_data)
        
        # 进行预测
        input_tensor = torch.FloatTensor(scaled_data).unsqueeze(0)  # 添加batch维度
        predictions = self.predictor.predict(input_tensor)
        
        # 生成预测日期
        last_date = pd.to_datetime(self.current_data['date'].iloc[-1])
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(len(predictions[0]))]
        
        print("✅ 预测完成！")
        
        return predictions[0], prediction_dates
    
    def generate_report(self):
        """生成分析报告"""
        if self.current_data is None:
            print("❌ 请先获取股票数据！")
            return
        
        print(f"\n📊 正在生成 {self.current_stock_code} 的分析报告...")
        
        # 获取预测结果
        predictions, prediction_dates = self.predict_future()
        
        if predictions is None:
            print("❌ 无法生成预测，跳过预测部分")
            predictions = []
            prediction_dates = []
        
        # 创建可视化
        print("🎨 正在生成图表...")
        
        # 1. 股票概览图
        overview_path = f"d:/股票分析/{self.current_stock_code}_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.visualizer.plot_stock_overview(self.current_data, self.current_stock_code, self.current_stock_name, overview_path)
        
        # 2. 交互式K线图
        interactive_path = f"d:/股票分析/{self.current_stock_code}_interactive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        self.visualizer.plot_interactive_kline(self.current_data, self.current_stock_code, self.current_stock_name, interactive_path)
        
        # 3. 预测结果图
        if len(predictions) > 0:
            prediction_path = f"d:/股票分析/{self.current_stock_code}_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.visualizer.plot_prediction_results(
                self.current_data.tail(30), predictions, prediction_dates, 
                self.current_stock_code, self.current_stock_name, prediction_path
            )
        
        # 4. 生成文本报告
        if len(predictions) > 0:
            report_path = f"d:/股票分析/{self.current_stock_code}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            stock_display_name = f"{self.current_stock_code} ({self.current_stock_name})" if self.current_stock_name else self.current_stock_code
            model_info = f"使用R-CSAN模型，基于最近{len(self.current_data)}天的历史数据训练"
            self.visualizer.create_prediction_report(
                self.current_data, predictions, stock_display_name, model_info, report_path
            )
        
        print("✅ 分析报告生成完成！")
    
    def run_interactive_mode(self):
        """运行交互模式"""
        while True:
            print("\n" + "=" * 50)
            print("📈 股票分析与预测系统")
            print("1. 获取股票数据")
            print("2. 训练预测模型")
            print("3. 预测未来股价")
            print("4. 生成完整报告")
            print("5. 查看当前数据")
            print("0. 退出系统")
            print("=" * 50)
            
            choice = input("请选择操作 (0-5): ").strip()
            
            if choice == '1':
                stock_code = input("请输入股票代码 (如: 000001): ").strip()
                days = input("请输入获取天数 (默认200天): ").strip()
                days = int(days) if days.isdigit() else 200
                
                self.get_stock_data(stock_code, days)
                
            elif choice == '2':
                if self.current_data is None:
                    print("❌ 请先获取股票数据！")
                    continue
                
                epochs = input("请输入训练轮数 (默认100): ").strip()
                epochs = int(epochs) if epochs.isdigit() else 100
                
                batch_size = input("请输入批次大小 (默认32): ").strip()
                batch_size = int(batch_size) if batch_size.isdigit() else 32
                
                self.train_model(epochs, batch_size)
                
            elif choice == '3':
                predictions, dates = self.predict_future()
                if predictions is not None:
                    print("\n🔮 预测结果:")
                    current_price = self.current_data['close'].iloc[-1]
                    for i, (pred, date) in enumerate(zip(predictions, dates)):
                        change = (pred - current_price) / current_price * 100
                        trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                        print(f"  第{i+1}天 ({date.strftime('%Y-%m-%d')}): ¥{pred:.2f} ({change:+.2f}%) {trend}")
                
            elif choice == '4':
                self.generate_report()
                
            elif choice == '5':
                if self.current_data is not None:
                    stock_display = f"{self.current_stock_code}"
                    if self.current_stock_name:
                        stock_display += f" ({self.current_stock_name})"
                    
                    print(f"\n📊 当前股票: {stock_display}")
                    print(f"📅 数据范围: {self.current_data['date'].min()} 至 {self.current_data['date'].max()}")
                    print(f"📈 数据量: {len(self.current_data)} 条")
                    print(f"💰 最新价格: ¥{self.current_data['close'].iloc[-1]:.2f}")
                    print("\n最近5天数据:")
                    print(self.current_data[['date', 'open', 'high', 'low', 'close', 'volume']].tail())
                else:
                    print("❌ 暂无数据")
                
            elif choice == '0':
                print("👋 感谢使用股票分析系统，再见！")
                break
                
            else:
                print("❌ 无效选择，请重试！")

def main():
    """主函数"""
    # 检查依赖包
    try:
        import torch
        import pandas as pd
        import numpy as np
        import requests
        import matplotlib.pyplot as plt
        print("✅ 所有依赖包检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return
    
    # 创建输出目录
    output_dir = "d:/股票分析"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建并运行系统
    system = StockAnalysisSystem()
    
    # 询问运行模式
    print("\n🚀 系统启动成功！")
    mode = input("选择运行模式 - 1: 交互模式, 2: 快速演示 (默认1): ").strip()
    
    if mode == '2':
        # 快速演示模式
        print("\n🎯 快速演示模式")
        demo_stock = input("请输入演示股票代码 (默认000001): ").strip() or "000001"
        
        # 获取数据
        if system.get_stock_data(demo_stock, 200):
            # 训练模型
            if system.train_model(epochs=50, batch_size=16):
                # 生成报告
                system.generate_report()
            else:
                print("❌ 演示失败：模型训练出错")
        else:
            print("❌ 演示失败：数据获取出错")
    else:
        # 交互模式
        system.run_interactive_mode()

if __name__ == '__main__':
    main()
