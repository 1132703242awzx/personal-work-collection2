function LTI_System_Analysis()
% LTI系统分析工具
% 功能：LTI连续系统激励与响应关系的数学模型和微分方程求解
% 作者：AI助手
% 日期：2024

clc;
clear;
close all;

fprintf('====================================\n');
fprintf('    LTI系统分析工具 v2.0\n');
fprintf('====================================\n');
fprintf('功能：LTI连续系统激励与响应关系分析\n');
fprintf('包含：数学建模、微分方程求解、性能分析\n');
fprintf('====================================\n\n');

% 分析类型选择
fprintf('请选择分析类型：\n');
fprintf('1. 传递函数分析\n');
fprintf('2. 脉冲响应分析\n');
fprintf('3. 阶跃响应分析\n');
fprintf('4. 频率响应分析\n');
fprintf('5. 微分方程求解 ← 数值求解功能\n');
fprintf('6. 完整分析\n');
analysis_type = input('请输入选择 (1-6): ');

% 系统参数输入
fprintf('\n====================================\n');
fprintf('系统传递函数：G(s) = B(s)/A(s)\n');
fprintf('例：G(s) = (s+1)/(s²+3s+2)\n');
fprintf('分母A(s): s²+3s+2 → 输入 [1,3,2]\n');
fprintf('分子B(s): s+1 → 输入 [1,1]\n');
fprintf('====================================\n');

% 输入系统参数
a = input('请输入分母系数向量 a (如 [1,3,2]): ');
b = input('请输入分子系数向量 b (如 [1,1]): ');

% 验证输入
if isempty(a) || isempty(b)
    error('系数向量不能为空！');
end

% 创建传递函数
sys = tf(b, a);
fprintf('\n系统传递函数：\n');
disp(sys);

% 根据选择执行相应分析
switch analysis_type
    case 1
        analyze_transfer_function(sys);
    case 2
        analyze_impulse_response(sys);
    case 3
        analyze_step_response(sys);
    case 4
        analyze_frequency_response(sys);
    case 5
        solve_differential_equation(a, b);  % 微分方程求解
    case 6
        complete_analysis(sys, a, b);
    otherwise
        error('无效的选择！');
end

fprintf('\n====================================\n');
fprintf('分析完成！请查看图形结果。\n');
fprintf('====================================\n');

end

% 传递函数分析
function analyze_transfer_function(sys)
    figure('Name', 'LTI系统传递函数分析', 'NumberTitle', 'off');
    
    % 零极点图
    subplot(2,2,1);
    pzmap(sys);
    grid on;
    title('零极点图');
    
    % 根轨迹
    subplot(2,2,2);
    rlocus(sys);
    grid on;
    title('根轨迹');
    
    % 系统信息
    subplot(2,2,3);
    poles = pole(sys);
    zeros = zero(sys);
    
    text(0.1, 0.8, '系统特性：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.7, sprintf('系统阶数：%d', length(poles)), 'FontSize', 10);
    text(0.1, 0.6, sprintf('极点个数：%d', length(poles)), 'FontSize', 10);
    text(0.1, 0.5, sprintf('零点个数：%d', length(zeros)), 'FontSize', 10);
    
    % 稳定性判断
    if all(real(poles) < 0)
        stability = '稳定';
    else
        stability = '不稳定';
    end
    text(0.1, 0.4, sprintf('稳定性：%s', stability), 'FontSize', 10);
    
    axis off;
    title('系统特性');
    
    % 传递函数表达式
    subplot(2,2,4);
    [num, den] = tfdata(sys, 'v');
    
    % 构建传递函数字符串
    num_str = poly2str(num, 's');
    den_str = poly2str(den, 's');
    
    text(0.1, 0.7, 'G(s) = ', 'FontSize', 14, 'FontWeight', 'bold');
    text(0.3, 0.8, num_str, 'FontSize', 12);
    text(0.3, 0.6, repmat('-', 1, max(length(num_str), length(den_str))), 'FontSize', 12);
    text(0.3, 0.4, den_str, 'FontSize', 12);
    
    axis off;
    title('传递函数');
end

% 脉冲响应分析
function analyze_impulse_response(sys)
    figure('Name', 'LTI系统脉冲响应分析', 'NumberTitle', 'off');
    
    % 脉冲响应
    subplot(2,2,1);
    impulse(sys);
    grid on;
    title('脉冲响应');
    
    % 脉冲响应信息
    [y, t] = impulse(sys);
    
    subplot(2,2,2);
    plot(t, y, 'b-', 'LineWidth', 2);
    xlabel('时间 (s)');
    ylabel('幅值');
    title('脉冲响应曲线');
    grid on;
    
    % 性能指标
    subplot(2,2,3);
    peak_value = max(abs(y));
    peak_time = t(find(abs(y) == peak_value, 1));
    settling_time = find(abs(y) < 0.02*peak_value, 1);
    if ~isempty(settling_time)
        settling_time = t(settling_time);
    else
        settling_time = t(end);
    end
    
    text(0.1, 0.8, '性能指标：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.7, sprintf('峰值：%.4f', peak_value), 'FontSize', 10);
    text(0.1, 0.6, sprintf('峰值时间：%.4f s', peak_time), 'FontSize', 10);
    text(0.1, 0.5, sprintf('调节时间：%.4f s', settling_time), 'FontSize', 10);
    
    axis off;
    title('性能指标');
    
    % 频域特性
    subplot(2,2,4);
    [mag, phase, w] = bode(sys);
    mag = squeeze(mag);
    phase = squeeze(phase);
    
    yyaxis left;
    semilogx(w, 20*log10(mag), 'b-', 'LineWidth', 2);
    ylabel('幅值 (dB)');
    
    yyaxis right;
    semilogx(w, phase, 'r-', 'LineWidth', 2);
    ylabel('相位 (度)');
    
    xlabel('频率 (rad/s)');
    title('频率响应');
    grid on;
end

% 阶跃响应分析
function analyze_step_response(sys)
    figure('Name', 'LTI系统阶跃响应分析', 'NumberTitle', 'off');
    
    % 阶跃响应
    subplot(2,2,1);
    step(sys);
    grid on;
    title('阶跃响应');
    
    % 阶跃响应信息
    [y, t] = step(sys);
    info = stepinfo(sys);
    
    subplot(2,2,2);
    plot(t, y, 'b-', 'LineWidth', 2);
    hold on;
    if isfield(info, 'Overshoot') && info.Overshoot > 0
        plot(info.PeakTime, info.Peak, 'ro', 'MarkerSize', 8);
    end
    xlabel('时间 (s)');
    ylabel('幅值');
    title('阶跃响应曲线');
    grid on;
    legend('响应曲线', '峰值点');
    
    % 性能指标
    subplot(2,2,3);
    text(0.1, 0.9, '阶跃响应性能指标：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('上升时间：%.4f s', info.RiseTime), 'FontSize', 10);
    text(0.1, 0.7, sprintf('峰值时间：%.4f s', info.PeakTime), 'FontSize', 10);
    text(0.1, 0.6, sprintf('调节时间：%.4f s', info.SettlingTime), 'FontSize', 10);
    text(0.1, 0.5, sprintf('超调量：%.2f%%', info.Overshoot), 'FontSize', 10);
    text(0.1, 0.4, sprintf('峰值：%.4f', info.Peak), 'FontSize', 10);
    text(0.1, 0.3, sprintf('稳态值：%.4f', info.SteadyStateValue), 'FontSize', 10);
    
    axis off;
    title('性能指标');
    
    % 误差分析
    subplot(2,2,4);
    steady_state = info.SteadyStateValue;
    error = abs(y - steady_state);
    
    semilogy(t, error, 'r-', 'LineWidth', 2);
    xlabel('时间 (s)');
    ylabel('误差');
    title('误差收敛曲线');
    grid on;
end

% 频率响应分析
function analyze_frequency_response(sys)
    figure('Name', 'LTI系统频率响应分析', 'NumberTitle', 'off');
    
    % 伯德图
    subplot(2,2,1);
    bode(sys);
    grid on;
    title('伯德图');
    
    % 奈奎斯特图
    subplot(2,2,2);
    nyquist(sys);
    grid on;
    title('奈奎斯特图');
    
    % 尼柯尔斯图
    subplot(2,2,3);
    nichols(sys);
    grid on;
    title('尼柯尔斯图');
    
    % 稳定性分析
    subplot(2,2,4);
    [Gm, Pm, Wcg, Wcp] = margin(sys);
    
    text(0.1, 0.8, '稳定性分析：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.7, sprintf('增益裕度：%.2f dB', 20*log10(Gm)), 'FontSize', 10);
    text(0.1, 0.6, sprintf('相位裕度：%.2f°', Pm), 'FontSize', 10);
    text(0.1, 0.5, sprintf('增益交越频率：%.4f rad/s', Wcg), 'FontSize', 10);
    text(0.1, 0.4, sprintf('相位交越频率：%.4f rad/s', Wcp), 'FontSize', 10);
    
    % 稳定性判断
    if Gm > 1 && Pm > 0
        stability = '稳定';
    else
        stability = '不稳定';
    end
    text(0.1, 0.3, sprintf('系统稳定性：%s', stability), 'FontSize', 10);
    
    axis off;
    title('稳定性分析');
end

% 微分方程求解 - 核心功能
function solve_differential_equation(a, b)
    fprintf('\n====================================\n');
    fprintf('    微分方程数值求解功能\n');
    fprintf('====================================\n');
    
    % 显示微分方程形式
    fprintf('系统微分方程形式：\n');
    n = length(a);
    m = length(b);
    
    fprintf('输出方程：');
    for i = 1:n
        if i == 1
            fprintf('%.2f*y', a(i));
        else
            fprintf(' + %.2f*y', a(i));
            for j = 1:n-i
                fprintf('^(%d)', j);
            end
        end
    end
    
    fprintf(' = ');
    
    for i = 1:m
        if i == 1
            fprintf('%.2f*u', b(i));
        else
            fprintf(' + %.2f*u', b(i));
            for j = 1:m-i
                fprintf('^(%d)', j);
            end
        end
    end
    fprintf('\n');
    
    % 输入信号选择
    fprintf('\n请选择输入信号类型：\n');
    fprintf('1. 阶跃信号\n');
    fprintf('2. 脉冲信号\n');
    fprintf('3. 正弦信号\n');
    fprintf('4. 斜坡信号\n');
    signal_type = input('请输入选择 (1-4): ');
    
    % 初始条件
    fprintf('\n请输入初始条件：\n');
    initial_conditions = zeros(1, n-1);
    for i = 1:n-1
        prompt = sprintf('y^(%d)(0) = ', i-1);
        initial_conditions(i) = input(prompt);
    end
    
    % 仿真参数
    fprintf('\n请输入仿真参数：\n');
    t_final = input('仿真时间 (s，默认10): ');
    if isempty(t_final)
        t_final = 10;
    end
    
    % 时间向量
    t = linspace(0, t_final, 1000);
    
    % 生成输入信号
    switch signal_type
        case 1 % 阶跃信号
            amplitude = input('阶跃幅值 (默认1): ');
            if isempty(amplitude)
                amplitude = 1;
            end
            u = amplitude * ones(size(t));
            signal_name = sprintf('阶跃信号 (幅值=%.2f)', amplitude);
            
        case 2 % 脉冲信号
            amplitude = input('脉冲幅值 (默认1): ');
            if isempty(amplitude)
                amplitude = 1;
            end
            u = zeros(size(t));
            u(1) = amplitude;
            signal_name = sprintf('脉冲信号 (幅值=%.2f)', amplitude);
            
        case 3 % 正弦信号
            amplitude = input('正弦幅值 (默认1): ');
            if isempty(amplitude)
                amplitude = 1;
            end
            frequency = input('正弦频率 (rad/s，默认1): ');
            if isempty(frequency)
                frequency = 1;
            end
            u = amplitude * sin(frequency * t);
            signal_name = sprintf('正弦信号 (幅值=%.2f, 频率=%.2f rad/s)', amplitude, frequency);
            
        case 4 % 斜坡信号
            slope = input('斜坡斜率 (默认1): ');
            if isempty(slope)
                slope = 1;
            end
            u = slope * t;
            signal_name = sprintf('斜坡信号 (斜率=%.2f)', slope);
    end
    
    % 使用lsim求解
    [y, t_out] = lsim(tf(b, a), u, t, initial_conditions);
    
    % 绘制结果
    figure('Name', 'LTI系统微分方程数值求解', 'NumberTitle', 'off');
    
    % 输入信号
    subplot(3,2,1);
    plot(t, u, 'b-', 'LineWidth', 2);
    xlabel('时间 (s)');
    ylabel('幅值');
    title(['输入信号：' signal_name]);
    grid on;
    
    % 输出响应
    subplot(3,2,2);
    plot(t_out, y, 'r-', 'LineWidth', 2);
    xlabel('时间 (s)');
    ylabel('幅值');
    title('系统输出响应');
    grid on;
    
    % 输入输出对比
    subplot(3,2,3);
    plot(t, u, 'b-', 'LineWidth', 2);
    hold on;
    plot(t_out, y, 'r-', 'LineWidth', 2);
    xlabel('时间 (s)');
    ylabel('幅值');
    title('输入输出对比');
    legend('输入信号', '输出响应');
    grid on;
    
    % 相平面图 (如果是二阶系统)
    if length(a) == 3
        subplot(3,2,4);
        dy = gradient(y) ./ gradient(t_out);
        plot(y, dy, 'g-', 'LineWidth', 2);
        xlabel('y');
        ylabel('dy/dt');
        title('相平面图');
        grid on;
    else
        subplot(3,2,4);
        text(0.3, 0.5, '相平面图', 'FontSize', 14, 'HorizontalAlignment', 'center');
        text(0.3, 0.4, '(仅适用于二阶系统)', 'FontSize', 12, 'HorizontalAlignment', 'center');
        axis off;
    end
    
    % 数值求解信息
    subplot(3,2,5);
    text(0.1, 0.9, '数值求解信息：', 'FontSize', 12, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('系统阶数：%d', length(a)-1), 'FontSize', 10);
    text(0.1, 0.7, sprintf('仿真时间：%.2f s', t_final), 'FontSize', 10);
    text(0.1, 0.6, sprintf('采样点数：%d', length(t)), 'FontSize', 10);
    text(0.1, 0.5, sprintf('最大输出：%.4f', max(y)), 'FontSize', 10);
    text(0.1, 0.4, sprintf('最小输出：%.4f', min(y)), 'FontSize', 10);
    text(0.1, 0.3, sprintf('稳态值：%.4f', y(end)), 'FontSize', 10);
    
    axis off;
    title('求解信息');
    
    % 频谱分析
    subplot(3,2,6);
    Y = fft(y);
    f = (0:length(Y)-1) * (1/(t_out(2)-t_out(1))) / length(Y);
    
    plot(f(1:floor(length(f)/2)), abs(Y(1:floor(length(Y)/2))), 'k-', 'LineWidth', 2);
    xlabel('频率 (Hz)');
    ylabel('幅值');
    title('输出信号频谱');
    grid on;
    
    % 保存结果
    fprintf('\n====================================\n');
    fprintf('微分方程数值求解完成！\n');
    fprintf('结果已保存到工作空间变量：\n');
    fprintf('  t_out: 时间向量\n');
    fprintf('  y: 输出响应\n');
    fprintf('  u: 输入信号\n');
    fprintf('====================================\n');
    
    % 导出到工作空间
    assignin('base', 't_out', t_out);
    assignin('base', 'y', y);
    assignin('base', 'u', u);
end

% 完整分析
function complete_analysis(sys, a, b)
    fprintf('\n====================================\n');
    fprintf('    执行完整系统分析\n');
    fprintf('====================================\n');
    
    % 创建大图窗
    figure('Name', 'LTI系统完整分析', 'NumberTitle', 'off');
    set(gcf, 'Position', [100, 100, 1400, 900]);
    
    % 1. 零极点图
    subplot(3,4,1);
    pzmap(sys);
    grid on;
    title('零极点图');
    
    % 2. 阶跃响应
    subplot(3,4,2);
    step(sys);
    grid on;
    title('阶跃响应');
    
    % 3. 脉冲响应
    subplot(3,4,3);
    impulse(sys);
    grid on;
    title('脉冲响应');
    
    % 4. 伯德图
    subplot(3,4,4);
    bode(sys);
    grid on;
    title('伯德图');
    
    % 5. 奈奎斯特图
    subplot(3,4,5);
    nyquist(sys);
    grid on;
    title('奈奎斯特图');
    
    % 6. 尼柯尔斯图
    subplot(3,4,6);
    nichols(sys);
    grid on;
    title('尼柯尔斯图');
    
    % 7. 根轨迹
    subplot(3,4,7);
    rlocus(sys);
    grid on;
    title('根轨迹');
    
    % 8. 性能指标
    subplot(3,4,8);
    info = stepinfo(sys);
    text(0.1, 0.9, '性能指标：', 'FontSize', 10, 'FontWeight', 'bold');
    text(0.1, 0.8, sprintf('上升时间：%.4f s', info.RiseTime), 'FontSize', 8);
    text(0.1, 0.7, sprintf('调节时间：%.4f s', info.SettlingTime), 'FontSize', 8);
    text(0.1, 0.6, sprintf('超调量：%.2f%%', info.Overshoot), 'FontSize', 8);
    text(0.1, 0.5, sprintf('峰值：%.4f', info.Peak), 'FontSize', 8);
    axis off;
    title('性能指标');
    
    % 9. 稳定性分析
    subplot(3,4,9);
    [Gm, Pm, Wcg, Wcp] = margin(sys);
    text(0.1, 0.8, '稳定性：', 'FontSize', 10, 'FontWeight', 'bold');
    text(0.1, 0.7, sprintf('增益裕度：%.2f dB', 20*log10(Gm)), 'FontSize', 8);
    text(0.1, 0.6, sprintf('相位裕度：%.2f°', Pm), 'FontSize', 8);
    text(0.1, 0.5, sprintf('增益交越：%.4f', Wcg), 'FontSize', 8);
    text(0.1, 0.4, sprintf('相位交越：%.4f', Wcp), 'FontSize', 8);
    axis off;
    title('稳定性分析');
    
    % 10. 传递函数
    subplot(3,4,10);
    [num, den] = tfdata(sys, 'v');
    num_str = poly2str(num, 's');
    den_str = poly2str(den, 's');
    text(0.1, 0.7, 'G(s) = ', 'FontSize', 10, 'FontWeight', 'bold');
    text(0.1, 0.6, num_str, 'FontSize', 8);
    text(0.1, 0.5, repmat('-', 1, 20), 'FontSize', 8);
    text(0.1, 0.4, den_str, 'FontSize', 8);
    axis off;
    title('传递函数');
    
    % 11. 频率响应数据
    subplot(3,4,11);
    [mag, phase, w] = bode(sys);
    mag = squeeze(mag);
    phase = squeeze(phase);
    
    loglog(w, mag, 'b-', 'LineWidth', 2);
    xlabel('频率 (rad/s)');
    ylabel('幅值');
    title('幅频响应');
    grid on;
    
    % 12. 相频响应
    subplot(3,4,12);
    semilogx(w, phase, 'r-', 'LineWidth', 2);
    xlabel('频率 (rad/s)');
    ylabel('相位 (度)');
    title('相频响应');
    grid on;
    
    % 同时执行微分方程求解
    fprintf('同时执行微分方程数值求解...\n');
    solve_differential_equation(a, b);
end

% 辅助函数：多项式转字符串
function str = poly2str(p, var)
    if nargin < 2
        var = 'x';
    end
    
    n = length(p);
    str = '';
    
    for i = 1:n
        coeff = p(i);
        power = n - i;
        
        if abs(coeff) < 1e-10
            continue;
        end
        
        if i > 1 && coeff > 0
            str = [str, ' + '];
        elseif coeff < 0
            str = [str, ' - '];
            coeff = -coeff;
        end
        
        if power == 0
            str = [str, sprintf('%.4g', coeff)];
        elseif power == 1
            if abs(coeff - 1) < 1e-10
                str = [str, var];
            else
                str = [str, sprintf('%.4g*%s', coeff, var)];
            end
        else
            if abs(coeff - 1) < 1e-10
                str = [str, sprintf('%s^%d', var, power)];
            else
                str = [str, sprintf('%.4g*%s^%d', coeff, var, power)];
            end
        end
    end
    
    if isempty(str)
        str = '0';
    end
end 