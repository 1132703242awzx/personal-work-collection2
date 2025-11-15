# 股票分析与预测系统配置文件

# 模型参数
MODEL_CONFIG = {
    'sequence_length': 60,      # 输入序列长度（天数）
    'prediction_days': 7,       # 预测天数
    'hidden_dim': 128,          # 隐藏层维度
    'num_layers': 4,            # 网络层数
    'num_heads': 8,             # 注意力头数
    'dropout': 0.1,             # Dropout率
    'learning_rate': 1e-3,      # 学习率
    'weight_decay': 1e-5,       # 权重衰减
    'batch_size': 32,           # 批次大小
    'epochs': 100,              # 训练轮数
}

# 数据获取配置
DATA_CONFIG = {
    'default_days': 200,        # 默认获取天数
    'min_data_length': 100,     # 最小数据长度
    'max_retries': 3,           # 最大重试次数
    'timeout': 10,              # 请求超时时间
}

# 技术指标配置
INDICATOR_CONFIG = {
    'ma_periods': [5, 10, 20, 60],  # 移动平均线周期
    'rsi_period': 14,               # RSI周期
    'macd_fast': 12,                # MACD快线
    'macd_slow': 26,                # MACD慢线
    'macd_signal': 9,               # MACD信号线
    'bb_period': 20,                # 布林带周期
    'bb_std': 2,                    # 布林带标准差倍数
}

# 可视化配置
PLOT_CONFIG = {
    'figsize': (15, 10),        # 图表大小
    'dpi': 300,                 # 图片分辨率
    'style': 'seaborn',         # 图表样式
    'colors': {
        'up': '#ff4757',        # 上涨颜色
        'down': '#2ed573',      # 下跌颜色
        'volume': '#3742fa',    # 成交量颜色
        'ma': '#ffa502',        # 均线颜色
        'prediction': '#ff6348' # 预测线颜色
    }
}

# API配置
API_CONFIG = {
    'eastmoney': {
        'base_url': 'https://push2his.eastmoney.com/api/qt/stock/kline/get',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    },
    'sina': {
        'base_url': 'https://hq.sinajs.cn/list=',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
}

# 文件路径配置
PATH_CONFIG = {
    'data_dir': 'd:/股票分析/data',
    'model_dir': 'd:/股票分析/models',
    'output_dir': 'd:/股票分析/output',
    'log_dir': 'd:/股票分析/logs',
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'd:/股票分析/logs/system.log'
}
