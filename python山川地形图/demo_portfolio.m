% 投资组合风险分析演示脚本
% 此脚本演示如何使用jinrong函数进行投资组合风险分析

clear; clc; close all;

fprintf('🚀 投资组合风险分析演示开始...\n\n');

% 模拟真实的金融数据
% 假设我们有4个资产：沪深300、中证500、国债、黄金
T = 500;  % 500个交易日数据
N = 4;    % 4个资产

% 设置随机种子
rng(42);

% 资产特征设置
assetNames = {'沪深300', '中证500', '10年期国债', '黄金ETF'};

% 年化统计特征
annualReturns = [0.08, 0.12, 0.035, 0.06];     % 期望年化收益率
annualVols = [0.28, 0.35, 0.08, 0.20];         % 年化波动率

% 相关性矩阵（基于真实市场观察）
corrMatrix = [1.00, 0.85, -0.15, 0.20;   % 沪深300
              0.85, 1.00, -0.10, 0.15;   % 中证500  
              -0.15, -0.10, 1.00, -0.05; % 国债
              0.20, 0.15, -0.05, 1.00];  % 黄金

% 转换为日收益率参数
dailyMeans = annualReturns / 252;
dailyCov = (annualVols' * annualVols .* corrMatrix) / 252;

% 生成多元正态分布的日收益率
returns = mvnrnd(dailyMeans, dailyCov, T);

% 构建价格序列（假设初始价格为1000点/元）
initialPrices = [3000, 6000, 100, 300]; % 沪深300, 中证500, 国债净值, 黄金价格
prices = zeros(T+1, N);
prices(1, :) = initialPrices;

for t = 2:T+1
    prices(t, :) = prices(t-1, :) .* (1 + returns(t-1, :));
end

fprintf('📊 生成的模拟数据统计:\n');
for i = 1:N
    actualReturn = mean(returns(:,i)) * 252;
    actualVol = std(returns(:,i)) * sqrt(252);
    fprintf('   %s: 收益率 %.1f%%, 波动率 %.1f%%\n', ...
            assetNames{i}, actualReturn*100, actualVol*100);
end
fprintf('\n');

% 调用投资组合分析函数
try
    % 检查是否存在jinrong函数
    if exist('jinrong', 'file') == 2
        fprintf('📈 开始投资组合风险分析...\n');
        results = jinrong(prices, 'ConfidenceLevel', 0.95, 'WindowLength', 250, 'OptimizePortfolio', true);
        
        fprintf('\n🎯 分析结果摘要:\n');
        fprintf('✓ 分析完成时间: %s\n', results.analysisInfo.timestamp);
        fprintf('✓ 数据点数量: %d个交易日\n', results.analysisInfo.dataPoints);
        fprintf('✓ 资产数量: %d个\n', results.analysisInfo.assets);
        fprintf('✓ 分析窗口: %d个交易日\n', results.analysisInfo.windowLength);
        
    else
        fprintf('❌ 错误: 找不到jinrong函数文件\n');
        fprintf('💡 请确保jinrong.m文件在当前路径中\n');
        
        % 显示当前路径和文件
        fprintf('\n📁 当前工作目录: %s\n', pwd);
        fprintf('📋 当前目录中的.m文件:\n');
        mFiles = dir('*.m');
        for i = 1:length(mFiles)
            fprintf('   • %s\n', mFiles(i).name);
        end
    end
    
catch ME
    fprintf('❌ 运行过程中出现错误:\n');
    fprintf('   错误类型: %s\n', ME.identifier);
    fprintf('   错误信息: %s\n', ME.message);
    
    if ~isempty(ME.stack)
        fprintf('   错误位置: %s (第%d行)\n', ME.stack(1).name, ME.stack(1).line);
    end
end

fprintf('\n✅ 演示脚本执行完毕\n');
