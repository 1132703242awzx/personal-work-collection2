function results = portfolio_analysis(priceData, varargin)
% PORTFOLIO_ANALYSIS - 投资组合风险分析函数
%
% 功能描述:
%   这是一个综合性的投资组合风险分析工具，提供VaR、CVaR、投资组合优化、
%   风险分解等多种金融风险管理功能。
%
% 语法:
%   results = portfolio_analysis(priceData)
%   results = portfolio_analysis(priceData, 'ParameterName', ParameterValue, ...)
%
% 输入参数:
%   priceData - (T+1) x N 矩阵，包含N个资产在T+1个时间点的价格数据
%               第一行为初始价格，后续行为历史价格
%
% 可选参数（名称-值对）:
%   'Weights'           - 1xN向量，投资组合权重（默认为等权重）
%   'ConfidenceLevel'   - 标量，VaR和CVaR的置信水平（默认0.95）
%   'WindowLength'      - 标量，滚动窗口长度（默认252，即一年）
%   'OptimizePortfolio' - 逻辑值，是否进行投资组合优化（默认true）
%   'RiskFreeRate'      - 标量，无风险利率年化值（默认0.03）
%   'Visualization'     - 逻辑值，是否生成可视化图表（默认true）
%
% 输出:
%   results - 结构体，包含所有分析结果
%
% 示例:
%   % 基本使用
%   data = randn(253, 4) + 1; % 模拟价格数据
%   results = jinrong(data);
%
%   % 自定义参数
%   weights = [0.4, 0.3, 0.2, 0.1];
%   results = jinrong(data, 'Weights', weights, 'ConfidenceLevel', 0.99);
%
% 作者: AI Assistant
% 版本: 1.0
% 日期: 2024

%% 输入参数解析和验证
p = inputParser;

% 必需参数
addRequired(p, 'priceData', @(x) isnumeric(x) && ismatrix(x) && size(x,1) >= 50);

% 可选参数
addParameter(p, 'Weights', [], @(x) isnumeric(x) && isvector(x) && all(x >= 0) && abs(sum(x) - 1) < 1e-6);
addParameter(p, 'ConfidenceLevel', 0.95, @(x) isnumeric(x) && isscalar(x) && x > 0 && x < 1);
addParameter(p, 'WindowLength', 252, @(x) isnumeric(x) && isscalar(x) && x > 0);
addParameter(p, 'OptimizePortfolio', true, @islogical);
addParameter(p, 'RiskFreeRate', 0.03, @(x) isnumeric(x) && isscalar(x));
addParameter(p, 'Visualization', true, @islogical);

parse(p, priceData, varargin{:});

% 提取参数
weights = p.Results.Weights;
confidenceLevel = p.Results.ConfidenceLevel;
windowLength = p.Results.WindowLength;
optimizePortfolio = p.Results.OptimizePortfolio;
riskFreeRate = p.Results.RiskFreeRate;
showVisualization = p.Results.Visualization;

%% 数据预处理
[T_prices, N] = size(priceData);
T_returns = T_prices - 1;

% 计算收益率
returns = diff(log(priceData));

% 设置默认权重
if isempty(weights)
    weights = ones(1, N) / N; % 等权重
end

% 验证权重维度
if length(weights) ~= N
    error('权重向量长度必须等于资产数量');
end

fprintf('📊 数据加载完成:\n');
fprintf('   • 资产数量: %d\n', N);
fprintf('   • 时间序列长度: %d个交易日\n', T_returns);
fprintf('   • 分析窗口: %d个交易日\n', min(windowLength, T_returns));

%% 计算投资组合收益率
portfolioReturns = returns * weights';

%% 风险指标计算
fprintf('🔍 正在计算风险指标...\n');

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

%% 投资组合优化
optimalWeights = [];
efficientFrontier = [];

if optimizePortfolio
    fprintf('🎯 正在进行投资组合优化...\n');
    
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
            
            % 有效前沿计算
            nPoints = 50;
            targetReturns = linspace(min(mu), max(mu), nPoints);
            efficientFrontier = zeros(nPoints, 2);
            
            for i = 1:nPoints
                % 添加收益率约束
                Aeq_temp = [Aeq; mu'];
                beq_temp = [beq; targetReturns(i)];
                
                try
                    [w_temp, fval] = quadprog(2*Sigma, f, [], [], Aeq_temp, beq_temp, lb, ub);
                    if ~isempty(w_temp)
                        efficientFrontier(i, 1) = sqrt(w_temp' * Sigma * w_temp) * sqrt(252); % 年化波动率
                        efficientFrontier(i, 2) = targetReturns(i) * 252; % 年化收益率
                    end
                catch
                    efficientFrontier(i, :) = NaN;
                end
            end
            
            % 移除无效点
            validIdx = ~any(isnan(efficientFrontier), 2);
            efficientFrontier = efficientFrontier(validIdx, :);
            
        catch
            warning('投资组合优化失败，使用等权重');
            optimalWeights = weights;
        end
        
    catch ME
        warning('优化过程出错: %s', ME.message);
    end
end

%% 可视化
if showVisualization
    fprintf('📈 生成可视化图表...\n');
    
    figure('Position', [100, 100, 1200, 800]);
    
    % 子图1: 投资组合收益率分布
    subplot(2, 3, 1);
    histogram(portfolioReturns * 100, 30, 'Normalization', 'probability', ...
             'FaceColor', [0.3, 0.6, 0.9], 'EdgeColor', 'white');
    hold on;
    xline(-VaR_daily * 100, 'r--', 'LineWidth', 2, 'Label', sprintf('VaR (%.1f%%)', confidenceLevel*100));
    xline(-CVaR_daily * 100, 'r-', 'LineWidth', 2, 'Label', 'CVaR');
    xlabel('日收益率 (%)');
    ylabel('概率密度');
    title('投资组合收益率分布');
    legend('Location', 'best');
    grid on;
    
    % 子图2: 累积收益率和回撤
    subplot(2, 3, 2);
    yyaxis left;
    plot(cumReturns - 1, 'b-', 'LineWidth', 1.5);
    ylabel('累积收益率', 'Color', 'b');
    yyaxis right;
    plot(drawdown * 100, 'r-', 'LineWidth', 1);
    ylabel('回撤 (%)', 'Color', 'r');
    xlabel('交易日');
    title('累积收益率与回撤');
    grid on;
    
    % 子图3: 滚动波动率
    subplot(2, 3, 3);
    if length(portfolioReturns) >= 30
        rollingVol = zeros(length(portfolioReturns) - 29, 1);
        for i = 30:length(portfolioReturns)
            rollingVol(i-29) = std(portfolioReturns(i-29:i)) * sqrt(252) * 100;
        end
        plot(30:length(portfolioReturns), rollingVol, 'g-', 'LineWidth', 1.5);
        xlabel('交易日');
        ylabel('30日滚动波动率 (%)');
        title('滚动波动率');
        grid on;
    else
        text(0.5, 0.5, '数据不足以计算滚动波动率', 'HorizontalAlignment', 'center');
    end
    
    % 子图4: 权重对比
    subplot(2, 3, 4);
    if ~isempty(optimalWeights)
        x = 1:N;
        width = 0.35;
        bar(x - width/2, weights * 100, width, 'FaceColor', [0.8, 0.8, 0.8], 'DisplayName', '当前权重');
        hold on;
        bar(x + width/2, optimalWeights * 100, width, 'FaceColor', [0.2, 0.6, 0.8], 'DisplayName', '最优权重');
        xlabel('资产编号');
        ylabel('权重 (%)');
        title('权重对比');
        legend('Location', 'best');
        grid on;
    else
        bar(weights * 100, 'FaceColor', [0.8, 0.8, 0.8]);
        xlabel('资产编号');
        ylabel('权重 (%)');
        title('当前投资组合权重');
        grid on;
    end
    
    % 子图5: 有效前沿
    subplot(2, 3, 5);
    if ~isempty(efficientFrontier) && size(efficientFrontier, 1) > 1
        plot(efficientFrontier(:, 1) * 100, efficientFrontier(:, 2) * 100, 'b-', 'LineWidth', 2);
        hold on;
        
        % 标记当前组合
        currentVol = annualizedVol * 100;
        currentRet = annualizedReturn * 100;
        plot(currentVol, currentRet, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r', 'DisplayName', '当前组合');
        
        % 标记最优组合
        if ~isempty(optimalWeights)
            optimalRet = (mean(returns) * optimalWeights') * 252 * 100;
            optimalVol = sqrt(optimalWeights * cov(returns) * optimalWeights') * sqrt(252) * 100;
            plot(optimalVol, optimalRet, 'go', 'MarkerSize', 8, 'MarkerFaceColor', 'g', 'DisplayName', '最优组合');
        end
        
        xlabel('年化波动率 (%)');
        ylabel('年化收益率 (%)');
        title('有效前沿');
        legend('Location', 'best');
        grid on;
    else
        text(0.5, 0.5, '无法生成有效前沿', 'HorizontalAlignment', 'center');
        title('有效前沿');
    end
    
    % 子图6: 风险指标雷达图
    subplot(2, 3, 6);
    % 风险指标归一化（用于雷达图显示）
    riskMetrics = [abs(maxDrawdown), dailyVol, abs(skewness_val)/3, (kurtosis_val-3)/3];
    riskMetrics = max(0, min(1, riskMetrics)); % 限制在[0,1]范围内
    
    angles = linspace(0, 2*pi, length(riskMetrics)+1);
    riskMetrics = [riskMetrics, riskMetrics(1)]; % 闭合图形
    
    polarplot(angles, riskMetrics, 'ro-', 'LineWidth', 2, 'MarkerSize', 6);
    thetaticks(angles(1:end-1) * 180/pi);
    thetaticklabels({'最大回撤', '波动率', '偏度', '超额峰度'});
    title('风险指标概览');
    
    % 调整子图间距
    sgtitle('投资组合风险分析报告', 'FontSize', 16, 'FontWeight', 'bold');
end

%% 组织输出结果
results = struct();

% 基本风险指标
results.annualizedVol = annualizedVol;
results.VaR = struct('daily', VaR_daily, 'annual', VaR_annual, 'confidenceLevel', confidenceLevel);
results.CVaR = struct('daily', CVaR_daily, 'annual', CVaR_annual, 'confidenceLevel', confidenceLevel);

% 投资组合数据
results.portfolioReturns = portfolioReturns;
results.weights = weights;
results.optimalWeights = optimalWeights;
results.efficientFrontier = efficientFrontier;

% 详细风险指标
results.riskMetrics = struct();
results.riskMetrics.annualizedReturn = annualizedReturn;
results.riskMetrics.sharpeRatio = sharpeRatio;
results.riskMetrics.maxDrawdown = maxDrawdown;
results.riskMetrics.calmarRatio = calmarRatio;
results.riskMetrics.skewness = skewness_val;
results.riskMetrics.kurtosis = kurtosis_val;

% 添加时间戳和参数信息
results.analysisInfo = struct();
results.analysisInfo.timestamp = datestr(now);
results.analysisInfo.dataPoints = T_returns;
results.analysisInfo.assets = N;
results.analysisInfo.windowLength = windowLength;
results.analysisInfo.confidenceLevel = confidenceLevel;

fprintf('✅ 投资组合风险分析完成！\n');
fprintf('🔍 主要发现:\n');
fprintf('   • 投资组合年化波动率: %.2f%%\n', annualizedVol * 100);
fprintf('   • %.1f%%置信水平下的年化VaR: %.2f%%\n', confidenceLevel * 100, VaR_annual * 100);
fprintf('   • 年化CVaR: %.2f%%\n', CVaR_annual * 100);
fprintf('   • 最大回撤: %.2f%%\n', maxDrawdown * 100);
if ~isempty(optimalWeights)
    fprintf('   • 投资组合优化已完成，建议权重已计算\n');
end

% 保存结果到文件（可选）
try
    save('portfolio_risk_analysis.mat', 'results');
    fprintf('💾 分析结果已保存到 portfolio_risk_analysis.mat\n');
catch
    warning('无法保存结果文件');
end

end
