"""
增强版流体力学模拟器 - 包含更多功能和优化
"""

import numpy as np
import matplotlib
# 设置matplotlib后端避免GUI错误
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams
import time
import os

# 设置matplotlib支持中文
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

class EnhancedFluidSimulator:
    """增强版流体模拟器，包含更多物理效果"""
    
    def __init__(self, size=64, dt=0.1, diffusion=0.0001, viscosity=0.0001):
        self.size = size
        self.dt = dt
        self.diffusion = diffusion
        self.viscosity = viscosity
        
        # 创建网格
        self.x = np.linspace(0, 1, size)
        self.y = np.linspace(0, 1, size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # 初始化所有场
        self._initialize_fields()
        
        # 数值参数
        self.iterations = 20
        
    def _initialize_fields(self):
        """初始化所有物理场"""
        # 速度场
        self.vx = np.zeros((self.size, self.size), dtype=np.float64)
        self.vy = np.zeros((self.size, self.size), dtype=np.float64)
        self.vx_prev = np.zeros((self.size, self.size), dtype=np.float64)
        self.vy_prev = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 密度场（多种染料）
        self.density = np.zeros((self.size, self.size), dtype=np.float64)
        self.density_prev = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 温度场（用于浮力效应）
        self.temperature = np.zeros((self.size, self.size), dtype=np.float64)
        self.temperature_prev = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 压力和散度
        self.pressure = np.zeros((self.size, self.size), dtype=np.float64)
        self.divergence = np.zeros((self.size, self.size), dtype=np.float64)
        
        # 涡度（用于分析）
        self.vorticity = np.zeros((self.size, self.size), dtype=np.float64)
    
    def add_circular_obstacle(self, x, y, radius):
        """添加圆形障碍物"""
        grid_x = int(x * self.size)
        grid_y = int(y * self.size)
        grid_radius = int(radius * self.size)
        
        for i in range(self.size):
            for j in range(self.size):
                distance = np.sqrt((i - grid_x)**2 + (j - grid_y)**2)
                if distance <= grid_radius:
                    self.vx[j, i] = 0
                    self.vy[j, i] = 0
    
    def add_temperature_source(self, x, y, radius, temp):
        """添加温度源"""
        grid_x = int(x * self.size)
        grid_y = int(y * self.size)
        grid_radius = int(radius * self.size)
        
        for i in range(max(0, grid_x - grid_radius), 
                      min(self.size, grid_x + grid_radius + 1)):
            for j in range(max(0, grid_y - grid_radius), 
                          min(self.size, grid_y + grid_radius + 1)):
                distance = np.sqrt((i - grid_x)**2 + (j - grid_y)**2)
                if distance <= grid_radius:
                    self.temperature[j, i] += temp * np.exp(-distance**2 / (2 * (grid_radius/2)**2))
    
    def calculate_vorticity(self):
        """计算涡度场"""
        # 涡度 = ∂vy/∂x - ∂vx/∂y
        dvx_dy = np.gradient(self.vx, axis=0)
        dvy_dx = np.gradient(self.vy, axis=1)
        self.vorticity = dvy_dx - dvx_dy
    
    def apply_buoyancy(self, dt, buoyancy_strength=0.1):
        """应用浮力效应"""
        # 浮力正比于温度差
        buoyancy_force = buoyancy_strength * self.temperature
        self.vy += dt * buoyancy_force
    
    def diffuse_gauss_seidel(self, field, field_prev, diff_rate, dt):
        """改进的扩散算法"""
        a = dt * diff_rate * (self.size - 2) ** 2
        
        for _ in range(self.iterations):
            field[1:-1, 1:-1] = (field_prev[1:-1, 1:-1] + a * (
                field[0:-2, 1:-1] + field[2:, 1:-1] + 
                field[1:-1, 0:-2] + field[1:-1, 2:]
            )) / (1 + 4 * a)
            
            # 边界条件
            field[0, :] = field[1, :]
            field[-1, :] = field[-2, :]
            field[:, 0] = field[:, 1]
            field[:, -1] = field[:, -2]
    
    def advect_maccormack(self, field, field_prev, vx, vy, dt):
        """MacCormack方法的平流（更高精度）"""
        dt_size = dt * (self.size - 2)
        
        # 前向步
        field_forward = np.zeros_like(field)
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                x = i - dt_size * vx[i, j]
                y = j - dt_size * vy[i, j]
                
                x = max(0.5, min(self.size - 1.5, x))
                y = max(0.5, min(self.size - 1.5, y))
                
                i0, i1 = int(x), int(x) + 1
                j0, j1 = int(y), int(y) + 1
                
                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1
                
                field_forward[i, j] = (s0 * (t0 * field_prev[i0, j0] + t1 * field_prev[i0, j1]) +
                                     s1 * (t0 * field_prev[i1, j0] + t1 * field_prev[i1, j1]))
        
        # 后向步和修正
        field[:] = field_forward
    
    def project_pressure(self, vx, vy):
        """压力投影方法"""
        h = 1.0 / (self.size - 2)
        
        # 计算散度
        self.divergence[1:-1, 1:-1] = -0.5 * h * (
            vx[2:, 1:-1] - vx[0:-2, 1:-1] + 
            vy[1:-1, 2:] - vy[1:-1, 0:-2]
        )
        
        self.pressure.fill(0)
        
        # 边界条件
        self.divergence[0, :] = self.divergence[1, :]
        self.divergence[-1, :] = self.divergence[-2, :]
        self.divergence[:, 0] = self.divergence[:, 1]
        self.divergence[:, -1] = self.divergence[:, -2]
        
        # 求解泊松方程
        for _ in range(self.iterations):
            self.pressure[1:-1, 1:-1] = (self.divergence[1:-1, 1:-1] + 
                                       self.pressure[0:-2, 1:-1] + self.pressure[2:, 1:-1] + 
                                       self.pressure[1:-1, 0:-2] + self.pressure[1:-1, 2:]) / 4
            
            self.pressure[0, :] = self.pressure[1, :]
            self.pressure[-1, :] = self.pressure[-2, :]
            self.pressure[:, 0] = self.pressure[:, 1]
            self.pressure[:, -1] = self.pressure[:, -2]
        
        # 更新速度
        vx[1:-1, 1:-1] -= 0.5 * (self.pressure[2:, 1:-1] - self.pressure[0:-2, 1:-1]) / h
        vy[1:-1, 1:-1] -= 0.5 * (self.pressure[1:-1, 2:] - self.pressure[1:-1, 0:-2]) / h
        
        # 速度边界条件
        vx[:, 0] = 0
        vx[:, -1] = 0
        vy[0, :] = 0
        vy[-1, :] = 0
    
    def step_simulation(self, apply_buoyancy=False):
        """执行一步模拟"""
        # 保存前一状态
        self.vx_prev[:] = self.vx
        self.vy_prev[:] = self.vy
        self.density_prev[:] = self.density
        self.temperature_prev[:] = self.temperature
        
        # 浮力效应
        if apply_buoyancy:
            self.apply_buoyancy(self.dt)
        
        # 速度扩散
        self.diffuse_gauss_seidel(self.vx, self.vx_prev, self.viscosity, self.dt)
        self.diffuse_gauss_seidel(self.vy, self.vy_prev, self.viscosity, self.dt)
        
        # 压力投影
        self.project_pressure(self.vx, self.vy)
        
        # 速度平流
        self.vx_prev[:] = self.vx
        self.vy_prev[:] = self.vy
        self.advect_maccormack(self.vx, self.vx_prev, self.vx_prev, self.vy_prev, self.dt)
        self.advect_maccormack(self.vy, self.vy_prev, self.vx_prev, self.vy_prev, self.dt)
        
        # 再次压力投影
        self.project_pressure(self.vx, self.vy)
        
        # 密度和温度扩散
        self.diffuse_gauss_seidel(self.density, self.density_prev, self.diffusion, self.dt)
        self.diffuse_gauss_seidel(self.temperature, self.temperature_prev, self.diffusion * 2, self.dt)
        
        # 密度和温度平流
        self.density_prev[:] = self.density
        self.temperature_prev[:] = self.temperature
        self.advect_maccormack(self.density, self.density_prev, self.vx, self.vy, self.dt)
        self.advect_maccormack(self.temperature, self.temperature_prev, self.vx, self.vy, self.dt)
        
        # 计算涡度
        self.calculate_vorticity()

class FluidDemo:
    """流体演示类，包含多种演示场景"""
    
    @staticmethod
    def demo_basic_diffusion():
        """基础扩散演示"""
        print("演示1: 基础扩散")
        sim = EnhancedFluidSimulator(size=60, diffusion=0.0003)
        
        # 添加密度源
        sim.density[30, 30] = 100.0
        
        # 运行模拟
        frames = []
        for step in range(100):
            sim.step_simulation()
            if step % 5 == 0:
                frames.append(sim.density.copy())
        
        # 可视化
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        for i, frame_idx in enumerate([0, 20, 40, 60]):
            if frame_idx < len(frames):
                row, col = i // 2, i % 2
                im = axes[row, col].imshow(frames[frame_idx], cmap='hot', origin='lower')
                axes[row, col].set_title(f'步数: {frame_idx * 5}')
                plt.colorbar(im, ax=axes[row, col])
        
        plt.suptitle('基础扩散过程')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def demo_vortex_dynamics():
        """涡流动力学演示"""
        print("演示2: 涡流动力学")
        sim = EnhancedFluidSimulator(size=80, viscosity=0.00005)
        
        # 创建初始涡流
        center_x, center_y = 40, 40
        for i in range(sim.size):
            for j in range(sim.size):
                dx = i - center_x
                dy = j - center_y
                r = np.sqrt(dx**2 + dy**2)
                if r > 0 and r < 20:
                    strength = np.exp(-r**2 / (2 * 10**2))
                    sim.vx[j, i] = -dy / r * strength * 3
                    sim.vy[j, i] = dx / r * strength * 3
        
        # 添加示踪染料
        sim.density[35:45, 35:45] = 50.0
        
        # 运行并记录
        frames = []
        vorticity_frames = []
        for step in range(200):
            sim.step_simulation()
            if step % 10 == 0:
                frames.append({
                    'density': sim.density.copy(),
                    'vorticity': sim.vorticity.copy(),
                    'step': step
                })
        
        # 创建动画
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        im1 = ax1.imshow(frames[0]['density'], cmap='hot', origin='lower')
        ax1.set_title('密度场')
        
        im2 = ax2.imshow(frames[0]['vorticity'], cmap='RdBu', origin='lower')
        ax2.set_title('涡度场')
        
        def animate(frame_idx):
            frame = frames[frame_idx]
            im1.set_array(frame['density'])
            im2.set_array(frame['vorticity'])
            im2.set_clim(vmin=-np.max(np.abs(frame['vorticity'])), 
                        vmax=np.max(np.abs(frame['vorticity'])))
            return [im1, im2]
        
        anim = animation.FuncAnimation(fig, animate, frames=len(frames),
                                     interval=200, repeat=True)
        plt.show()
        return anim
    
    @staticmethod
    def demo_thermal_convection():
        """热对流演示"""
        print("演示3: 热对流")
        sim = EnhancedFluidSimulator(size=60, diffusion=0.0002, viscosity=0.0001)
        
        # 底部加热
        sim.temperature[-5:, :] = 100.0
        # 顶部冷却
        sim.temperature[:5, :] = 0.0
        
        # 添加示踪染料
        sim.density[50:55, 25:35] = 80.0
        
        frames = []
        for step in range(300):
            sim.step_simulation(apply_buoyancy=True)
            if step % 15 == 0:
                frames.append({
                    'density': sim.density.copy(),
                    'temperature': sim.temperature.copy(),
                    'vx': sim.vx.copy(),
                    'vy': sim.vy.copy()
                })
        
        # 显示最终状态
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        im1 = axes[0, 0].imshow(frames[-1]['density'], cmap='hot', origin='lower')
        axes[0, 0].set_title('最终密度场')
        plt.colorbar(im1, ax=axes[0, 0])
        
        im2 = axes[0, 1].imshow(frames[-1]['temperature'], cmap='coolwarm', origin='lower')
        axes[0, 1].set_title('最终温度场')
        plt.colorbar(im2, ax=axes[0, 1])
        
        # 速度矢量场
        skip = 3
        x_sub = np.arange(0, sim.size, skip)
        y_sub = np.arange(0, sim.size, skip)
        X_sub, Y_sub = np.meshgrid(x_sub, y_sub)
        vx_sub = frames[-1]['vx'][::skip, ::skip]
        vy_sub = frames[-1]['vy'][::skip, ::skip]
        
        axes[1, 0].quiver(X_sub, Y_sub, vx_sub, vy_sub, scale=10)
        axes[1, 0].set_title('速度场')
        axes[1, 0].set_aspect('equal')
        
        # 流线
        axes[1, 1].streamplot(np.arange(sim.size), np.arange(sim.size),
                            frames[-1]['vx'], frames[-1]['vy'], density=2)
        axes[1, 1].set_title('流线')
        
        plt.suptitle('热对流模拟结果')
        plt.tight_layout()
        plt.show()

def main():
    """主程序 - 运行所有演示"""
    print("=" * 60)
    print("增强版流体力学模拟器演示")
    print("=" * 60)
    
    try:
        # 运行各种演示
        FluidDemo.demo_basic_diffusion()
        input("按回车键继续下一个演示...")
        
        anim = FluidDemo.demo_vortex_dynamics()
        input("按回车键继续下一个演示...")
        
        FluidDemo.demo_thermal_convection()
        
        print("所有演示完成！")
        
    except KeyboardInterrupt:
        print("程序被用户中断")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    main()
