import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import warnings
warnings.filterwarnings('ignore')

class StockDataCrawler:
    """股票数据爬虫类，支持从东方财富和新浪财经获取数据"""
    
    def __init__(self):
        self.eastmoney_base_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        self.sina_base_url = "https://hq.sinajs.cn/list="
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 常见股票名称字典
        self.stock_names = {
            '000001': '平安银行',
            '000002': '万科A', 
            '000858': '五粮液',
            '600000': '浦发银行',
            '600036': '招商银行',
            '600519': '贵州茅台',
            '600111': '北方稀土',
            '000858': '五粮液',
            '002415': '海康威视',
            '300059': '东方财富',
            '601318': '中国平安',
            '601398': '工商银行',
            '601166': '兴业银行',
            '600887': '伊利股份',
            '000568': '泸州老窖',
            '002304': '洋河股份',
            '600276': '恒瑞医药',
            '300750': '宁德时代',
            '002594': '比亚迪',
            '601012': '隆基绿能'
        }
    
    def get_stock_code_format(self, stock_code):
        """格式化股票代码"""
        if stock_code.startswith('6'):
            return f"sh{stock_code}"  # 上海交易所
        elif stock_code.startswith(('0', '3')):
            return f"sz{stock_code}"  # 深圳交易所
        else:
            return stock_code
    
    def get_stock_name(self, stock_code):
        """获取股票名称"""
        # 首先检查本地字典
        if stock_code in self.stock_names:
            return self.stock_names[stock_code]
        
        try:
            # 从新浪获取股票名称
            formatted_code = self.get_stock_code_format(stock_code)
            url = f"{self.sina_base_url}{formatted_code}"
            
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                content = response.text
                if content and 'var hq_str_' in content:
                    data_str = content.split('="')[1].split('";')[0]
                    data_parts = data_str.split(',')
                    
                    if len(data_parts) >= 1 and data_parts[0] and data_parts[0] != '':
                        stock_name = data_parts[0].strip()
                        if stock_name and stock_name != stock_code:
                            # 缓存获取到的名称
                            self.stock_names[stock_code] = stock_name
                            return stock_name
            
            # 如果新浪获取失败，返回默认名称
            return f"股票{stock_code}"
            
        except Exception as e:
            print(f"获取股票名称失败: {str(e)}")
            return f"股票{stock_code}"
    
    def crawl_eastmoney_data(self, stock_code, days=200):
        """从东方财富获取股票历史数据"""
        try:
            # 计算开始日期
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # 格式化股票代码
            if stock_code.startswith('6'):
                secid = f"1.{stock_code}"  # 上海
            else:
                secid = f"0.{stock_code}"  # 深圳
            
            params = {
                'secid': secid,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'fields1': 'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt': '101',  # 日K线
                'fqt': '1',    # 前复权
                'beg': start_date.strftime('%Y%m%d'),
                'end': end_date.strftime('%Y%m%d'),
                '_': str(int(time.time() * 1000))
            }
            
            response = self.session.get(self.eastmoney_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and data['data'] and 'klines' in data['data']:
                    klines = data['data']['klines']
                    df_data = []
                    
                    for kline in klines:
                        parts = kline.split(',')
                        if len(parts) >= 11:
                            df_data.append({
                                'date': parts[0],
                                'open': float(parts[1]),
                                'close': float(parts[2]),
                                'high': float(parts[3]),
                                'low': float(parts[4]),
                                'volume': float(parts[5]),
                                'amount': float(parts[6]),
                                'amplitude': float(parts[7]),
                                'change_pct': float(parts[8]),
                                'change': float(parts[9]),
                                'turnover': float(parts[10])
                            })
                    
                    df = pd.DataFrame(df_data)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    print(f"成功从东方财富获取到 {len(df)} 条数据")
                    return df
                
            print("东方财富API返回数据格式异常")
            return None
            
        except Exception as e:
            print(f"从东方财富获取数据失败: {str(e)}")
            return None
    
    def crawl_sina_data(self, stock_code, days=200):
        """从新浪财经获取股票数据（作为备用）"""
        try:
            formatted_code = self.get_stock_code_format(stock_code)
            url = f"{self.sina_base_url}{formatted_code}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                if content and 'var hq_str_' in content:
                    data_str = content.split('="')[1].split('";')[0]
                    data_parts = data_str.split(',')
                    
                    if len(data_parts) >= 32:
                        current_data = {
                            'name': data_parts[0],
                            'open': float(data_parts[1]) if data_parts[1] else 0,
                            'close_yesterday': float(data_parts[2]) if data_parts[2] else 0,
                            'close': float(data_parts[3]) if data_parts[3] else 0,
                            'high': float(data_parts[4]) if data_parts[4] else 0,
                            'low': float(data_parts[5]) if data_parts[5] else 0,
                            'volume': float(data_parts[8]) if data_parts[8] else 0,
                            'amount': float(data_parts[9]) if data_parts[9] else 0,
                            'date': data_parts[30],
                            'time': data_parts[31]
                        }
                        
                        print(f"成功从新浪财经获取到当前数据: {current_data['name']}")
                        return pd.DataFrame([current_data])
                
            print("新浪财经API返回数据格式异常")
            return None
            
        except Exception as e:
            print(f"从新浪财经获取数据失败: {str(e)}")
            return None
    
    def get_stock_data(self, stock_code, days=200):
        """获取股票数据的主方法"""
        print(f"正在获取股票 {stock_code} 最近 {days} 天的数据...")
        
        # 首先尝试从东方财富获取数据
        df = self.crawl_eastmoney_data(stock_code, days)
        
        if df is not None and len(df) > 0:
            return df
        
        # 如果东方财富失败，尝试新浪财经
        print("尝试从新浪财经获取数据...")
        df = self.crawl_sina_data(stock_code, days)
        
        if df is not None and len(df) > 0:
            print("警告: 仅获取到当前数据，历史数据获取失败")
            return df
        
        print("所有数据源都无法获取数据")
        return None
    
    def add_technical_indicators(self, df):
        """添加技术指标"""
        if df is None or len(df) == 0:
            return df
        
        # 移动平均线
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma60'] = df['close'].rolling(window=60).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12).mean()
        exp2 = df['close'].ewm(span=26).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # 布林带
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        return df

if __name__ == "__main__":
    # 测试数据爬虫
    crawler = StockDataCrawler()
    
    # 测试获取平安银行数据
    stock_data = crawler.get_stock_data("000001", days=200)
    
    if stock_data is not None:
        # 添加技术指标
        stock_data = crawler.add_technical_indicators(stock_data)
        print(f"数据形状: {stock_data.shape}")
        print("\n数据预览:")
        print(stock_data.head())
        print("\n数据列:")
        print(stock_data.columns.tolist())
    else:
        print("数据获取失败")
