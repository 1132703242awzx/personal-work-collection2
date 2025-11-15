function boerziman()
% 化学中玻尔兹曼分布分析工具
% 功能：分析分子在不同能级上的玻尔兹曼分布
% 作者：AI助手
% 日期：2024
% 
% 玻尔兹曼分布公式：N(E) = N₀ * exp(-E/kT)
% 其中：N(E) - 能量为E的状态的粒子数
%       N₀ - 基态粒子数  
%       E - 能量 (J)
%       k - 玻尔兹曼常数 (1.381×10⁻²³ J/K)
%       T - 绝对温度 (K)

clc;
clear;
close all;

fprintf('====================================\n');
fprintf('  化学玻尔兹曼分布分析工具 v1.0\n');
fprintf('====================================\n');
fprintf('功能：分析分子能级的玻尔兹曼分布\n');
fprintf('应用：化学反应、光谱学、热力学\n');
fprintf('====================================\n\n');

% 物理常数
k_B = 1.381e-23;  % 玻尔兹曼常数 (J/K)
h = 6.626e-34;    % 普朗克常数 (J·s)
c = 3e8;          % 光速 (m/s)
N_A = 6.022e23;   % 阿伏伽德罗常数 (mol⁻¹)

fprintf('物理常数：\n');
fprintf('玻尔兹曼常数 k = %.3e J/K\n', k_B);
fprintf('普朗克常数 h = %.3e J·s\n', h);
fprintf('光速 c = %.0e m/s\n', c);
fprintf('阿伏伽德罗常数 N_A = %.3e mol⁻¹\n\n', N_A);

% 分析类型选择
fprintf('请选择分析类型：\n');
fprintf('1. 基本玻尔兹曼分布\n');
fprintf('2. 温度效应分析\n');
fprintf('3. 能级分布分析\n');
fprintf('4. 化学反应平衡\n');
fprintf('5. 光谱线强度分析\n');
fprintf('6. 完整分析\n');
analysis_type = input('请输入选择 (1-6): ');

switch analysis_type
    case 1
        basic_boltzmann_analysis(k_B);
    case 2
        temperature_effect_analysis(k_B);
    case 3
        energy_level_analysis(k_B);
    case 4
        chemical_equilibrium_analysis(k_B);
    case 5
        spectral_intensity_analysis(k_B, h, c);
    case 6
        complete_analysis(k_B, h, c, N_A);
    otherwise
        error('无效的选择！');
end

fprintf('\n====================================\n');
fprintf('玻尔兹曼分布分析完成！\n');
fprintf('====================================\n');

end

% 1. 基本玻尔兹曼分布分析
function basic_boltzmann_analysis(k_B)
    fprintf('\n====================================\n');
    fprintf('    基本玻尔兹曼分布分析\n');
    fprintf('====================================\n');
    
    % 输入参数
    T = input('请输入温度 (K，默认300): ');
    if isempty(T)
        T = 300;
    end
    
    E_max = input('请输入最大能量 (×10⁻²⁰ J，默认10): ');
    if isempty(E_max)
        E_max = 10;
    end
    E_max = E_max * 1e-20; % 转换为焦耳
    
    N0 = input('请输入基态粒子数 (默认1000): ');
    if isempty(N0)
        N0 = 1000;
    end
    
    % 能量范围
    E = linspace(0, E_max, 1000);
    
    % 计算玻尔兹曼分布
    N = N0 * exp(-E ./ (k_B * T));
    
    % 创建图形
    figure('Name', '基本玻尔兹曼分布分析', 'NumberTitle', 'off');
    
    % 主分布图
    subplot(2,2,1);
    plot(E*1e20, N, 'b-', 'LineWidth', 2);
    xlabel('能量 (×10^{-20} J)');
    ylabel('粒子数 N(E)');
    title(sprintf('玻尔兹曼分布 (T = %.0f K)', T));
    grid on;
    
    % 半对数图
    subplot(2,2,2);
    semilogy(E*1e20, N, 'r-', 'LineWidth', 2);
    xlabel('能量 (×10^{-20} J)');
    ylabel('粒子数 N(E) (对数)');
    title('玻尔兹曼分布 (半对数)');
    grid on;
    
    % 归一化分布
    subplot(2,2,3);
    N_norm = N / N0;
    plot(E*1e20, N_norm, 'g-', 'LineWidth', 2);
    xlabel('能量 (×10^{-20} J)');
    ylabel('相对粒子数 N(E)/N₀');
    title('归一化玻尔兹曼分布');
    grid on;
    
    % 统计信息
    subplot(2,2,4);
    % 计算平均能量
    E_avg = trapz(E, E .* N) / trapz(E, N);
    % 计算最概然能量
    E_most_probable = 0; % 基态
    % 计算能量方差
    E_var = trapz(E, (E - E_avg).^2 .* N) / trapz(E, N);
    
    text(0.1, 0.9, '统计参数：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('温度：%.0f K', T), 'FontSize', 10);
    text(0.1, 0.7, sprintf('总粒子数：%.0f', trapz(E, N)), 'FontSize', 10);
    text(0.1, 0.6, sprintf('平均能量：%.2e J', E_avg), 'FontSize', 10);
    text(0.1, 0.5, sprintf('最概然能量：%.2e J', E_most_probable), 'FontSize', 10);
    text(0.1, 0.4, sprintf('能量方差：%.2e J²', E_var), 'FontSize', 10);
    text(0.1, 0.3, sprintf('kT = %.2e J', k_B * T), 'FontSize', 10);
    
    axis off;
    title('统计参数');
    
    % 输出结果
    fprintf('分析结果：\n');
    fprintf('温度：%.0f K\n', T);
    fprintf('平均能量：%.2e J\n', E_avg);
    fprintf('kT：%.2e J\n', k_B * T);
    fprintf('E_avg/kT：%.2f\n', E_avg / (k_B * T));
end

% 2. 温度效应分析
function temperature_effect_analysis(k_B)
    fprintf('\n====================================\n');
    fprintf('    温度效应分析\n');
    fprintf('====================================\n');
    
    % 输入参数
    T_range = input('请输入温度范围 [T_min, T_max] (K，默认[200, 800]): ');
    if isempty(T_range)
        T_range = [200, 800];
    end
    
    E_max = input('请输入最大能量 (×10⁻²⁰ J，默认15): ');
    if isempty(E_max)
        E_max = 15;
    end
    E_max = E_max * 1e-20;
    
    % 温度序列
    T_values = linspace(T_range(1), T_range(2), 5);
    colors = ['b', 'r', 'g', 'm', 'c'];
    
    % 能量范围
    E = linspace(0, E_max, 1000);
    
    % 创建图形
    figure('Name', '温度效应分析', 'NumberTitle', 'off');
    
    % 不同温度的分布
    subplot(2,2,1);
    hold on;
    legend_entries = {};
    for i = 1:length(T_values)
        T = T_values(i);
        N = exp(-E ./ (k_B * T));
        plot(E*1e20, N, 'Color', colors(i), 'LineWidth', 2);
        legend_entries{i} = sprintf('T = %.0f K', T);
    end
    xlabel('能量 (×10^{-20} J)');
    ylabel('相对粒子数 N(E)/N₀');
    title('不同温度下的玻尔兹曼分布');
    legend(legend_entries, 'Location', 'best');
    grid on;
    
    % 半对数图
    subplot(2,2,2);
    hold on;
    for i = 1:length(T_values)
        T = T_values(i);
        N = exp(-E ./ (k_B * T));
        semilogy(E*1e20, N, 'Color', colors(i), 'LineWidth', 2);
    end
    xlabel('能量 (×10^{-20} J)');
    ylabel('相对粒子数 N(E)/N₀ (对数)');
    title('玻尔兹曼分布 (半对数)');
    legend(legend_entries, 'Location', 'best');
    grid on;
    
    % 平均能量随温度变化
    subplot(2,2,3);
    T_fine = linspace(T_range(1), T_range(2), 100);
    E_avg_values = zeros(size(T_fine));
    
    for i = 1:length(T_fine)
        T = T_fine(i);
        N = exp(-E ./ (k_B * T));
        E_avg_values(i) = trapz(E, E .* N) / trapz(E, N);
    end
    
    plot(T_fine, E_avg_values*1e20, 'b-', 'LineWidth', 2);
    hold on;
    plot(T_fine, k_B * T_fine * 1e20, 'r--', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('平均能量 (×10^{-20} J)');
    title('平均能量随温度变化');
    legend('实际平均能量', 'kT', 'Location', 'northwest');
    grid on;
    
    % 高能态占比随温度变化
    subplot(2,2,4);
    E_threshold = E_max * 0.5; % 定义高能态阈值
    high_energy_fraction = zeros(size(T_fine));
    
    for i = 1:length(T_fine)
        T = T_fine(i);
        N = exp(-E ./ (k_B * T));
        total_particles = trapz(E, N);
        high_energy_particles = trapz(E(E > E_threshold), N(E > E_threshold));
        high_energy_fraction(i) = high_energy_particles / total_particles;
    end
    
    plot(T_fine, high_energy_fraction * 100, 'g-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('高能态占比 (%)');
    title(sprintf('高能态占比 (E > %.1f×10^{-20} J)', E_threshold*1e20));
    grid on;
    
    fprintf('温度效应分析完成！\n');
    fprintf('温度范围：%.0f - %.0f K\n', T_range(1), T_range(2));
    fprintf('在%.0f K时，高能态占比约为%.1f%%\n', T_fine(end), high_energy_fraction(end)*100);
end

% 3. 能级分布分析
function energy_level_analysis(k_B)
    fprintf('\n====================================\n');
    fprintf('    能级分布分析\n');
    fprintf('====================================\n');
    
    % 输入参数
    fprintf('请输入能级参数：\n');
    n_levels = input('能级数目 (默认10): ');
    if isempty(n_levels)
        n_levels = 10;
    end
    
    spacing_type = input('能级间距类型 (1-等间距, 2-平方关系, 3-指数关系, 默认1): ');
    if isempty(spacing_type)
        spacing_type = 1;
    end
    
    T = input('温度 (K，默认300): ');
    if isempty(T)
        T = 300;
    end
    
    % 生成能级
    switch spacing_type
        case 1 % 等间距
            delta_E = 1e-20; % J
            E_levels = (0:n_levels-1) * delta_E;
            spacing_name = '等间距';
        case 2 % 平方关系 (谐振子)
            delta_E = 1e-20; % J
            E_levels = ((0:n_levels-1).^2) * delta_E;
            spacing_name = '平方关系 (谐振子)';
        case 3 % 指数关系
            delta_E = 1e-20; % J
            E_levels = (exp(0:n_levels-1) - 1) * delta_E;
            spacing_name = '指数关系';
    end
    
    % 计算各能级的粒子数
    N_levels = exp(-E_levels ./ (k_B * T));
    N_levels = N_levels / N_levels(1); % 归一化到基态
    
    % 创建图形
    figure('Name', '能级分布分析', 'NumberTitle', 'off');
    
    % 能级图
    subplot(2,2,1);
    for i = 1:n_levels
        % 画能级线
        line([i-0.4, i+0.4], [E_levels(i), E_levels(i)]*1e20, 'Color', 'k', 'LineWidth', 2);
        % 标注能级
        text(i+0.5, E_levels(i)*1e20, sprintf('E_{%d}', i-1), 'FontSize', 8);
    end
    xlabel('能级序号');
    ylabel('能量 (×10^{-20} J)');
    title(['能级结构 - ' spacing_name]);
    grid on;
    xlim([0.5, n_levels+0.5]);
    
    % 粒子数分布
    subplot(2,2,2);
    bar(1:n_levels, N_levels, 'FaceColor', 'b', 'FaceAlpha', 0.7);
    xlabel('能级序号');
    ylabel('相对粒子数');
    title(sprintf('粒子数分布 (T = %.0f K)', T));
    grid on;
    
    % 半对数粒子数分布
    subplot(2,2,3);
    semilogy(1:n_levels, N_levels, 'ro-', 'LineWidth', 2, 'MarkerSize', 8);
    xlabel('能级序号');
    ylabel('相对粒子数 (对数)');
    title('粒子数分布 (半对数)');
    grid on;
    
    % 统计信息
    subplot(2,2,4);
    % 计算配分函数
    Z = sum(N_levels);
    % 计算平均能量
    E_avg = sum(E_levels .* N_levels) / Z;
    % 计算熵
    p_i = N_levels / Z; % 概率
    S = -k_B * sum(p_i .* log(p_i + 1e-10)); % 避免log(0)
    
    text(0.1, 0.9, '统计热力学参数：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('温度：%.0f K', T), 'FontSize', 10);
    text(0.1, 0.7, sprintf('配分函数：%.4f', Z), 'FontSize', 10);
    text(0.1, 0.6, sprintf('平均能量：%.2e J', E_avg), 'FontSize', 10);
    text(0.1, 0.5, sprintf('熵：%.2e J/K', S), 'FontSize', 10);
    text(0.1, 0.4, sprintf('基态占比：%.1f%%', N_levels(1)/Z*100), 'FontSize', 10);
    text(0.1, 0.3, sprintf('能级间距类型：%s', spacing_name), 'FontSize', 10);
    
    axis off;
    title('统计参数');
    
    % 输出结果
    fprintf('能级分布分析结果：\n');
    fprintf('能级间距类型：%s\n', spacing_name);
    fprintf('配分函数：%.4f\n', Z);
    fprintf('平均能量：%.2e J\n', E_avg);
    fprintf('基态占比：%.1f%%\n', N_levels(1)/Z*100);
end

% 4. 化学反应平衡分析
function chemical_equilibrium_analysis(k_B)
    fprintf('\n====================================\n');
    fprintf('    化学反应平衡分析\n');
    fprintf('====================================\n');
    
    % 输入参数
    fprintf('分析化学反应：A ⇌ B\n');
    delta_E = input('反应能量差 ΔE (kJ/mol，默认20): ');
    if isempty(delta_E)
        delta_E = 20;
    end
    delta_E = delta_E * 1000 / 6.022e23; % 转换为J/分子
    
    T_range = input('温度范围 [T_min, T_max] (K，默认[200, 800]): ');
    if isempty(T_range)
        T_range = [200, 800];
    end
    
    % 温度序列
    T_values = linspace(T_range(1), T_range(2), 100);
    
    % 计算平衡常数
    K_eq = exp(-delta_E ./ (k_B * T_values));
    
    % 计算摩尔分数
    % 假设初始只有A，平衡时：[A] = 1-x, [B] = x
    % K = [B]/[A] = x/(1-x)
    % 解得：x = K/(1+K)
    x_B = K_eq ./ (1 + K_eq);
    x_A = 1 - x_B;
    
    % 创建图形
    figure('Name', '化学反应平衡分析', 'NumberTitle', 'off');
    
    % 平衡常数随温度变化
    subplot(2,2,1);
    semilogy(T_values, K_eq, 'b-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('平衡常数 K_{eq}');
    title('平衡常数随温度变化');
    grid on;
    
    % 摩尔分数随温度变化
    subplot(2,2,2);
    plot(T_values, x_A, 'r-', 'LineWidth', 2);
    hold on;
    plot(T_values, x_B, 'b-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('摩尔分数');
    title('摩尔分数随温度变化');
    legend('反应物 A', '产物 B', 'Location', 'best');
    grid on;
    
    % 反应进度随温度变化
    subplot(2,2,3);
    plot(T_values, x_B * 100, 'g-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('反应进度 (%)');
    title('反应进度随温度变化');
    grid on;
    
    % 范特霍夫方程验证
    subplot(2,2,4);
    plot(1./T_values, log(K_eq), 'ko-', 'LineWidth', 1, 'MarkerSize', 4);
    xlabel('1/T (K^{-1})');
    ylabel('ln(K_{eq})');
    title('范特霍夫方程 (ln K vs 1/T)');
    grid on;
    
    % 线性拟合
    hold on;
    p = polyfit(1./T_values, log(K_eq), 1);
    plot(1./T_values, polyval(p, 1./T_values), 'r-', 'LineWidth', 2);
    legend('数据点', '线性拟合', 'Location', 'best');
    
    % 输出结果
    fprintf('化学反应平衡分析结果：\n');
    fprintf('反应能量差：%.1f kJ/mol\n', delta_E * 6.022e23 / 1000);
    fprintf('在%.0f K时，平衡常数：%.2e\n', T_range(1), K_eq(1));
    fprintf('在%.0f K时，平衡常数：%.2e\n', T_range(2), K_eq(end));
    fprintf('在%.0f K时，产物B的摩尔分数：%.1f%%\n', T_range(1), x_B(1)*100);
    fprintf('在%.0f K时，产物B的摩尔分数：%.1f%%\n', T_range(2), x_B(end)*100);
end

% 5. 光谱线强度分析
function spectral_intensity_analysis(k_B, h, c)
    fprintf('\n====================================\n');
    fprintf('    光谱线强度分析\n');
    fprintf('====================================\n');
    
    % 输入参数
    fprintf('分析原子或分子的光谱线强度\n');
    T = input('温度 (K，默认2000): ');
    if isempty(T)
        T = 2000;
    end
    
    % 能级数据 (以氢原子为例)
    n_levels = 8;
    E_levels = zeros(1, n_levels);
    for n = 1:n_levels
        E_levels(n) = -13.6 * (1 - 1/n^2) * 1.602e-19; % eV转J
    end
    
    % 统计权重 (简化)
    g_levels = 2 * (1:n_levels).^2; % 2n²
    
    % 计算各能级的粒子数密度
    N_levels = g_levels .* exp(-E_levels ./ (k_B * T));
    
    % 归一化
    N_levels = N_levels / sum(N_levels);
    
    % 创建图形
    figure('Name', '光谱线强度分析', 'NumberTitle', 'off');
    
    % 能级图
    subplot(2,2,1);
    for i = 1:n_levels
        % 画能级线
        line([i-0.4, i+0.4], [E_levels(i), E_levels(i)]*6.242e18, 'Color', 'k', 'LineWidth', 2);
        % 标注能级
        text(i+0.5, E_levels(i)*6.242e18, sprintf('n=%d', i), 'FontSize', 8);
    end
    xlabel('主量子数 n');
    ylabel('能量 (eV)');
    title('氢原子能级结构');
    grid on;
    xlim([0.5, n_levels+0.5]);
    
    % 粒子数密度分布
    subplot(2,2,2);
    bar(1:n_levels, N_levels, 'FaceColor', 'r', 'FaceAlpha', 0.7);
    xlabel('主量子数 n');
    ylabel('相对粒子数密度');
    title(sprintf('能级粒子数密度 (T = %.0f K)', T));
    grid on;
    
    % 计算跃迁强度 (以巴尔末系为例)
    subplot(2,2,3);
    n_upper = 3:n_levels;
    n_lower = 2;
    
    % 跃迁波长
    lambda = zeros(size(n_upper));
    intensity = zeros(size(n_upper));
    
    for i = 1:length(n_upper)
        nu = n_upper(i);
        nl = n_lower;
        
        % 计算波长 (里德伯公式)
        R_H = 1.097e7; % 里德伯常数 (m⁻¹)
        lambda(i) = 1 / (R_H * (1/nl^2 - 1/nu^2));
        
        % 跃迁强度正比于上能级粒子数
        intensity(i) = N_levels(nu);
    end
    
    bar(lambda*1e9, intensity/max(intensity), 'FaceColor', 'b', 'FaceAlpha', 0.7);
    xlabel('波长 (nm)');
    ylabel('相对强度');
    title('巴尔末系光谱线强度');
    grid on;
    
    % 统计信息
    subplot(2,2,4);
    % 计算配分函数
    Z = sum(g_levels .* exp(-E_levels ./ (k_B * T)));
    
    % 计算平均能量
    E_avg = sum(E_levels .* N_levels);
    
    text(0.1, 0.9, '光谱分析参数：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('温度：%.0f K', T), 'FontSize', 10);
    text(0.1, 0.7, sprintf('配分函数：%.2e', Z), 'FontSize', 10);
    text(0.1, 0.6, sprintf('平均能量：%.2f eV', E_avg*6.242e18), 'FontSize', 10);
    text(0.1, 0.5, sprintf('基态占比：%.1f%%', N_levels(1)*100), 'FontSize', 10);
    text(0.1, 0.4, '最强谱线：', 'FontSize', 10);
    [~, idx] = max(intensity);
    text(0.1, 0.3, sprintf('  %d→%d: %.1f nm', n_upper(idx), n_lower, lambda(idx)*1e9), 'FontSize', 10);
    
    axis off;
    title('分析参数');
    
    % 输出结果
    fprintf('光谱线强度分析结果：\n');
    fprintf('温度：%.0f K\n', T);
    fprintf('基态占比：%.1f%%\n', N_levels(1)*100);
    fprintf('最强巴尔末系谱线：%d→%d，波长%.1f nm\n', n_upper(idx), n_lower, lambda(idx)*1e9);
end

% 6. 完整分析
function complete_analysis(k_B, h, c, N_A)
    fprintf('\n====================================\n');
    fprintf('    完整玻尔兹曼分布分析\n');
    fprintf('====================================\n');
    
    % 输入参数
    T = input('分析温度 (K，默认500): ');
    if isempty(T)
        T = 500;
    end
    
    % 创建大图窗
    figure('Name', '完整玻尔兹曼分布分析', 'NumberTitle', 'off');
    set(gcf, 'Position', [50, 50, 1400, 900]);
    
    % 1. 基本分布
    subplot(3,4,1);
    E_max = 20e-20; % J
    E = linspace(0, E_max, 1000);
    N = exp(-E ./ (k_B * T));
    plot(E*1e20, N, 'b-', 'LineWidth', 2);
    xlabel('能量 (×10^{-20} J)');
    ylabel('N(E)/N₀');
    title('基本玻尔兹曼分布');
    grid on;
    
    % 2. 半对数分布
    subplot(3,4,2);
    semilogy(E*1e20, N, 'r-', 'LineWidth', 2);
    xlabel('能量 (×10^{-20} J)');
    ylabel('N(E)/N₀');
    title('半对数分布');
    grid on;
    
    % 3. 温度比较
    subplot(3,4,3);
    T_values = [200, 500, 800];
    colors = ['b', 'r', 'g'];
    hold on;
    for i = 1:3
        N_temp = exp(-E ./ (k_B * T_values(i)));
        plot(E*1e20, N_temp, 'Color', colors(i), 'LineWidth', 2);
    end
    xlabel('能量 (×10^{-20} J)');
    ylabel('N(E)/N₀');
    title('温度比较');
    legend('200K', '500K', '800K');
    grid on;
    
    % 4. 麦克斯韦-玻尔兹曼速度分布
    subplot(3,4,4);
    m = 4.65e-26; % 氮气分子质量 (kg)
    v = linspace(0, 2000, 1000);
    f_v = 4*pi * (m/(2*pi*k_B*T))^(3/2) * v.^2 .* exp(-m*v.^2/(2*k_B*T));
    plot(v, f_v, 'b-', 'LineWidth', 2);
    xlabel('速度 (m/s)');
    ylabel('f(v)');
    title('麦克斯韦-玻尔兹曼速度分布');
    grid on;
    
    % 5. 能级分布
    subplot(3,4,5);
    n_levels = 8;
    E_levels = (0:n_levels-1) * 2e-20; % J
    N_levels = exp(-E_levels ./ (k_B * T));
    bar(1:n_levels, N_levels, 'FaceColor', 'g', 'FaceAlpha', 0.7);
    xlabel('能级');
    ylabel('相对粒子数');
    title('离散能级分布');
    grid on;
    
    % 6. 化学反应平衡
    subplot(3,4,6);
    T_range = 200:50:800;
    delta_E = 30e3 / N_A; % J/分子
    K_eq = exp(-delta_E ./ (k_B * T_range));
    semilogy(T_range, K_eq, 'r-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('平衡常数');
    title('化学平衡常数');
    grid on;
    
    % 7. 热容量
    subplot(3,4,7);
    C_v = (E.^2 .* exp(-E ./ (k_B * T))) ./ (k_B * T^2);
    C_v_int = trapz(E, C_v) / trapz(E, exp(-E ./ (k_B * T)));
    T_cv = 100:50:1000;
    C_v_values = zeros(size(T_cv));
    for i = 1:length(T_cv)
        C_v_temp = (E.^2 .* exp(-E ./ (k_B * T_cv(i)))) ./ (k_B * T_cv(i)^2);
        C_v_values(i) = trapz(E, C_v_temp) / trapz(E, exp(-E ./ (k_B * T_cv(i))));
    end
    plot(T_cv, C_v_values/k_B, 'b-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('C_v/k_B');
    title('热容量');
    grid on;
    
    % 8. 配分函数
    subplot(3,4,8);
    Z_values = zeros(size(T_cv));
    for i = 1:length(T_cv)
        Z_values(i) = trapz(E, exp(-E ./ (k_B * T_cv(i))));
    end
    plot(T_cv, Z_values, 'g-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('配分函数 Z');
    title('配分函数');
    grid on;
    
    % 9. 熵
    subplot(3,4,9);
    S_values = zeros(size(T_cv));
    for i = 1:length(T_cv)
        N_temp = exp(-E ./ (k_B * T_cv(i)));
        Z_temp = trapz(E, N_temp);
        p_temp = N_temp / Z_temp;
        S_values(i) = -k_B * trapz(E, p_temp .* log(p_temp + 1e-10));
    end
    plot(T_cv, S_values/k_B, 'r-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('S/k_B');
    title('熵');
    grid on;
    
    % 10. 内能
    subplot(3,4,10);
    U_values = zeros(size(T_cv));
    for i = 1:length(T_cv)
        N_temp = exp(-E ./ (k_B * T_cv(i)));
        Z_temp = trapz(E, N_temp);
        U_values(i) = trapz(E, E .* N_temp) / Z_temp;
    end
    plot(T_cv, U_values*1e20, 'b-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('内能 (×10^{-20} J)');
    title('内能');
    grid on;
    
    % 11. 自由能
    subplot(3,4,11);
    F_values = -k_B * T_cv .* log(Z_values);
    plot(T_cv, F_values*1e20, 'g-', 'LineWidth', 2);
    xlabel('温度 (K)');
    ylabel('自由能 (×10^{-20} J)');
    title('亥姆霍兹自由能');
    grid on;
    
    % 12. 统计参数
    subplot(3,4,12);
    text(0.1, 0.9, '统计热力学参数：', 'FontSize', 10, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('温度：%.0f K', T), 'FontSize', 8);
    text(0.1, 0.7, sprintf('kT = %.2e J', k_B*T), 'FontSize', 8);
    Z_current = trapz(E, exp(-E ./ (k_B * T)));
    text(0.1, 0.6, sprintf('配分函数：%.2e', Z_current), 'FontSize', 8);
    E_avg = trapz(E, E .* exp(-E ./ (k_B * T))) / Z_current;
    text(0.1, 0.5, sprintf('平均能量：%.2e J', E_avg), 'FontSize', 8);
    text(0.1, 0.4, sprintf('E_avg/kT：%.2f', E_avg/(k_B*T)), 'FontSize', 8);
    v_avg = sqrt(8*k_B*T/(pi*m));
    text(0.1, 0.3, sprintf('平均速度：%.0f m/s', v_avg), 'FontSize', 8);
    text(0.1, 0.2, sprintf('(氮气分子)', ''), 'FontSize', 8);
    
    axis off;
    title('统计参数');
    
    % 输出完整分析结果
    fprintf('完整玻尔兹曼分布分析结果：\n');
    fprintf('分析温度：%.0f K\n', T);
    fprintf('玻尔兹曼因子 kT：%.2e J\n', k_B*T);
    fprintf('配分函数：%.2e\n', Z_current);
    fprintf('平均能量：%.2e J (%.2f kT)\n', E_avg, E_avg/(k_B*T));
    fprintf('氮气分子平均速度：%.0f m/s\n', v_avg);
end 