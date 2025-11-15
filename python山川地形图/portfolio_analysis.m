% PORTFOLIO_ANALYSIS - 投资组合风险分析脚本
%
% 功能描述:
%   这是一个综合性的投资组合风险分析工具，提供VaR、CVaR、投资组合优化、
%   风险分解等多种金融风险管理功能。
%
% 运行方式:
%   直接运行此脚本即可，不需要输入参数
%
% 输出:
%   results - 结构体，包含所有分析结果
%   生成多个可视化图表
%
% 作者: AI Assistant
% 版本: 2.0 (脚本版本)
% 日期: 2024

clear; clc; close all;

fprintf('🚀 启动投资组合风险分析系统...\n\n');

%% ═══════════════════════════════════════════════════════════════════════════
%% 📊 投资策略配置区域 - 请在此处自定义您的投资策略
%% ═══════════════════════════════════════════════════════════════════════════

% 分析参数设置
confidenceLevel = 0.95;      % VaR置信水平 (0.90, 0.95, 0.99)
windowLength = 252;          % 滚动窗口长度 (天数)
optimizePortfolio = true;    % 是否进行数学优化
riskFreeRate = 0.03;         % 无风险利率 (年化)
showVisualization = true;    % 是否显示图表

% 资产说明: [沪深300, 中证500, 10年期国债, 黄金ETF]
% 权重必须和为1.0，例如: [0.4, 0.3, 0.2, 0.1] 表示 40%, 30%, 20%, 10%

% 🎯 定义多种投资策略进行对比分析
strategies = struct();

% 策略1: 等权重组合 (25% × 4)
strategies.equal = struct();
strategies.equal.name = '等权重组合';
strategies.equal.weights = [0.25, 0.25, 0.25, 0.25];
strategies.equal.description = '四个资产平均配置，风险分散';

% 策略2: 保守型组合 (低风险偏好)
strategies.conservative = struct();
strategies.conservative.name = '保守型组合';
strategies.conservative.weights = [0.20, 0.10, 0.60, 0.10];
strategies.conservative.description = '大比例国债配置，追求稳健收益';

% 策略3: 成长型组合 (高风险高收益)
strategies.growth = struct();
strategies.growth.name = '成长型组合';
strategies.growth.weights = [0.50, 0.35, 0.10, 0.05];
strategies.growth.description = '股票为主，追求高收益潜力';

% 策略4: 平衡型组合 (股债平衡)
strategies.balanced = struct();
strategies.balanced.name = '平衡型组合';
strategies.balanced.weights = [0.35, 0.25, 0.30, 0.10];
strategies.balanced.description = '股债均衡，风险收益兼顾';

% 策略5: 自定义策略 - 请在此处设置您的个人投资策略
strategies.custom = struct();
strategies.custom.name = '自定义策略';
strategies.custom.weights = [0.40, 0.20, 0.25, 0.15];  % ← 在此修改您的权重配置
strategies.custom.description = '根据个人偏好定制的投资组合';

% 🔧 高级设置 (可选)
% 如果只想分析特定策略，请在下面列表中指定策略名称
% 例如: analyze_strategies = {'equal', 'custom'};  % 只分析等权重和自定义策略
analyze_strategies = {'equal', 'conservative', 'growth', 'balanced', 'custom'};  % 分析所有策略

fprintf('📋 已配置 %d 种投资策略待分析\n', length(analyze_strategies));
for i = 1:length(analyze_strategies)
    strategy_name = analyze_strategies{i};
    strategy = strategies.(strategy_name);
    fprintf('   %d. %s: [%.0f%%, %.0f%%, %.0f%%, %.0f%%] - %s\n', ...
            i, strategy.name, ...
            strategy.weights(1)*100, strategy.weights(2)*100, ...
            strategy.weights(3)*100, strategy.weights(4)*100, ...
            strategy.description);
end
fprintf('\n');

%% ═══════════════════════════════════════════════════════════════════════════
%% 📈 市场数据生成 (模拟真实市场环境)
%% ═══════════════════════════════════════════════════════════════════════════

% 数据生成参数
rng(42);  % 设置随机种子确保结果可重现
T = 500;  % 500个交易日
N = 4;    % 4个资产

fprintf('📊 正在生成模拟市场数据...\n');

% 资产特征设置 (基于历史统计)
assetNames = {'沪深300指数', '中证500指数', '10年期国债', '黄金ETF'};
annualReturns = [0.08, 0.12, 0.035, 0.06];     % 年化收益率
annualVols = [0.28, 0.35, 0.08, 0.20];         % 年化波动率

% 相关性矩阵 (基于市场观察)
corrMatrix = [1.00, 0.85, -0.15, 0.20;   % 沪深300
              0.85, 1.00, -0.10, 0.15;   % 中证500  
              -0.15, -0.10, 1.00, -0.05; % 国债
              0.20, 0.15, -0.05, 1.00];  % 黄金

% 生成收益率数据
dailyMeans = annualReturns / 252;
dailyCov = (annualVols' * annualVols .* corrMatrix) / 252;
returns = mvnrnd(dailyMeans, dailyCov, T);

% 构建价格时间序列
initialPrices = [3000, 6000, 100, 300]; % 各资产初始价格
priceData = zeros(T+1, N);
priceData(1, :) = initialPrices;

for t = 2:T+1
    priceData(t, :) = priceData(t-1, :) .* (1 + returns(t-1, :));
end

fprintf('✅ 市场数据生成完成\n');
for i = 1:N
    actualReturn = mean(returns(:,i)) * 252;
    actualVol = std(returns(:,i)) * sqrt(252);
    fprintf('   %-12s: 收益率 %5.1f%%, 波动率 %5.1f%%\n', ...
            assetNames{i}, actualReturn*100, actualVol*100);
end
fprintf('\n');

%% ═══════════════════════════════════════════════════════════════════════════
%% 🔍 多策略投资组合分析
%% ═══════════════════════════════════════════════════════════════════════════

[T_prices, N] = size(priceData);
T_returns = T_prices - 1;
returns = diff(log(priceData));  % 计算对数收益率

fprintf('🚀 开始多策略投资组合分析...\n');
fprintf('   • 数据期间: %d个交易日\n', T_returns);
fprintf('   • 分析资产: %d个\n', N);
fprintf('   • 分析策略: %d个\n\n', length(analyze_strategies));

% 存储所有策略的分析结果
all_results = struct();

% 循环分析每个策略
for s = 1:length(analyze_strategies)
    strategy_name = analyze_strategies{s};
    strategy = strategies.(strategy_name);
    weights = strategy.weights;
    
    fprintf('📈 分析策略 %d/%d: %s\n', s, length(analyze_strategies), strategy.name);
    fprintf('   权重配置: [%.0f%%, %.0f%%, %.0f%%, %.0f%%]\n', ...
            weights(1)*100, weights(2)*100, weights(3)*100, weights(4)*100);
    fprintf('   策略描述: %s\n', strategy.description);
    
    % 验证权重
    if abs(sum(weights) - 1) > 1e-6
        error('策略 %s 的权重之和必须等于1', strategy.name);
    end
    
    %% 计算该策略的投资组合收益率
    portfolioReturns = returns * weights';
    
    %% 风险指标计算
    fprintf('   🔍 计算风险指标...\n');
    
    % 1. 波动率
    dailyVol = std(portfolioReturns);
    annualizedVol = dailyVol * sqrt(252);
    
    % 2. VaR计算（历史模拟法）
    sortedReturns = sort(portfolioReturns);
    VaR_index = floor((1 - confidenceLevel) * length(sortedReturns));
    VaR_daily = -sortedReturns(max(1, VaR_index));
    VaR_annual = VaR_daily * sqrt(252);
    
    % 3. CVaR计算（条件风险价值）
    tailReturns = sortedReturns(1:VaR_index);
    CVaR_daily = -mean(tailReturns);
    CVaR_annual = CVaR_daily * sqrt(252);
    
    % 4. 其他风险指标
    annualizedReturn = mean(portfolioReturns) * 252;
    sharpeRatio = (annualizedReturn - riskFreeRate) / annualizedVol;
    
    % 最大回撤计算
    cumReturns = cumprod(1 + portfolioReturns);
    peak = cummax(cumReturns);
    drawdown = (cumReturns - peak) ./ peak;
    maxDrawdown = min(drawdown);
    
    % Calmar比率
    calmarRatio = annualizedReturn / abs(maxDrawdown);
    
    % 偏度和峰度
    skewness_val = skewness(portfolioReturns);
    kurtosis_val = kurtosis(portfolioReturns);
    
    %% 投资组合优化 (仅对第一个策略进行，避免重复计算)
    optimalWeights = [];
    efficientFrontier = [];
    
    if optimizePortfolio && s == 1
        fprintf('   🎯 进行投资组合优化...\n');
        
        try
            % 计算均值和协方差矩阵
            mu = mean(returns)';
            Sigma = cov(returns);
            
            % 检查协方差矩阵
            if any(eig(Sigma) <= 0)
                warning('协方差矩阵不是正定的，进行修正');
                Sigma = Sigma + 1e-6 * eye(size(Sigma));
            end
            
            % 约束条件：权重和为1，权重非负
            Aeq = ones(1, N);
            beq = 1;
            lb = zeros(N, 1);
            ub = ones(N, 1);
            
            % 最小方差组合
            f = zeros(N, 1);
            try
                [optimalWeights, ~] = quadprog(2*Sigma, f, [], [], Aeq, beq, lb, ub);
                optimalWeights = optimalWeights';
                
                % 有效前沿计算 (简化版本)
                nPoints = 20;
                targetReturns = linspace(min(mu), max(mu), nPoints);
                efficientFrontier = zeros(nPoints, 2);
                
                for i = 1:nPoints
                    Aeq_temp = [Aeq; mu'];
                    beq_temp = [beq; targetReturns(i)];
                    
                    try
                        [w_temp, ~] = quadprog(2*Sigma, f, [], [], Aeq_temp, beq_temp, lb, ub);
                        if ~isempty(w_temp)
                            efficientFrontier(i, 1) = sqrt(w_temp' * Sigma * w_temp) * sqrt(252);
                            efficientFrontier(i, 2) = targetReturns(i) * 252;
                        end
                    catch
                        efficientFrontier(i, :) = NaN;
                    end
                end
                
                % 移除无效点
                validIdx = ~any(isnan(efficientFrontier), 2);
                efficientFrontier = efficientFrontier(validIdx, :);
                
            catch
                warning('投资组合优化失败');
            end
            
        catch ME
            warning('优化过程出错: %s', ME.message);
        end
    end
    
    %% 保存该策略的结果
    result = struct();
    result.strategyName = strategy.name;
    result.weights = weights;
    result.description = strategy.description;
    result.annualizedVol = annualizedVol;
    result.annualizedReturn = annualizedReturn;
    result.sharpeRatio = sharpeRatio;
    result.maxDrawdown = maxDrawdown;
    result.calmarRatio = calmarRatio;
    result.VaR_annual = VaR_annual;
    result.CVaR_annual = CVaR_annual;
    result.skewness = skewness_val;
    result.kurtosis = kurtosis_val;
    result.portfolioReturns = portfolioReturns;
    result.cumReturns = cumReturns;
    result.drawdown = drawdown;
    
    if s == 1  % 只在第一个策略保存优化结果
        result.optimalWeights = optimalWeights;
        result.efficientFrontier = efficientFrontier;
    end
    
    % 存储结果
    all_results.(strategy_name) = result;
    
    % 显示该策略的关键指标
    fprintf('   ✅ %s 分析完成\n', strategy.name);
    fprintf('      年化收益率: %6.2f%%  | 年化波动率: %6.2f%%\n', ...
            annualizedReturn*100, annualizedVol*100);
    fprintf('      夏普比率:   %6.3f   | 最大回撤:   %6.2f%%\n', ...
            sharpeRatio, abs(maxDrawdown)*100);
    fprintf('      VaR(%.0f%%):   %6.2f%%  | CVaR:       %6.2f%%\n\n', ...
            confidenceLevel*100, VaR_annual*100, CVaR_annual*100);
end

%% ═══════════════════════════════════════════════════════════════════════════
%% 📊 策略对比分析和可视化
%% ═══════════════════════════════════════════════════════════════════════════

fprintf('📊 生成策略对比分析...\n');

% 生成策略对比表格
fprintf('\n📋 ═══════════════ 投资策略对比分析表 ═══════════════\n');
fprintf('%-12s %8s %8s %8s %8s %8s %8s\n', ...
        '策略名称', '年化收益', '年化波动', '夏普比率', '最大回撤', 'VaR', 'CVaR');
fprintf('%-12s %8s %8s %8s %8s %8s %8s\n', ...
        '--------', '--------', '--------', '--------', '--------', '-----', '-----');

strategy_names = fieldnames(all_results);
for i = 1:length(strategy_names)
    strategy_name = strategy_names{i};
    result = all_results.(strategy_name);
    
    fprintf('%-12s %7.2f%% %7.2f%% %8.3f %7.2f%% %6.2f%% %6.2f%%\n', ...
            result.strategyName, ...
            result.annualizedReturn*100, ...
            result.annualizedVol*100, ...
            result.sharpeRatio, ...
            abs(result.maxDrawdown)*100, ...
            result.VaR_annual*100, ...
            result.CVaR_annual*100);
end

% 找出最佳策略
fprintf('\n🏆 最佳策略推荐:\n');
sharpe_ratios = zeros(length(strategy_names), 1);
for i = 1:length(strategy_names)
    sharpe_ratios(i) = all_results.(strategy_names{i}).sharpeRatio;
end
[~, best_idx] = max(sharpe_ratios);
best_strategy = all_results.(strategy_names{best_idx});
fprintf('   🥇 基于夏普比率: %s (夏普比率: %.3f)\n', ...
        best_strategy.strategyName, best_strategy.sharpeRatio);

% 风险最低策略
vols = zeros(length(strategy_names), 1);
for i = 1:length(strategy_names)
    vols(i) = all_results.(strategy_names{i}).annualizedVol;
end
[~, low_risk_idx] = min(vols);
low_risk_strategy = all_results.(strategy_names{low_risk_idx});
fprintf('   🛡️  风险最低: %s (波动率: %.2f%%)\n', ...
        low_risk_strategy.strategyName, low_risk_strategy.annualizedVol*100);

%% 生成可视化图表
if showVisualization
    fprintf('\n📈 生成可视化图表...\n');
    
    % 创建大型图表窗口
    figure('Position', [100, 100, 1400, 900], 'Name', '投资策略对比分析');
    
    % 子图1: 权重配置对比
    subplot(2, 4, 1);
    weight_matrix = zeros(length(strategy_names), N);
    for i = 1:length(strategy_names)
        weight_matrix(i, :) = all_results.(strategy_names{i}).weights;
    end
    bar(weight_matrix*100, 'grouped');
    title('📊 各策略权重配置', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('策略');
    ylabel('权重 (%)');
    legend(assetNames, 'Location', 'best', 'FontSize', 8);
    set(gca, 'XTickLabel', {all_results.(strategy_names{1}).strategyName, ...
                            all_results.(strategy_names{2}).strategyName, ...
                            all_results.(strategy_names{3}).strategyName, ...
                            all_results.(strategy_names{4}).strategyName, ...
                            all_results.(strategy_names{5}).strategyName}, ...
                            'XTickLabelRotation', 45);
    grid on;
    
    % 子图2: 风险收益散点图
    subplot(2, 4, 2);
    returns_vec = zeros(length(strategy_names), 1);
    risks_vec = zeros(length(strategy_names), 1);
    colors = ['r', 'b', 'g', 'm', 'c'];
    
    for i = 1:length(strategy_names)
        result = all_results.(strategy_names{i});
        returns_vec(i) = result.annualizedReturn*100;
        risks_vec(i) = result.annualizedVol*100;
        scatter(risks_vec(i), returns_vec(i), 100, colors(i), 'filled', 'o');
        hold on;
        text(risks_vec(i)+0.5, returns_vec(i), result.strategyName, 'FontSize', 8);
    end
    
    % 添加有效前沿（如果有）
    first_strategy = strategy_names{1};
    if isfield(all_results.(first_strategy), 'efficientFrontier') && ...
       ~isempty(all_results.(first_strategy).efficientFrontier)
        ef = all_results.(first_strategy).efficientFrontier;
        plot(ef(:,1)*100, ef(:,2)*100, 'k--', 'LineWidth', 2, 'DisplayName', '有效前沿');
    end
    
    title('🎯 风险-收益分布图', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('年化波动率 (%)');
    ylabel('年化收益率 (%)');
    grid on;
    hold off;
    
    % 子图3: 夏普比率对比
    subplot(2, 4, 3);
    sharpe_data = zeros(length(strategy_names), 1);
    strategy_labels = cell(length(strategy_names), 1);
    for i = 1:length(strategy_names)
        sharpe_data(i) = all_results.(strategy_names{i}).sharpeRatio;
        strategy_labels{i} = all_results.(strategy_names{i}).strategyName;
    end
    bar(sharpe_data, 'FaceColor', [0.2, 0.6, 0.8]);
    title('📈 夏普比率对比', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('策略');
    ylabel('夏普比率');
    set(gca, 'XTickLabel', strategy_labels, 'XTickLabelRotation', 45);
    grid on;
    
    % 在最高的柱子上标记数值
    [max_val, max_idx] = max(sharpe_data);
    text(max_idx, max_val + 0.01, sprintf('%.3f', max_val), ...
         'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    
    % 子图4: 最大回撤对比
    subplot(2, 4, 4);
    drawdown_data = zeros(length(strategy_names), 1);
    for i = 1:length(strategy_names)
        drawdown_data(i) = abs(all_results.(strategy_names{i}).maxDrawdown)*100;
    end
    bar(drawdown_data, 'FaceColor', [0.8, 0.3, 0.3]);
    title('📉 最大回撤对比', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('策略');
    ylabel('最大回撤 (%)');
    set(gca, 'XTickLabel', strategy_labels, 'XTickLabelRotation', 45);
    grid on;
    
    % 子图5: 累积收益率曲线对比
    subplot(2, 4, [5, 6]);
    colors_full = {[1,0,0], [0,0,1], [0,0.7,0], [1,0,1], [0,0.7,0.7]};
    for i = 1:length(strategy_names)
        result = all_results.(strategy_names{i});
        plot((result.cumReturns - 1)*100, 'Color', colors_full{i}, ...
             'LineWidth', 2, 'DisplayName', result.strategyName);
        hold on;
    end
    title('📈 累积收益率曲线对比', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('交易日');
    ylabel('累积收益率 (%)');
    legend('show', 'Location', 'best');
    grid on;
    hold off;
    
    % 子图6: VaR和CVaR对比
    subplot(2, 4, 7);
    var_data = zeros(length(strategy_names), 1);
    cvar_data = zeros(length(strategy_names), 1);
    for i = 1:length(strategy_names)
        var_data(i) = all_results.(strategy_names{i}).VaR_annual*100;
        cvar_data(i) = all_results.(strategy_names{i}).CVaR_annual*100;
    end
    
    x = 1:length(strategy_names);
    width = 0.35;
    bar(x - width/2, var_data, width, 'FaceColor', [0.8, 0.6, 0.2], 'DisplayName', 'VaR');
    hold on;
    bar(x + width/2, cvar_data, width, 'FaceColor', [0.6, 0.2, 0.8], 'DisplayName', 'CVaR');
    
    title('⚠️ VaR vs CVaR 对比', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('策略');
    ylabel('风险指标 (%)');
    set(gca, 'XTickLabel', strategy_labels, 'XTickLabelRotation', 45);
    legend('show');
    grid on;
    hold off;
    
    % 子图7: 风险指标雷达图
    subplot(2, 4, 8);
    % 选择第一个策略做雷达图示例
    first_result = all_results.(strategy_names{1});
    
    % 归一化风险指标用于雷达图
    metrics = [abs(first_result.maxDrawdown), first_result.annualizedVol/0.5, ...
               abs(first_result.skewness)/3, (first_result.kurtosis-3)/3];
    metrics = max(0, min(1, metrics));  % 限制在[0,1]范围
    
    angles = linspace(0, 2*pi, length(metrics)+1);
    metrics = [metrics, metrics(1)];  % 闭合图形
    
    polarplot(angles, metrics, 'ro-', 'LineWidth', 2, 'MarkerSize', 6);
    thetaticks(angles(1:end-1) * 180/pi);
    thetaticklabels({'最大回撤', '波动率', '偏度', '超额峰度'});
    title(sprintf('🕷️ %s 风险画像', first_result.strategyName), 'FontSize', 12);
    
    % 添加总标题
    sgtitle('🎯 多策略投资组合对比分析报告', 'FontSize', 16, 'FontWeight', 'bold');
end

%% ═══════════════════════════════════════════════════════════════════════════
%% 💾 保存结果和总结
%% ═══════════════════════════════════════════════════════════════════════════

% 保存所有结果
results = struct();
results.strategies = all_results;
results.analysisInfo = struct();
results.analysisInfo.timestamp = datestr(now);
results.analysisInfo.dataPoints = T_returns;
results.analysisInfo.assets = N;
results.analysisInfo.assetNames = {assetNames};
results.analysisInfo.windowLength = windowLength;
results.analysisInfo.confidenceLevel = confidenceLevel;
results.analysisInfo.analyzedStrategies = analyze_strategies;

% 保存到文件
try
    save('multi_strategy_analysis.mat', 'results', 'all_results');
    fprintf('💾 分析结果已保存到 multi_strategy_analysis.mat\n');
catch
    warning('无法保存结果文件');
end

% 最终总结
fprintf('\n🎉 ═══════════════ 分析完成总结 ═══════════════\n');
fprintf('✅ 已完成 %d 种投资策略的对比分析\n', length(analyze_strategies));
fprintf('📊 生成了 8 个可视化图表\n');
fprintf('📈 最佳策略 (基于夏普比率): %s\n', best_strategy.strategyName);
fprintf('🛡️  最低风险策略: %s\n', low_risk_strategy.strategyName);

fprintf('\n💡 个性化建议:\n');
fprintf('   • 风险厌恶者: 建议选择 "%s" (波动率 %.1f%%)\n', ...
        low_risk_strategy.strategyName, low_risk_strategy.annualizedVol*100);
fprintf('   • 风险中性者: 建议选择 "%s" (夏普比率 %.3f)\n', ...
        best_strategy.strategyName, best_strategy.sharpeRatio);
fprintf('   • 自定义需求: 修改脚本开头的权重配置\n');

if optimizePortfolio && isfield(all_results.(strategy_names{1}), 'optimalWeights') && ...
   ~isempty(all_results.(strategy_names{1}).optimalWeights)
    opt_weights = all_results.(strategy_names{1}).optimalWeights;
    fprintf('   • 数学最优配置: [%.1f%%, %.1f%%, %.1f%%, %.1f%%]\n', ...
            opt_weights(1)*100, opt_weights(2)*100, opt_weights(3)*100, opt_weights(4)*100);
end

fprintf('\n📋 使用说明:\n');
fprintf('   • results 变量包含所有分析结果\n');
fprintf('   • all_results 变量包含各策略详细数据\n');
fprintf('   • 修改脚本开头的策略配置可进行新的分析\n');
fprintf('   • 图表窗口可缩放和保存\n');

fprintf('\n⚠️  重要提醒:\n');
fprintf('   • 本分析基于历史模拟，不代表未来表现\n');
fprintf('   • 投资有风险，决策需谨慎\n');
fprintf('   • 建议结合实际市场情况调整策略\n');
fprintf('   • 定期重新评估和调整投资组合\n');

fprintf('\n🚀 分析完成！祝您投资顺利！\n');
