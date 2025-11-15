import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math

class ChannelAttention(nn.Module):
    """通道注意力模块"""
    def __init__(self, in_channels, reduction=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        
        self.fc = nn.Sequential(
            nn.Conv2d(in_channels, in_channels // reduction, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(in_channels // reduction, in_channels, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x))
        max_out = self.fc(self.max_pool(x))
        out = avg_out + max_out
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    """空间注意力模块"""
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=kernel_size//2, bias=False)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv1(x)
        return self.sigmoid(x)

class ResidualBlock(nn.Module):
    """残差块"""
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm1d(out_channels)
            )
    
    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class RCSAN(nn.Module):
    """残差通道-空间注意力网络 (Residual Channel-Spatial Attention Network)"""
    
    def __init__(self, input_features=15, sequence_length=60, hidden_dim=128, num_layers=4, 
                 num_heads=8, dropout=0.1, prediction_days=7):
        super(RCSAN, self).__init__()
        
        self.input_features = input_features
        self.sequence_length = sequence_length
        self.hidden_dim = hidden_dim
        self.prediction_days = prediction_days
        
        # 输入层
        self.input_projection = nn.Linear(input_features, hidden_dim)
        
        # 残差卷积层
        self.conv_layers = nn.ModuleList([
            ResidualBlock(hidden_dim if i == 0 else hidden_dim, hidden_dim)
            for i in range(num_layers)
        ])
        
        # 注意力机制
        self.channel_attention = ChannelAttention(hidden_dim)
        self.spatial_attention = SpatialAttention()
        
        # Transformer编码器
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # LSTM层
        self.lstm = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=2,
            batch_first=True,
            dropout=dropout,
            bidirectional=True
        )
        
        # 注意力融合层
        self.attention_fusion = nn.MultiheadAttention(
            embed_dim=hidden_dim * 2,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )
        
        # 输出层
        self.output_layers = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, prediction_days)
        )
        
        # 位置编码
        self.pos_encoding = self._create_positional_encoding(sequence_length, hidden_dim)
        
    def _create_positional_encoding(self, seq_len, d_model):
        """创建位置编码"""
        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        return pe.unsqueeze(0)
    
    def forward(self, x):
        batch_size, seq_len, features = x.shape
        
        # 输入投影
        x = self.input_projection(x)  # [batch_size, seq_len, hidden_dim]
        
        # 添加位置编码
        if x.device != self.pos_encoding.device:
            self.pos_encoding = self.pos_encoding.to(x.device)
        x = x + self.pos_encoding[:, :seq_len, :]
        
        # 残差卷积处理 (需要转换维度)
        x_conv = x.transpose(1, 2)  # [batch_size, hidden_dim, seq_len]
        for conv_layer in self.conv_layers:
            x_conv = conv_layer(x_conv)
        
        # 通道注意力 (添加一个维度用于2D卷积)
        x_conv_2d = x_conv.unsqueeze(-1)  # [batch_size, hidden_dim, seq_len, 1]
        ca_weight = self.channel_attention(x_conv_2d)
        x_conv_2d = x_conv_2d * ca_weight
        
        # 空间注意力
        sa_weight = self.spatial_attention(x_conv_2d)
        x_conv_2d = x_conv_2d * sa_weight
        
        # 转回原维度
        x_conv = x_conv_2d.squeeze(-1).transpose(1, 2)  # [batch_size, seq_len, hidden_dim]
        
        # Transformer编码
        x_transformer = self.transformer_encoder(x_conv)
        
        # LSTM处理
        x_lstm, _ = self.lstm(x_transformer)
        
        # 注意力融合
        x_fused, _ = self.attention_fusion(x_lstm, x_lstm, x_lstm)
        
        # 取最后一个时间步的输出
        x_final = x_fused[:, -1, :]  # [batch_size, hidden_dim * 2]
        
        # 预测输出
        predictions = self.output_layers(x_final)  # [batch_size, prediction_days]
        
        return predictions

class StockPredictor:
    """股票预测器"""
    
    def __init__(self, input_features=15, sequence_length=60, prediction_days=7, device=None):
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.sequence_length = sequence_length
        self.prediction_days = prediction_days
        
        # 初始化模型
        self.model = RCSAN(
            input_features=input_features,
            sequence_length=sequence_length,
            prediction_days=prediction_days
        ).to(self.device)
        
        # 损失函数和优化器
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3, weight_decay=1e-5)
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=10
        )
        
        print(f"模型已初始化，使用设备: {self.device}")
        print(f"模型参数数量: {sum(p.numel() for p in self.model.parameters()):,}")
    
    def prepare_data(self, data, target_column='close'):
        """准备训练数据"""
        # 选择特征列
        feature_columns = [
            'open', 'high', 'low', 'close', 'volume', 'amount',
            'ma5', 'ma10', 'ma20', 'ma60', 'rsi', 'macd', 'macd_signal', 'macd_hist'
        ]
        
        # 检查列是否存在
        available_columns = [col for col in feature_columns if col in data.columns]
        if len(available_columns) < len(feature_columns):
            print(f"警告: 缺少某些特征列，将使用可用的 {len(available_columns)} 个特征")
        
        # 数据归一化
        from sklearn.preprocessing import MinMaxScaler
        self.scaler = MinMaxScaler()
        
        # 准备特征数据
        features = data[available_columns].fillna(method='bfill').fillna(method='ffill')
        scaled_features = self.scaler.fit_transform(features)
        
        # 准备目标数据
        target = data[target_column].values
        
        # 创建序列数据
        X, y = [], []
        for i in range(len(scaled_features) - self.sequence_length - self.prediction_days + 1):
            X.append(scaled_features[i:i + self.sequence_length])
            y.append(target[i + self.sequence_length:i + self.sequence_length + self.prediction_days])
        
        X = np.array(X)
        y = np.array(y)
        
        # 目标值归一化
        self.target_scaler = MinMaxScaler()
        y_reshaped = y.reshape(-1, 1)
        y_scaled = self.target_scaler.fit_transform(y_reshaped)
        y = y_scaled.reshape(y.shape)
        
        return torch.FloatTensor(X), torch.FloatTensor(y)
    
    def train(self, train_data, epochs=100, batch_size=32, validation_split=0.2):
        """训练模型"""
        X, y = train_data
        
        # 分割训练和验证数据
        split_idx = int(len(X) * (1 - validation_split))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # 创建数据加载器
        from torch.utils.data import DataLoader, TensorDataset
        train_dataset = TensorDataset(X_train, y_train)
        val_dataset = TensorDataset(X_val, y_val)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        print(f"开始训练模型...")
        print(f"训练集大小: {len(X_train)}, 验证集大小: {len(X_val)}")
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            # 训练阶段
            self.model.train()
            train_loss = 0.0
            
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                self.optimizer.zero_grad()
                predictions = self.model(batch_X)
                loss = self.criterion(predictions, batch_y)
                loss.backward()
                
                # 梯度裁剪
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                
                self.optimizer.step()
                train_loss += loss.item()
            
            # 验证阶段
            self.model.eval()
            val_loss = 0.0
            
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                    predictions = self.model(batch_X)
                    loss = self.criterion(predictions, batch_y)
                    val_loss += loss.item()
            
            train_loss /= len(train_loader)
            val_loss /= len(val_loader)
            
            # 学习率调度
            self.scheduler.step(val_loss)
            
            # 早停机制
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # 保存最佳模型
                torch.save(self.model.state_dict(), 'd:/股票分析/best_model.pth')
            else:
                patience_counter += 1
            
            if epoch % 10 == 0 or patience_counter >= 20:
                print(f'Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}')
            
            if patience_counter >= 20:
                print("早停触发，训练结束")
                break
        
        # 加载最佳模型
        self.model.load_state_dict(torch.load('d:/股票分析/best_model.pth'))
        print("训练完成！")
    
    def predict(self, input_data):
        """预测未来股价"""
        self.model.eval()
        
        with torch.no_grad():
            if isinstance(input_data, np.ndarray):
                input_data = torch.FloatTensor(input_data)
            
            input_data = input_data.to(self.device)
            if len(input_data.shape) == 2:
                input_data = input_data.unsqueeze(0)
            
            predictions = self.model(input_data)
            
            # 反归一化
            predictions_np = predictions.cpu().numpy()
            predictions_original = self.target_scaler.inverse_transform(
                predictions_np.reshape(-1, 1)
            ).reshape(predictions_np.shape)
            
            return predictions_original
    
    def save_model(self, filepath):
        """保存模型"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scaler': self.scaler,
            'target_scaler': self.target_scaler,
            'sequence_length': self.sequence_length,
            'prediction_days': self.prediction_days
        }, filepath)
        print(f"模型已保存到: {filepath}")
    
    def load_model(self, filepath):
        """加载模型"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scaler = checkpoint['scaler']
        self.target_scaler = checkpoint['target_scaler']
        self.sequence_length = checkpoint['sequence_length']
        self.prediction_days = checkpoint['prediction_days']
        print(f"模型已从 {filepath} 加载")

if __name__ == "__main__":
    # 测试模型
    print("测试R-CSAN模型...")
    
    # 创建预测器
    predictor = StockPredictor(input_features=14, sequence_length=60, prediction_days=7)
    
    # 创建测试数据
    batch_size = 16
    sequence_length = 60
    input_features = 14
    
    test_input = torch.randn(batch_size, sequence_length, input_features)
    
    # 测试前向传播
    predictor.model.eval()
    with torch.no_grad():
        output = predictor.model(test_input)
        print(f"输入形状: {test_input.shape}")
        print(f"输出形状: {output.shape}")
        print("模型测试成功！")
