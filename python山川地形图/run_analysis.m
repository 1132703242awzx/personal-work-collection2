% 运行投资组合风险分析演示
clear; clc; close all;

fprintf('🚀 启动投资组合风险分析系统...\n\n');

% 设置随机种子
rng(42);

% 模拟数据
T = 500;
N = 4;
assetNames = {'沪深300', '中证500', '国债', '黄金'};
annualReturns = [0.08, 0.12, 0.035, 0.06];
annualVols = [0.28, 0.35, 0.08, 0.20];

% 相关性矩阵
corrMatrix = [1.00, 0.85, -0.15, 0.20;
              0.85, 1.00, -0.10, 0.15;
              -0.15, -0.10, 1.00, -0.05;
              0.20, 0.15, -0.05, 1.00];

% 生成数据
dailyMeans = annualReturns / 252;
dailyCov = (annualVols' * annualVols .* corrMatrix) / 252;
returns = mvnrnd(dailyMeans, dailyCov, T);

% 构建价格序列
initialPrices = [3000, 6000, 100, 300];
prices = zeros(T+1, N);
prices(1, :) = initialPrices;

for t = 2:T+1
    prices(t, :) = prices(t-1, :) .* (1 + returns(t-1, :));
end

fprintf('📊 数据生成完成，开始分析...\n');

% 策略1: 等权重
results1 = portfolio_analysis(prices, 'ConfidenceLevel', 0.95);

fprintf('✅ 等权重组合分析完成\n');
fprintf('   年化波动率: %.2f%%\n', results1.annualizedVol*100);
fprintf('   VaR (95%%): %.2f%%\n', results1.VaR.annual*100);
fprintf('   最大回撤: %.2f%%\n', abs(results1.riskMetrics.maxDrawdown)*100);

% 策略2: 保守型
conservativeWeights = [0.25, 0.15, 0.5, 0.1];
results2 = portfolio_analysis(prices, 'Weights', conservativeWeights, 'ConfidenceLevel', 0.99);

fprintf('✅ 保守型组合分析完成\n');
fprintf('   年化波动率: %.2f%%\n', results2.annualizedVol*100);
fprintf('   VaR (99%%): %.2f%%\n', results2.VaR.annual*100);
fprintf('   最大回撤: %.2f%%\n', abs(results2.riskMetrics.maxDrawdown)*100);

fprintf('\n🎯 分析完成！请查看生成的图表。\n');
