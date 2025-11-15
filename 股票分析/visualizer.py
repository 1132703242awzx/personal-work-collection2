import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和美化样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['savefig.edgecolor'] = 'none'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'
plt.rcParams['text.color'] = '#333333'
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['grid.linewidth'] = 0.8
plt.rcParams['grid.alpha'] = 0.7

# 设置seaborn样式
sns.set_style("whitegrid", {
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "grid.linewidth": 0.8,
    "grid.color": "#e0e0e0",
    "grid.alpha": 0.7
})

class StockVisualizer:
    """股票数据可视化类"""
    
    def __init__(self):
        # 更丰富的配色方案
        self.colors = {
            'up': '#f55353',         # 上涨红色 - 更柔和
            'down': '#00d4aa',       # 下跌绿色 - 更现代
            'volume_up': '#ff8a80',  # 上涨成交量
            'volume_down': '#69f0ae', # 下跌成交量
            'ma5': '#ff6b35',        # MA5 - 橙色
            'ma10': '#7b68ee',       # MA10 - 紫色
            'ma20': '#ffa726',       # MA20 - 深橙色
            'ma60': '#42a5f5',       # MA60 - 蓝色
            'rsi': '#ab47bc',        # RSI - 紫色
            'macd': '#26c6da',       # MACD - 青色
            'prediction': '#ff5722', # 预测线 - 深橙红色
            'background': '#fafafa', # 背景色
            'grid': '#e8e8e8',       # 网格线
            'text': '#37474f',       # 文字颜色
            'border': '#bdbdbd'      # 边框颜色
        }
        
        # 渐变色配置
        self.gradients = {
            'up': ['#ffcdd2', '#f55353'],
            'down': ['#c8e6c9', '#00d4aa'],
            'volume': ['#e1f5fe', '#0277bd']
        }
    
    def get_stock_name_dict(self):
        """获取股票名称字典"""
        return {
            '000001': '平安银行',
            '000002': '万科A', 
            '000858': '五粮液',
            '600000': '浦发银行',
            '600036': '招商银行',
            '600519': '贵州茅台',
            '600111': '北方稀土',
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

    def plot_stock_overview(self, data, stock_code="未知股票", stock_name="", save_path=None):
        """绘制股票概览图 - 修复版本，去除方框，显示股票名称"""
        # 创建清晰的子图布局
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        # 使用GridSpec创建布局
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig, height_ratios=[2, 1.5, 1.5], hspace=0.35, wspace=0.25)
        
        # 获取股票名称和日期范围
        if not stock_name and stock_code in self.get_stock_name_dict():
            stock_name = self.get_stock_name_dict()[stock_code]
        
        title_text = f'{stock_code}'
        if stock_name:
            title_text += f' ({stock_name})'
        title_text += ' 股票数据概览'
        
        if 'date' in data.columns:
            start_date = pd.to_datetime(data['date'].iloc[0]).strftime('%Y-%m-%d')
            end_date = pd.to_datetime(data['date'].iloc[-1]).strftime('%Y-%m-%d')
            subtitle = f'数据时间: {start_date} 至 {end_date} | 共 {len(data)} 个交易日'
        else:
            subtitle = f'共 {len(data)} 个交易日数据'
        
        # 主标题
        fig.suptitle(title_text, fontsize=18, fontweight='bold', 
                    color='#333333', y=0.95)
        fig.text(0.5, 0.92, subtitle, ha='center', va='center', 
                fontsize=12, color='#666666', style='italic')
        
        # 1. K线图 - 占据上方整行
        ax1 = fig.add_subplot(gs[0, :])
        dates_range = range(len(data))
        
        # 绘制K线图
        for i in range(len(data)):
            open_price = data.iloc[i]['open']
            close_price = data.iloc[i]['close']
            high_price = data.iloc[i]['high']
            low_price = data.iloc[i]['low']
            
            # 确定颜色
            color = self.colors['up'] if close_price >= open_price else self.colors['down']
            
            # 绘制高低线
            ax1.plot([i, i], [low_price, high_price], color=color, linewidth=1.5, alpha=0.8)
            
            # 绘制实体矩形
            height = abs(close_price - open_price)
            bottom = min(open_price, close_price)
            rect = plt.Rectangle((i-0.3, bottom), 0.6, height, 
                               facecolor=color, edgecolor=color, alpha=0.8, linewidth=0)
            ax1.add_patch(rect)
        
        # 添加移动平均线
        if 'ma5' in data.columns:
            ax1.plot(dates_range, data['ma5'], color=self.colors['ma5'], 
                    linewidth=2, alpha=0.8, label='MA5', linestyle='-')
        if 'ma10' in data.columns:
            ax1.plot(dates_range, data['ma10'], color=self.colors['ma10'], 
                    linewidth=2, alpha=0.8, label='MA10', linestyle='-')
        if 'ma20' in data.columns:
            ax1.plot(dates_range, data['ma20'], color=self.colors['ma20'], 
                    linewidth=2, alpha=0.8, label='MA20', linestyle='-')
        
        ax1.set_title('K线图与移动平均线', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylabel('价格 (元)', fontsize=12)
        
        # 设置x轴标签
        if 'date' in data.columns:
            # 选择合适的日期标签间隔
            interval = max(1, len(data) // 10)
            tick_positions = range(0, len(data), interval)
            tick_labels = [pd.to_datetime(data['date'].iloc[i]).strftime('%m-%d') 
                          for i in tick_positions]
            ax1.set_xticks(tick_positions)
            ax1.set_xticklabels(tick_labels, rotation=45)
        
        # 图例
        ax1.legend(loc='upper left', frameon=False, fontsize=10)
        self._beautify_axis_simple(ax1)
        
        # 2. 成交量图
        ax2 = fig.add_subplot(gs[1, 0])
        volume_colors = [self.colors['up'] if data.iloc[i]['close'] >= data.iloc[i]['open'] 
                        else self.colors['down'] for i in range(len(data))]
        
        bars = ax2.bar(dates_range, data['volume'], color=volume_colors, alpha=0.7, width=0.8)
        ax2.set_title('成交量', fontsize=14, fontweight='bold')
        ax2.set_ylabel('成交量', fontsize=12)
        
        # 格式化成交量显示
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(self._format_volume))
        
        if 'date' in data.columns:
            ax2.set_xticks(tick_positions)
            ax2.set_xticklabels(tick_labels, rotation=45)
        
        self._beautify_axis_simple(ax2)
        
        # 3. RSI指标
        ax3 = fig.add_subplot(gs[1, 1])
        if 'rsi' in data.columns:
            ax3.plot(dates_range, data['rsi'], color=self.colors['rsi'], linewidth=2)
            ax3.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线(70)')
            ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线(30)')
            ax3.fill_between(dates_range, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(dates_range, 0, 30, alpha=0.1, color='green')
            
        ax3.set_title('RSI相对强弱指标', fontsize=14, fontweight='bold')
        ax3.set_ylabel('RSI', fontsize=12)
        ax3.set_ylim(0, 100)
        
        if 'date' in data.columns:
            ax3.set_xticks(tick_positions)
            ax3.set_xticklabels(tick_labels, rotation=45)
            
        ax3.legend(frameon=False, fontsize=10)
        self._beautify_axis_simple(ax3)
        
        # 4. MACD指标
        ax4 = fig.add_subplot(gs[2, :])
        if all(col in data.columns for col in ['macd', 'macd_signal', 'macd_hist']):
            # MACD线
            ax4.plot(dates_range, data['macd'], color=self.colors['macd'], 
                    linewidth=2, label='MACD', alpha=0.8)
            # 信号线
            ax4.plot(dates_range, data['macd_signal'], color='orange', 
                    linewidth=2, label='Signal', alpha=0.8)
            # 柱状图
            colors = [self.colors['up'] if x > 0 else self.colors['down'] 
                     for x in data['macd_hist']]
            ax4.bar(dates_range, data['macd_hist'], color=colors, 
                   alpha=0.6, width=0.8, label='Histogram')
        
        ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax4.set_title('MACD指标', fontsize=14, fontweight='bold')
        ax4.set_ylabel('MACD', fontsize=12)
        ax4.set_xlabel('交易日期', fontsize=12)
        
        if 'date' in data.columns:
            ax4.set_xticks(tick_positions)
            ax4.set_xticklabels(tick_labels, rotation=45)
            
        ax4.legend(frameon=False, fontsize=10)
        self._beautify_axis_simple(ax4)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
        
        return fig
    
    def _beautify_axis_simple(self, ax):
        """简化的坐标轴美化，确保网格和坐标轴清晰可见"""
        # 设置清晰的网格
        ax.grid(True, alpha=0.7, color='#e0e0e0', linewidth=0.8, linestyle='-')
        ax.set_axisbelow(True)
        
        # 设置坐标轴边框 - 只保留左边和底边
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        
        # 设置边框颜色和粗细
        ax.spines['left'].set_color('#333333')
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_linewidth(1.0)
        ax.spines['bottom'].set_linewidth(1.0)
        
        # 设置刻度样式
        ax.tick_params(colors='#333333', labelsize=10, width=1.0, length=4)
        ax.tick_params(axis='x', colors='#333333', labelsize=10, rotation=0)
        ax.tick_params(axis='y', colors='#333333', labelsize=10)
        
        # 确保背景为白色，去除任何方框
        ax.set_facecolor('white')
        
        # 移除图例的边框
        legend = ax.get_legend()
        if legend:
            legend.get_frame().set_linewidth(0)
            legend.get_frame().set_facecolor('white')
            legend.get_frame().set_alpha(0.9)
    
    def _beautify_axis(self, ax, data, show_xlabel=False):
        """美化坐标轴"""
        # 设置网格
        ax.grid(True, alpha=0.3, color=self.colors['grid'], linewidth=0.5)
        ax.set_axisbelow(True)
        
        # 设置边框
        for spine in ax.spines.values():
            spine.set_color(self.colors['border'])
            spine.set_linewidth(0.8)
        
        # 设置刻度
        ax.tick_params(colors=self.colors['text'], labelsize=10)
        
        # 设置x轴日期标签
        if 'date' in data.columns and len(data) > 0:
            step = max(1, len(data) // 8)  # 显示8个日期点
            tick_positions = range(0, len(data), step)
            if len(tick_positions) > 0 and tick_positions[-1] < len(data) - 1:
                tick_positions = list(tick_positions) + [len(data) - 1]
            
            tick_labels = [pd.to_datetime(data['date'].iloc[i]).strftime('%m-%d') 
                          for i in tick_positions]
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(tick_labels, rotation=45)
        
        if show_xlabel:
            ax.set_xlabel('交易日期', fontsize=12, color=self.colors['text'])
    
    def _format_volume(self, x, pos):
        """格式化成交量显示"""
        if x >= 1e8:
            return f'{x/1e8:.1f}亿'
        elif x >= 1e4:
            return f'{x/1e4:.1f}万'
        else:
            return f'{x:.0f}'
    
    def plot_interactive_kline(self, data, stock_code="未知股票", stock_name="", save_path=None):
        """绘制交互式K线图 - 改进版，增强hover功能和坐标显示"""
        # 创建子图布局
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            subplot_titles=('K线图与移动平均线', '成交量', 'RSI相对强弱指标', 'MACD指标'),
            row_heights=[0.5, 0.2, 0.15, 0.15]
        )
        
        # 准备数据和标题
        dates = pd.to_datetime(data['date']) if 'date' in data.columns else pd.date_range(start='2023-01-01', periods=len(data))
        
        # 获取股票名称
        if not stock_name and stock_code in self.get_stock_name_dict():
            stock_name = self.get_stock_name_dict()[stock_code]
        
        title_text = f'{stock_code}'
        if stock_name:
            title_text += f' ({stock_name})'
        title_text += ' 交互式分析图表'
        
        if 'date' in data.columns:
            start_date = pd.to_datetime(data['date'].iloc[0]).strftime('%Y年%m月%d日')
            end_date = pd.to_datetime(data['date'].iloc[-1]).strftime('%Y年%m月%d日')
            title_text += f'<br><sub style="color: #666;">数据时间: {start_date} 至 {end_date}</sub>'
        
        # 1. K线图 - 增强hover信息
        fig.add_trace(
            go.Candlestick(
                x=dates,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name='K线',
                increasing_line_color='#f55353',
                decreasing_line_color='#00d4aa',
                increasing_fillcolor='#f55353',
                decreasing_fillcolor='#00d4aa',
                line_width=1,
                text=[f'开盘:{o:.2f}<br>最高:{h:.2f}<br>最低:{l:.2f}<br>收盘:{c:.2f}' 
                      for o,h,l,c in zip(data['open'], data['high'], data['low'], data['close'])]
            ),
            row=1, col=1
        )
        
        # 添加移动平均线 - 增强hover信息
        if 'ma5' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=dates, y=data['ma5'], 
                    name='MA5', 
                    line=dict(color='#ff6b35', width=2),
                    hovertemplate='<b>MA5</b><br>%{x}<br>价格: %{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
        
        if 'ma10' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=dates, y=data['ma10'], 
                    name='MA10', 
                    line=dict(color='#7b68ee', width=2),
                    hovertemplate='<b>MA10</b><br>%{x}<br>价格: %{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
        
        if 'ma20' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=dates, y=data['ma20'], 
                    name='MA20', 
                    line=dict(color='#ffa726', width=2),
                    hovertemplate='<b>MA20</b><br>%{x}<br>价格: %{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
        
        # 2. 成交量 - 增强hover信息
        volume_colors = ['#f55353' if data.iloc[i]['close'] >= data.iloc[i]['open'] 
                        else '#00d4aa' for i in range(len(data))]
        
        fig.add_trace(
            go.Bar(
                x=dates, 
                y=data['volume'], 
                name='成交量',
                marker_color=volume_colors,
                hovertemplate='<b>成交量</b><br>%{x}<br>成交量: %{y:,.0f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 3. RSI指标 - 增强hover信息
        if 'rsi' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=dates, y=data['rsi'], 
                    name='RSI',
                    line=dict(color='#ab47bc', width=2),
                    hovertemplate='<b>RSI</b><br>%{x}<br>RSI: %{y:.2f}<extra></extra>'
                ),
                row=3, col=1
            )
            
            # 添加RSI参考线
            fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.7, row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.7, row=3, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="gray", opacity=0.5, row=3, col=1)
        
        # 4. MACD指标 - 增强hover信息
        if all(col in data.columns for col in ['macd', 'macd_signal', 'macd_hist']):
            # MACD柱状图
            colors = ['#f55353' if x >= 0 else '#00d4aa' for x in data['macd_hist']]
            fig.add_trace(
                go.Bar(
                    x=dates, y=data['macd_hist'], 
                    name='MACD柱状图',
                    marker_color=colors,
                    hovertemplate='<b>MACD柱状图</b><br>%{x}<br>数值: %{y:.4f}<extra></extra>'
                ),
                row=4, col=1
            )
            
            # MACD线
            fig.add_trace(
                go.Scatter(
                    x=dates, y=data['macd'], 
                    name='MACD线',
                    line=dict(color='#26c6da', width=2),
                    hovertemplate='<b>MACD线</b><br>%{x}<br>数值: %{y:.4f}<extra></extra>'
                ),
                row=4, col=1
            )
            
            # 信号线
            fig.add_trace(
                go.Scatter(
                    x=dates, y=data['macd_signal'], 
                    name='信号线',
                    line=dict(color='#ff7043', width=2),
                    hovertemplate='<b>信号线</b><br>%{x}<br>数值: %{y:.4f}<extra></extra>'
                ),
                row=4, col=1
            )
            
            # 零轴线
            fig.add_hline(y=0, line_color="black", opacity=0.3, row=4, col=1)
        
        # 更新布局 - 增强可读性和交互性
        fig.update_layout(
            title={
                'text': title_text,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#333333'}
            },
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1
            ),
            margin=dict(l=50, r=50, t=100, b=50),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='x unified',
            # 添加缩放和平移工具
            dragmode='zoom'
        )
        
        # 更新x轴格式
        fig.update_xaxes(
            title_text="交易日期",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(224,224,224,0.7)',
            showline=True,
            linewidth=1,
            linecolor='#333333',
            tickformat='%Y-%m-%d',
            row=4, col=1
        )
        
        # 更新y轴格式
        for i in range(1, 5):
            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(224,224,224,0.7)',
                showline=True,
                linewidth=1,
                linecolor='#333333',
                row=i, col=1
            )
        
        # 设置y轴标题
        fig.update_yaxes(title_text="价格 (元)", row=1, col=1)
        fig.update_yaxes(title_text="成交量", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        fig.update_yaxes(title_text="MACD", row=4, col=1)
        
        # 设置RSI的范围
        fig.update_yaxes(range=[0, 100], row=3, col=1)
        
        # 添加工具栏配置
        config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'{stock_code}_interactive',
                'height': 800,
                'width': 1200,
                'scale': 2
            }
        }
        
        if save_path:
            fig.write_html(save_path, config=config)
            print(f"交互式图表已保存到: {save_path}")
        else:
            fig.show(config=config)
        
        return fig
    
    def plot_prediction_results(self, historical_data, predictions, prediction_dates=None, 
                              stock_code="未知股票", stock_name="", save_path=None):
        """绘制预测结果"""
        # 创建更美观的布局
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor('white')
        
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig, height_ratios=[2, 1, 1], hspace=0.35, wspace=0.25)
        
        # 生成标题
        title_text = f'{stock_code}'
        if stock_name:
            title_text += f' ({stock_name})'
        title_text += ' 股价预测分析'
        
        if 'date' in historical_data.columns:
            last_date = pd.to_datetime(historical_data['date'].iloc[-1]).strftime('%Y年%m月%d日')
            subtitle = f'基于截至 {last_date} 的历史数据预测未来7个交易日'
        else:
            subtitle = '基于历史数据的未来7日预测分析'
        
        # 主标题
        fig.suptitle(title_text, fontsize=18, fontweight='bold', 
                    color=self.colors['text'], y=0.95)
        fig.text(0.5, 0.92, subtitle, ha='center', va='center', 
                fontsize=12, color='#666666', style='italic')
        
        # 历史数据
        hist_dates = pd.to_datetime(historical_data['date']) if 'date' in historical_data.columns else range(len(historical_data))
        
        # 预测日期
        if prediction_dates is None:
            if 'date' in historical_data.columns:
                last_date = pd.to_datetime(historical_data['date'].iloc[-1])
                prediction_dates = pd.date_range(start=last_date + timedelta(days=1), periods=len(predictions))
            else:
                prediction_dates = range(len(historical_data), len(historical_data) + len(predictions))
        
        # 1. 主预测图 - 占据上方整行
        ax1 = fig.add_subplot(gs[0, :])
        
        # 绘制历史数据 - 使用渐变效果
        if 'date' in historical_data.columns:
            ax1.plot(hist_dates, historical_data['close'], 
                    color=self.colors['ma20'], linewidth=2.5, alpha=0.8,
                    label='历史收盘价', marker='o', markersize=3, markevery=5)
            
            # 添加历史数据的填充区域
            ax1.fill_between(hist_dates, historical_data['close'], alpha=0.1, 
                           color=self.colors['ma20'])
            
            # 绘制预测数据 - 使用醒目的样式
            pred_line = ax1.plot(prediction_dates, predictions, 
                               color=self.colors['prediction'], linewidth=3.5, 
                               label='预测收盘价', marker='o', markersize=6,
                               markerfacecolor='white', markeredgewidth=2)
            
            # 添加预测区间的阴影
            ax1.fill_between(prediction_dates, predictions, alpha=0.2, 
                           color=self.colors['prediction'])
            
            # 连接线 - 使用虚线
            if len(hist_dates) > 0 and len(prediction_dates) > 0:
                ax1.plot([hist_dates.iloc[-1], prediction_dates[0]], 
                        [historical_data['close'].iloc[-1], predictions[0]], 
                        color=self.colors['prediction'], linewidth=2.5, 
                        linestyle='--', alpha=0.8, label='预测连接线')
            
            # 添加预测点的标注
            for i, (date, pred) in enumerate(zip(prediction_dates, predictions)):
                ax1.annotate(f'{pred:.2f}', 
                           xy=(date, pred), 
                           xytext=(10, 10), 
                           textcoords='offset points',
                           fontsize=9, 
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor=self.colors['prediction'], 
                                   alpha=0.7, edgecolor='white'),
                           color='white', fontweight='bold')
        else:
            # 处理没有日期列的情况
            ax1.plot(hist_dates, historical_data['close'], 
                    color=self.colors['ma20'], linewidth=2.5, alpha=0.8,
                    label='历史收盘价')
            ax1.plot(prediction_dates, predictions, 
                    color=self.colors['prediction'], linewidth=3, 
                    label='预测收盘价', marker='o', markersize=6)
        
        ax1.set_title('股价走势预测分析', fontsize=14, fontweight='bold', 
                     color=self.colors['text'], pad=20)
        ax1.set_ylabel('价格 (元)', fontsize=12, color=self.colors['text'])
        ax1.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, 
                  framealpha=0.9, fontsize=11)
        
        # 美化主图
        ax1.grid(True, alpha=0.3, color=self.colors['grid'], linewidth=0.5)
        
        # 格式化x轴日期显示
        if 'date' in historical_data.columns:
            ax1.tick_params(axis='x', rotation=45, labelsize=10, color=self.colors['text'])
            import matplotlib.dates as mdates
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(historical_data)//10)))
        
        # 2. 预测详情柱状图
        ax2 = fig.add_subplot(gs[1, :])
        
        # 创建渐变色柱状图
        bars = ax2.bar(range(len(predictions)), predictions, 
                      color=self.colors['prediction'], alpha=0.8,
                      edgecolor='white', linewidth=1.5, width=0.7)
        
        # 为每个柱子添加渐变效果
        for i, bar in enumerate(bars):
            # 根据预测值的高低调整颜色深度
            intensity = (predictions[i] - min(predictions)) / (max(predictions) - min(predictions)) if max(predictions) != min(predictions) else 0.5
            bar.set_facecolor(plt.cm.Reds(0.4 + intensity * 0.4))
        
        ax2.set_title('未来7个交易日预测详情', fontsize=14, fontweight='bold', 
                     color=self.colors['text'])
        ax2.set_xlabel('预测日期', fontsize=12, color=self.colors['text'])
        ax2.set_ylabel('预测价格 (元)', fontsize=12, color=self.colors['text'])
        
        # 设置x轴标签为具体日期
        if prediction_dates is not None and hasattr(prediction_dates[0], 'strftime'):
            date_labels = [date.strftime('%m-%d') for date in prediction_dates]
            ax2.set_xticks(range(len(predictions)))
            ax2.set_xticklabels(date_labels, rotation=45)
        else:
            ax2.set_xticks(range(len(predictions)))
            ax2.set_xticklabels([f'第{i+1}天' for i in range(len(predictions))])
        
        # 添加数值标签 - 更美观的样式
        for i, v in enumerate(predictions):
            ax2.text(i, v + max(predictions) * 0.01, f'¥{v:.2f}', 
                    ha='center', va='bottom', fontweight='bold', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                             alpha=0.8, edgecolor=self.colors['border']))
        
        ax2.grid(True, alpha=0.3, color=self.colors['grid'], linewidth=0.5)
        
        # 3. 预测趋势分析图
        ax3 = fig.add_subplot(gs[2, 0])
        
        # 计算涨跌幅
        current_price = historical_data['close'].iloc[-1]
        changes = [(pred - current_price) / current_price * 100 for pred in predictions]
        
        # 绘制涨跌幅趋势
        colors = [self.colors['up'] if change > 0 else self.colors['down'] for change in changes]
        bars = ax3.bar(range(len(changes)), changes, color=colors, alpha=0.8, width=0.7)
        
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
        ax3.set_title('预测涨跌幅趋势', fontsize=12, fontweight='bold', color=self.colors['text'])
        ax3.set_ylabel('涨跌幅 (%)', fontsize=11, color=self.colors['text'])
        ax3.set_xlabel('预测日期', fontsize=11, color=self.colors['text'])
        
        # 添加数值标签
        for i, v in enumerate(changes):
            ax3.text(i, v + (max(changes) - min(changes)) * 0.05 if v > 0 else v - (max(changes) - min(changes)) * 0.05, 
                    f'{v:+.1f}%', ha='center', va='bottom' if v > 0 else 'top', 
                    fontsize=9, fontweight='bold')
        
        if prediction_dates is not None and hasattr(prediction_dates[0], 'strftime'):
            date_labels = [date.strftime('%m-%d') for date in prediction_dates]
            ax3.set_xticks(range(len(predictions)))
            ax3.set_xticklabels(date_labels, rotation=45, fontsize=9)
        
        ax3.grid(True, alpha=0.3, color=self.colors['grid'], linewidth=0.5)
        
        # 4. 预测统计信息
        ax4 = fig.add_subplot(gs[2, 1])
        ax4.axis('off')  # 隐藏坐标轴
        
        # 创建统计信息文本
        avg_pred = np.mean(predictions)
        max_pred = np.max(predictions)
        min_pred = np.min(predictions)
        avg_change = np.mean(changes)
        
        stats_text = f"""预测统计摘要
        
当前价格: ¥{current_price:.2f}
平均预测: ¥{avg_pred:.2f}
最高预测: ¥{max_pred:.2f}
最低预测: ¥{min_pred:.2f}

平均涨跌: {avg_change:+.2f}%
预测趋势: {'📈 看涨' if avg_change > 0 else '📉 看跌' if avg_change < 0 else '➡️ 震荡'}

预测区间: ¥{min_pred:.2f} - ¥{max_pred:.2f}
波动幅度: {((max_pred - min_pred) / current_price * 100):.2f}%"""
        
        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8f9fa', 
                         alpha=0.8, edgecolor=self.colors['border']))
        
        ax4.set_title('预测摘要', fontsize=12, fontweight='bold', 
                     color=self.colors['text'], pad=10)
        
        # 美化所有子图
        for ax in [ax1, ax2, ax3]:
            self._beautify_axis_simple(ax)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"预测结果图已保存至: {save_path}")
        else:
            plt.show()
        
        return fig
    
    def plot_model_performance(self, train_losses, val_losses, save_path=None):
        """绘制模型训练性能"""
        # 使用更美观的布局
        fig = plt.figure(figsize=(16, 6))
        fig.patch.set_facecolor('white')
        
        # 主标题
        fig.suptitle('R-CSAN模型训练性能分析', fontsize=16, fontweight='bold', 
                    color=self.colors['text'], y=0.95)
        
        # 损失曲线图
        ax1 = plt.subplot(1, 2, 1)
        epochs = range(1, len(train_losses) + 1)
        
        # 绘制平滑的损失曲线
        ax1.plot(epochs, train_losses, label='训练损失', 
                color=self.colors['up'], linewidth=3, alpha=0.8,
                marker='o', markersize=4, markevery=max(1, len(epochs)//20))
        ax1.plot(epochs, val_losses, label='验证损失', 
                color=self.colors['down'], linewidth=3, alpha=0.8,
                marker='s', markersize=4, markevery=max(1, len(epochs)//20))
        
        # 添加填充区域显示趋势
        ax1.fill_between(epochs, train_losses, alpha=0.1, color=self.colors['up'])
        ax1.fill_between(epochs, val_losses, alpha=0.1, color=self.colors['down'])
        
        ax1.set_title('训练与验证损失曲线', fontsize=14, fontweight='bold', 
                     color=self.colors['text'], pad=15)
        ax1.set_xlabel('训练轮次 (Epoch)', fontsize=12, color=self.colors['text'])
        ax1.set_ylabel('损失值 (Loss)', fontsize=12, color=self.colors['text'])
        
        # 美化图例
        legend = ax1.legend(loc='upper right', frameon=True, fancybox=True, 
                          shadow=True, framealpha=0.9, fontsize=11)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor(self.colors['border'])
        
        ax1.grid(True, alpha=0.3, color=self.colors['grid'], linewidth=0.5)
        
        # 添加最终损失值标注
        final_train_loss = train_losses[-1]
        final_val_loss = val_losses[-1]
        ax1.annotate(f'训练: {final_train_loss:.4f}', 
                    xy=(len(epochs), final_train_loss), 
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', 
                             facecolor=self.colors['up'], alpha=0.7),
                    color='white')
        ax1.annotate(f'验证: {final_val_loss:.4f}', 
                    xy=(len(epochs), final_val_loss), 
                    xytext=(10, -15), textcoords='offset points',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', 
                             facecolor=self.colors['down'], alpha=0.7),
                    color='white')
        
        # 损失分布直方图
        ax2 = plt.subplot(1, 2, 2)
        
        # 创建更美观的直方图
        n_bins = min(20, len(train_losses)//2)
        alpha = 0.7
        
        # 训练损失分布
        n1, bins1, patches1 = ax2.hist(train_losses, bins=n_bins, alpha=alpha, 
                                       label='训练损失分布', 
                                       color=self.colors['up'], 
                                       edgecolor='white', linewidth=1)
        
        # 验证损失分布  
        n2, bins2, patches2 = ax2.hist(val_losses, bins=n_bins, alpha=alpha, 
                                       label='验证损失分布', 
                                       color=self.colors['down'],
                                       edgecolor='white', linewidth=1)
        
        # 为直方图添加渐变效果
        for patch in patches1:
            patch.set_facecolor(self.colors['up'])
            patch.set_alpha(alpha)
        for patch in patches2:
            patch.set_facecolor(self.colors['down'])
            patch.set_alpha(alpha)
        
        ax2.set_title('损失值分布统计', fontsize=14, fontweight='bold', 
                     color=self.colors['text'], pad=15)
        ax2.set_xlabel('损失值', fontsize=12, color=self.colors['text'])
        ax2.set_ylabel('频次', fontsize=12, color=self.colors['text'])
        
        # 美化图例
        legend2 = ax2.legend(loc='upper right', frameon=True, fancybox=True, 
                           shadow=True, framealpha=0.9, fontsize=11)
        legend2.get_frame().set_facecolor('white')
        legend2.get_frame().set_edgecolor(self.colors['border'])
        
        ax2.grid(True, alpha=0.3, color=self.colors['grid'], linewidth=0.5)
        
        # 添加统计信息
        stats_text = f"""统计摘要:
训练损失均值: {np.mean(train_losses):.4f}
验证损失均值: {np.mean(val_losses):.4f}
收敛程度: {'良好' if abs(final_train_loss - final_val_loss) < 0.01 else '一般'}"""
        
        ax2.text(0.98, 0.98, stats_text, transform=ax2.transAxes, 
                fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', 
                         alpha=0.8, edgecolor=self.colors['border']))
        
        # 美化子图
        for ax in [ax1, ax2]:
            self._beautify_axis_simple(ax)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"训练性能图已保存到: {save_path}")
        
        plt.show()
    
    def create_prediction_report(self, historical_data, predictions, stock_code, 
                               model_info=None, save_path=None):
        """创建预测报告"""
        # 计算统计信息
        current_price = historical_data['close'].iloc[-1]
        predicted_prices = predictions
        
        # 涨跌情况
        price_changes = [(pred - current_price) / current_price * 100 for pred in predicted_prices]
        
        # 创建报告
        report = f"""
# {stock_code} 股票预测报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 当前股票信息
- 当前股价: ¥{current_price:.2f}
- 最高价: ¥{historical_data['high'].iloc[-1]:.2f}
- 最低价: ¥{historical_data['low'].iloc[-1]:.2f}
- 成交量: {historical_data['volume'].iloc[-1]:,.0f}

## 未来7天预测
"""
        
        for i, (pred, change) in enumerate(zip(predicted_prices, price_changes)):
            trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            report += f"- 第{i+1}天: ¥{pred:.2f} ({change:+.2f}%) {trend}\n"
        
        report += f"""
## 预测摘要
- 平均预测价格: ¥{np.mean(predicted_prices):.2f}
- 最高预测价格: ¥{np.max(predicted_prices):.2f}
- 最低预测价格: ¥{np.min(predicted_prices):.2f}
- 平均涨跌幅: {np.mean(price_changes):+.2f}%
- 预测趋势: {'看涨' if np.mean(price_changes) > 0 else '看跌' if np.mean(price_changes) < 0 else '震荡'}

## 风险提示
本预测结果仅供参考，股市有风险，投资需谨慎！
"""
        
        if model_info:
            report += f"\n## 模型信息\n{model_info}\n"
        
        print(report)
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"预测报告已保存到: {save_path}")
        
        return report

if __name__ == "__main__":
    # 测试可视化功能
    print("测试股票可视化功能...")
    
    # 创建测试数据
    dates = pd.date_range(start='2023-01-01', periods=100)
    test_data = pd.DataFrame({
        'date': dates,
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 102,
        'low': np.random.randn(100).cumsum() + 98,
        'close': np.random.randn(100).cumsum() + 101,
        'volume': np.random.randint(1000000, 10000000, 100),
        'ma5': np.random.randn(100).cumsum() + 100,
        'ma20': np.random.randn(100).cumsum() + 100,
        'rsi': np.random.uniform(20, 80, 100)
    })
    
    # 创建可视化器
    visualizer = StockVisualizer()
    
    # 测试概览图
    visualizer.plot_stock_overview(test_data, "测试股票", "d:/股票分析/test_overview.png")
    
    # 测试预测结果
    predictions = np.random.randn(7).cumsum() + 101
    visualizer.plot_prediction_results(test_data.tail(30), predictions, stock_code="测试股票")
    
    # 测试预测报告
    report = visualizer.create_prediction_report(test_data, predictions, "测试股票")
    
    print("可视化功能测试完成！")
