"""
流体力学模拟器 - 二维不可压缩流体模拟
基于Navier-Stokes方程的数值求解

作者：用户
日期：2025年8月29日
版本：1.0

物理原理：
- 使用有限差分法求解Navier-Stokes方程
- 实现扩散（diffusion）、平流（advection）和压力投影（projection）
- 模拟染料在流体中的扩散和运动
"""

# =============================================================================
# 第一部分：导入必要的库
# =============================================================================

import numpy as np
import matplotlib
# 设置matplotlib后端为Agg，避免GUI相关错误
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import gaussian_filter
import time
import os

# =============================================================================
# 第二部分：定义模拟参数和网格
# =============================================================================

class FluidSimulator:
    """
    流体模拟器类
    实现基于格子Boltzmann方法的简化版流体模拟
    """
    
    def __init__(self, size=64, dt=0.1, diffusion=0.0001, viscosity=0.0001):
        """
        初始化流体模拟器
        
        参数:
        size: int - 网格大小 (size x size)
        dt: float - 时间步长
        diffusion: float - 扩散率
        viscosity: float - 粘度
        """
        # 网格参数
        self.size = size
        self.dt = dt
        self.diffusion = diffusion
        self.viscosity = viscosity
        
        # 计算网格坐标
        self.x = np.linspace(0, 1, size)
        self.y = np.linspace(0, 1, size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # 初始化物理场
        self._initialize_fields()
        
        # 迭代参数
        self.gauss_seidel_iterations = 20  # Gauss-Seidel迭代次数
        
    def _initialize_fields(self):
        """初始化速度场和密度场"""
        # 速度场 (Vx, Vy)
        self.vx = np.zeros((self.size, self.size), dtype=np.float64)
        self.vy = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 前一步的速度场（用于时间积分）
        self.vx_prev = np.zeros((self.size, self.size), dtype=np.float64)
        self.vy_prev = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 密度场（染料浓度）
        self.density = np.zeros((self.size, self.size), dtype=np.float64)
        self.density_prev = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 压力场和散度场
        self.pressure = np.zeros((self.size, self.size), dtype=np.float64)
        self.divergence = np.zeros((self.size, self.size), dtype=np.float64)
        
    # =============================================================================
    # 第三部分：初始化流体场
    # =============================================================================
    
    def add_density_source(self, x, y, radius, intensity):
        """
        在指定位置添加密度源（染料注入）
        
        参数:
        x, y: float - 源的位置 (0-1范围)
        radius: float - 源的半径
        intensity: float - 密度强度
        """
        # 转换为网格坐标
        grid_x = int(x * self.size)
        grid_y = int(y * self.size)
        grid_radius = int(radius * self.size)
        
        # 创建圆形密度源
        for i in range(max(0, grid_x - grid_radius), 
                      min(self.size, grid_x + grid_radius + 1)):
            for j in range(max(0, grid_y - grid_radius), 
                          min(self.size, grid_y + grid_radius + 1)):
                distance = np.sqrt((i - grid_x)**2 + (j - grid_y)**2)
                if distance <= grid_radius:
                    # 高斯分布的密度
                    self.density[j, i] += intensity * np.exp(-distance**2 / (2 * (grid_radius/2)**2))
    
    def add_velocity_source(self, x, y, radius, vx, vy):
        """
        在指定位置添加速度源（创建涡流）
        
        参数:
        x, y: float - 源的位置 (0-1范围)
        radius: float - 影响半径
        vx, vy: float - 速度分量
        """
        grid_x = int(x * self.size)
        grid_y = int(y * self.size)
        grid_radius = int(radius * self.size)
        
        for i in range(max(0, grid_x - grid_radius), 
                      min(self.size, grid_x + grid_radius + 1)):
            for j in range(max(0, grid_y - grid_radius), 
                          min(self.size, grid_y + grid_radius + 1)):
                distance = np.sqrt((i - grid_x)**2 + (j - grid_y)**2)
                if distance <= grid_radius and distance > 0:
                    # 创建涡流
                    strength = np.exp(-distance**2 / (2 * (grid_radius/3)**2))
                    # 切向速度（创建旋转）
                    angle = np.arctan2(j - grid_y, i - grid_x)
                    self.vx[j, i] += vx * strength + 0.5 * strength * np.cos(angle + np.pi/2)
                    self.vy[j, i] += vy * strength + 0.5 * strength * np.sin(angle + np.pi/2)
    
    # =============================================================================
    # 第四部分：核心计算函数
    # =============================================================================
    
    def set_boundary_conditions(self, field, boundary_type='neumann'):
        """
        设置边界条件
        
        参数:
        field: np.array - 要设置边界的场
        boundary_type: str - 边界类型 ('dirichlet' 或 'neumann')
        """
        if boundary_type == 'neumann':
            # Neumann边界条件（法向导数为零）
            field[0, :] = field[1, :]      # 上边界
            field[-1, :] = field[-2, :]    # 下边界
            field[:, 0] = field[:, 1]      # 左边界
            field[:, -1] = field[:, -2]    # 右边界
        elif boundary_type == 'dirichlet':
            # Dirichlet边界条件（值为零）
            field[0, :] = 0    # 上边界
            field[-1, :] = 0   # 下边界
            field[:, 0] = 0    # 左边界
            field[:, -1] = 0   # 右边界
    
    def set_velocity_boundary_conditions(self, vx, vy):
        """设置速度场的边界条件（无滑移边界）"""
        # 水平速度在垂直边界上为零
        vx[:, 0] = 0
        vx[:, -1] = 0
        # 垂直速度在水平边界上为零
        vy[0, :] = 0
        vy[-1, :] = 0
        
        # 角点特殊处理
        vx[0, :] = -vx[1, :]
        vx[-1, :] = -vx[-2, :]
        vy[:, 0] = -vy[:, 1]
        vy[:, -1] = -vy[:, -2]
    
    def diffuse(self, field, field_prev, diff_rate, dt):
        """
        扩散过程 - 求解扩散方程 ∂φ/∂t = D∇²φ
        使用隐式方法（向后欧拉）保证数值稳定性
        
        参数:
        field: np.array - 当前时刻的场
        field_prev: np.array - 前一时刻的场
        diff_rate: float - 扩散率
        dt: float - 时间步长
        """
        a = dt * diff_rate * (self.size - 2) ** 2
        
        # 使用Gauss-Seidel迭代求解线性系统
        # (1 + 4a)φ[i,j] - a(φ[i-1,j] + φ[i+1,j] + φ[i,j-1] + φ[i,j+1]) = φ_prev[i,j]
        for _ in range(self.gauss_seidel_iterations):
            field[1:-1, 1:-1] = (field_prev[1:-1, 1:-1] + a * (
                field[0:-2, 1:-1] + field[2:, 1:-1] + 
                field[1:-1, 0:-2] + field[1:-1, 2:]
            )) / (1 + 4 * a)
            
            self.set_boundary_conditions(field)
    
    def advect(self, field, field_prev, vx, vy, dt):
        """
        平流过程 - 求解平流方程 ∂φ/∂t + u·∇φ = 0
        使用半拉格朗日方法（反向粒子追踪）
        
        参数:
        field: np.array - 当前时刻的场
        field_prev: np.array - 前一时刻的场
        vx, vy: np.array - 速度场
        dt: float - 时间步长
        """
        dt_size = dt * (self.size - 2)
        
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                # 反向追踪粒子轨迹
                x = i - dt_size * vx[i, j]
                y = j - dt_size * vy[i, j]
                
                # 确保坐标在边界内
                x = max(0.5, min(self.size - 1.5, x))
                y = max(0.5, min(self.size - 1.5, y))
                
                # 双线性插值
                i0, i1 = int(x), int(x) + 1
                j0, j1 = int(y), int(y) + 1
                
                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1
                
                field[i, j] = (s0 * (t0 * field_prev[i0, j0] + t1 * field_prev[i0, j1]) +
                              s1 * (t0 * field_prev[i1, j0] + t1 * field_prev[i1, j1]))
    
    def project(self, vx, vy):
        """
        压力投影 - 确保速度场满足不可压缩条件 ∇·u = 0
        求解泊松方程 ∇²p = ∇·u / dt，然后更新速度 u = u - dt∇p
        
        参数:
        vx, vy: np.array - 速度场分量
        """
        h = 1.0 / (self.size - 2)
        
        # 计算速度散度
        self.divergence[1:-1, 1:-1] = -0.5 * h * (
            vx[2:, 1:-1] - vx[0:-2, 1:-1] + 
            vy[1:-1, 2:] - vy[1:-1, 0:-2]
        )
        
        # 初始化压力场
        self.pressure.fill(0)
        
        self.set_boundary_conditions(self.divergence)
        self.set_boundary_conditions(self.pressure)
        
        # 使用Gauss-Seidel迭代求解泊松方程
        for _ in range(self.gauss_seidel_iterations):
            self.pressure[1:-1, 1:-1] = (self.divergence[1:-1, 1:-1] + 
                                       self.pressure[0:-2, 1:-1] + self.pressure[2:, 1:-1] + 
                                       self.pressure[1:-1, 0:-2] + self.pressure[1:-1, 2:]) / 4
            self.set_boundary_conditions(self.pressure)
        
        # 从速度场中减去压力梯度
        vx[1:-1, 1:-1] -= 0.5 * (self.pressure[2:, 1:-1] - self.pressure[0:-2, 1:-1]) / h
        vy[1:-1, 1:-1] -= 0.5 * (self.pressure[1:-1, 2:] - self.pressure[1:-1, 0:-2]) / h
        
        self.set_velocity_boundary_conditions(vx, vy)
    
    def apply_force(self, vx, vy, force_x, force_y, dt):
        """
        施加外力
        
        参数:
        vx, vy: np.array - 速度场
        force_x, force_y: np.array - 力场
        dt: float - 时间步长
        """
        vx += dt * force_x
        vy += dt * force_y
    
    # =============================================================================
    # 第五部分：主循环
    # =============================================================================
    
    def step(self, external_force_x=None, external_force_y=None):
        """
        执行一个时间步的模拟
        
        参数:
        external_force_x, external_force_y: np.array - 外力场（可选）
        """
        # 保存前一步的状态
        self.vx_prev[:] = self.vx
        self.vy_prev[:] = self.vy
        self.density_prev[:] = self.density
        
        # 1. 施加外力
        if external_force_x is not None:
            self.apply_force(self.vx, self.vy, external_force_x, external_force_y, self.dt)
        
        # 2. 速度场扩散（粘性效应）
        self.diffuse(self.vx, self.vx_prev, self.viscosity, self.dt)
        self.diffuse(self.vy, self.vy_prev, self.viscosity, self.dt)
        
        # 3. 压力投影（确保不可压缩性）
        self.project(self.vx, self.vy)
        
        # 4. 速度场平流（自平流）
        self.vx_prev[:] = self.vx
        self.vy_prev[:] = self.vy
        self.advect(self.vx, self.vx_prev, self.vx_prev, self.vy_prev, self.dt)
        self.advect(self.vy, self.vy_prev, self.vx_prev, self.vy_prev, self.dt)
        
        # 5. 再次压力投影
        self.project(self.vx, self.vy)
        
        # 6. 密度场扩散
        self.diffuse(self.density, self.density_prev, self.diffusion, self.dt)
        
        # 7. 密度场平流
        self.density_prev[:] = self.density
        self.advect(self.density, self.density_prev, self.vx, self.vy, self.dt)
    
    def simulate(self, num_steps, save_interval=10):
        """
        运行完整的模拟
        
        参数:
        num_steps: int - 模拟步数
        save_interval: int - 保存数据的间隔
        
        返回:
        frames: list - 保存的帧数据
        """
        frames = []
        
        print(f"开始流体模拟，共 {num_steps} 步...")
        start_time = time.time()
        
        for step in range(num_steps):
            # 执行一步模拟
            self.step()
            
            # 保存关键帧
            if step % save_interval == 0:
                frame_data = {
                    'density': self.density.copy(),
                    'vx': self.vx.copy(),
                    'vy': self.vy.copy(),
                    'step': step
                }
                frames.append(frame_data)
                
            # 进度显示
            if (step + 1) % 50 == 0:
                elapsed = time.time() - start_time
                eta = elapsed * (num_steps - step - 1) / (step + 1)
                print(f"步数: {step + 1}/{num_steps}, "
                      f"已用时: {elapsed:.1f}s, "
                      f"预计剩余: {eta:.1f}s")
        
        total_time = time.time() - start_time
        print(f"模拟完成！总用时: {total_time:.2f}s")
        
        return frames

# =============================================================================
# 第六部分：可视化
# =============================================================================

class FluidVisualizer:
    """流体可视化器"""
    
    def __init__(self, simulator):
        """
        初始化可视化器
        
        参数:
        simulator: FluidSimulator - 流体模拟器实例
        """
        self.simulator = simulator
        
    def plot_static(self, show_density=True, show_velocity=True, show_streamlines=True, save_path=None):
        """
        绘制静态图像
        
        参数:
        show_density: bool - 是否显示密度场
        show_velocity: bool - 是否显示速度矢量
        show_streamlines: bool - 是否显示流线
        save_path: str - 保存路径（如果为None则显示图像）
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        if show_density:
            # 密度场
            im1 = axes[0].imshow(self.simulator.density, cmap='hot', 
                               interpolation='bilinear', origin='lower')
            axes[0].set_title('Density Field (Dye Concentration)')
            axes[0].set_xlabel('X')
            axes[0].set_ylabel('Y')
            plt.colorbar(im1, ax=axes[0])
        
        if show_velocity:
            # 速度矢量场
            skip = 4  # 矢量采样间隔
            X_sub = self.simulator.X[::skip, ::skip]
            Y_sub = self.simulator.Y[::skip, ::skip]
            vx_sub = self.simulator.vx[::skip, ::skip]
            vy_sub = self.simulator.vy[::skip, ::skip]
            
            speed = np.sqrt(vx_sub**2 + vy_sub**2)
            axes[1].quiver(X_sub, Y_sub, vx_sub, vy_sub, speed, 
                          cmap='viridis', scale=5, alpha=0.8)
            axes[1].set_title('Velocity Vector Field')
            axes[1].set_xlabel('X')
            axes[1].set_ylabel('Y')
            axes[1].set_aspect('equal')
        
        if show_streamlines:
            # 流线
            axes[2].streamplot(self.simulator.X, self.simulator.Y, 
                             self.simulator.vx, self.simulator.vy,
                             density=2, color='blue', linewidth=1)
            
            # 叠加密度场作为背景
            axes[2].imshow(self.simulator.density, cmap='Reds', 
                         alpha=0.6, interpolation='bilinear', 
                         extent=[0, 1, 0, 1], origin='lower')
            axes[2].set_title('Streamlines + Density Field')
            axes[2].set_xlabel('X')
            axes[2].set_ylabel('Y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"图像已保存到: {save_path}")
        else:
            # 在Agg后端下无法显示，保存到临时文件
            temp_path = "fluid_simulation_result.png"
            plt.savefig(temp_path, dpi=150, bbox_inches='tight')
            print(f"图像已保存到: {temp_path}")
            
        plt.close(fig)  # 关闭图形避免内存泄漏
    
    def create_animation(self, frames, interval=100, save_path=None):
        """
        创建动画
        
        参数:
        frames: list - 帧数据列表
        interval: int - 帧间隔（毫秒）
        save_path: str - 保存路径（如果为None则保存为默认文件名）
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # 初始化图像
        im = ax.imshow(frames[0]['density'], cmap='hot', 
                      interpolation='bilinear', origin='lower',
                      vmin=0, vmax=np.max([f['density'].max() for f in frames]))
        
        ax.set_title('Fluid Dye Diffusion Animation')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Density')
        
        # 时间文本
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, 
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        def animate(frame_idx):
            """动画更新函数"""
            frame = frames[frame_idx]
            im.set_array(frame['density'])
            time_text.set_text(f'Step: {frame["step"]}')
            return [im, time_text]
        
        # 创建动画
        anim = animation.FuncAnimation(fig, animate, frames=len(frames),
                                     interval=interval, blit=True, repeat=True)
        
        # 保存动画
        if save_path is None:
            save_path = "fluid_animation.gif"
            
        print(f"正在保存动画到 {save_path}...")
        try:
            anim.save(save_path, writer='pillow', fps=10)
            print("动画保存完成！")
        except Exception as e:
            print(f"动画保存失败: {e}")
            # 尝试保存为PNG序列
            print("尝试保存为PNG图像序列...")
            os.makedirs("animation_frames", exist_ok=True)
            for i, frame in enumerate(frames[::5]):  # 每5帧保存一张
                plt.figure(figsize=(8, 8))
                plt.imshow(frame['density'], cmap='hot', origin='lower', interpolation='bilinear')
                plt.title(f'Step: {frame["step"]}')
                plt.colorbar(label='Density')
                plt.savefig(f"animation_frames/frame_{i:03d}.png", dpi=100, bbox_inches='tight')
                plt.close()
            print("PNG序列保存完成！")
        
        plt.close(fig)
        return anim

# =============================================================================
# 主程序
# =============================================================================

def main():
    """主函数 - 演示流体模拟"""
    print("=" * 60)
    print("流体力学模拟器")
    print("模拟染料在流体中的扩散和平流过程")
    print("=" * 60)
    
    # 创建模拟器
    simulator = FluidSimulator(size=80, dt=0.1, diffusion=0.0002, viscosity=0.0001)
    
    # 设置初始条件
    print("设置初始条件...")
    
    # 在中心添加高密度染料
    simulator.add_density_source(0.5, 0.5, 0.1, 100.0)
    
    # 添加一些初始速度场（创建有趣的流动模式）
    simulator.add_velocity_source(0.3, 0.3, 0.15, 2.0, 1.0)
    simulator.add_velocity_source(0.7, 0.7, 0.15, -1.5, -2.0)
    
    # 运行模拟
    num_steps = 300
    frames = simulator.simulate(num_steps, save_interval=5)
    
    # 创建可视化器
    visualizer = FluidVisualizer(simulator)
    
    # 显示最终状态的静态图
    print("显示最终状态...")
    visualizer.plot_static()
    
    # 创建动画
    print("创建动画...")
    visualizer.create_animation(frames, interval=100)
    
    print("模拟完成！")

if __name__ == '__main__':
    main()
