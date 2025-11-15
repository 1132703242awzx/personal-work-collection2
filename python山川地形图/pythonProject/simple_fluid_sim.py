"""
简化版流体模拟器 - 专注于性能和可读性
适合学习和实验的基础版本
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

# 配置中文字体
rcParams['font.sans-serif'] = ['Arial']  # 使用Arial避免中文字体问题
rcParams['axes.unicode_minus'] = False

class SimpleFluidSim:
    """简化的流体模拟器"""
    
    def __init__(self, width=64, height=64, dt=0.1):
        """
        初始化模拟器
        
        参数:
        width, height: 网格尺寸
        dt: 时间步长
        """
        self.width = width
        self.height = height
        self.dt = dt
        
        # 物理参数
        self.diffusion = 0.0001   # 扩散率
        self.viscosity = 0.00001  # 粘度
        
        # 创建场数组
        self.reset_fields()
        
        # 数值参数
        self.solver_iterations = 20
    
    def reset_fields(self):
        """重置所有物理场"""
        size = (self.height, self.width)
        
        # 密度场
        self.density = np.zeros(size, dtype=np.float32)
        self.density_prev = np.zeros(size, dtype=np.float32)
        
        # 速度场
        self.vel_x = np.zeros(size, dtype=np.float32)
        self.vel_y = np.zeros(size, dtype=np.float32)
        self.vel_x_prev = np.zeros(size, dtype=np.float32)
        self.vel_y_prev = np.zeros(size, dtype=np.float32)
        
        # 辅助场
        self.pressure = np.zeros(size, dtype=np.float32)
        self.divergence = np.zeros(size, dtype=np.float32)
    
    def add_density(self, x, y, amount):
        """在指定位置添加密度"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.density[y, x] += amount
    
    def add_velocity(self, x, y, vel_x, vel_y):
        """在指定位置添加速度"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.vel_x[y, x] += vel_x
            self.vel_y[y, x] += vel_y
    
    def add_source_circle(self, center_x, center_y, radius, density_amount=0, vel_x=0, vel_y=0):
        """添加圆形源"""
        for y in range(self.height):
            for x in range(self.width):
                dx = x - center_x
                dy = y - center_y
                dist = np.sqrt(dx*dx + dy*dy)
                
                if dist <= radius:
                    # 高斯分布
                    strength = np.exp(-dist*dist / (2 * (radius/3)**2))
                    
                    if density_amount > 0:
                        self.density[y, x] += density_amount * strength
                    
                    if vel_x != 0 or vel_y != 0:
                        self.vel_x[y, x] += vel_x * strength
                        self.vel_y[y, x] += vel_y * strength
    
    def set_boundary(self, field, boundary_type='zero_gradient'):
        """设置边界条件"""
        if boundary_type == 'zero_gradient':
            # 零梯度边界（Neumann边界条件）
            field[0, :] = field[1, :]      # 上边界
            field[-1, :] = field[-2, :]    # 下边界
            field[:, 0] = field[:, 1]      # 左边界
            field[:, -1] = field[:, -2]    # 右边界
        elif boundary_type == 'zero_value':
            # 零值边界（Dirichlet边界条件）
            field[0, :] = 0
            field[-1, :] = 0
            field[:, 0] = 0
            field[:, -1] = 0
    
    def set_velocity_boundary(self):
        """设置速度场边界条件（无滑移）"""
        # 法向速度为零
        self.vel_x[:, 0] = 0
        self.vel_x[:, -1] = 0
        self.vel_y[0, :] = 0
        self.vel_y[-1, :] = 0
        
        # 切向速度反向（无滑移条件）
        self.vel_x[0, :] = -self.vel_x[1, :]
        self.vel_x[-1, :] = -self.vel_x[-2, :]
        self.vel_y[:, 0] = -self.vel_y[:, 1]
        self.vel_y[:, -1] = -self.vel_y[:, -2]
    
    def diffuse_step(self, field, field_prev, diff_rate):
        """扩散步骤"""
        a = self.dt * diff_rate * self.width * self.height
        
        # Gauss-Seidel迭代
        for iteration in range(self.solver_iterations):
            field[1:-1, 1:-1] = (field_prev[1:-1, 1:-1] + a * (
                field[:-2, 1:-1] + field[2:, 1:-1] + 
                field[1:-1, :-2] + field[1:-1, 2:]
            )) / (1 + 4*a)
            
            self.set_boundary(field)
    
    def advect_step(self, field, field_prev, vel_x, vel_y):
        """平流步骤（半拉格朗日方法）"""
        dt0 = self.dt * max(self.width, self.height)
        
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                # 反向追踪
                prev_x = x - dt0 * vel_x[y, x]
                prev_y = y - dt0 * vel_y[y, x]
                
                # 边界限制
                prev_x = max(0.5, min(self.width-1.5, prev_x))
                prev_y = max(0.5, min(self.height-1.5, prev_y))
                
                # 双线性插值
                x0, x1 = int(prev_x), min(int(prev_x)+1, self.width-1)
                y0, y1 = int(prev_y), min(int(prev_y)+1, self.height-1)
                
                sx = prev_x - x0
                sy = prev_y - y0
                
                field[y, x] = (
                    (1-sx) * (1-sy) * field_prev[y0, x0] +
                    sx * (1-sy) * field_prev[y0, x1] +
                    (1-sx) * sy * field_prev[y1, x0] +
                    sx * sy * field_prev[y1, x1]
                )
        
        self.set_boundary(field)
    
    def project_step(self):
        """压力投影步骤（确保无散度）"""
        # 计算速度散度
        h = 1.0 / max(self.width, self.height)
        
        self.divergence[1:-1, 1:-1] = -0.5 * h * (
            self.vel_x[1:-1, 2:] - self.vel_x[1:-1, :-2] +
            self.vel_y[2:, 1:-1] - self.vel_y[:-2, 1:-1]
        )
        
        # 初始化压力
        self.pressure.fill(0)
        self.set_boundary(self.divergence)
        self.set_boundary(self.pressure)
        
        # 求解压力泊松方程
        for iteration in range(self.solver_iterations):
            self.pressure[1:-1, 1:-1] = (
                self.divergence[1:-1, 1:-1] +
                self.pressure[:-2, 1:-1] + self.pressure[2:, 1:-1] +
                self.pressure[1:-1, :-2] + self.pressure[1:-1, 2:]
            ) / 4.0
            
            self.set_boundary(self.pressure)
        
        # 从速度中减去压力梯度
        self.vel_x[1:-1, 1:-1] -= 0.5 * (self.pressure[1:-1, 2:] - self.pressure[1:-1, :-2]) / h
        self.vel_y[1:-1, 1:-1] -= 0.5 * (self.pressure[2:, 1:-1] - self.pressure[:-2, 1:-1]) / h
        
        self.set_velocity_boundary()
    
    def step(self):
        """执行一个完整的模拟步骤"""
        # 1. 速度扩散
        self.vel_x_prev[:] = self.vel_x
        self.vel_y_prev[:] = self.vel_y
        
        self.diffuse_step(self.vel_x, self.vel_x_prev, self.viscosity)
        self.diffuse_step(self.vel_y, self.vel_y_prev, self.viscosity)
        
        # 2. 压力投影
        self.project_step()
        
        # 3. 速度平流
        self.vel_x_prev[:] = self.vel_x
        self.vel_y_prev[:] = self.vel_y
        
        self.advect_step(self.vel_x, self.vel_x_prev, self.vel_x_prev, self.vel_y_prev)
        self.advect_step(self.vel_y, self.vel_y_prev, self.vel_x_prev, self.vel_y_prev)
        
        # 4. 再次压力投影
        self.project_step()
        
        # 5. 密度扩散和平流
        self.density_prev[:] = self.density
        self.diffuse_step(self.density, self.density_prev, self.diffusion)
        
        self.density_prev[:] = self.density
        self.advect_step(self.density, self.density_prev, self.vel_x, self.vel_y)

class FluidVisualizer:
    """流体可视化工具"""
    
    def __init__(self, simulator):
        self.sim = simulator
    
    def plot_current_state(self, save_path=None):
        """绘制当前状态"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 密度场
        im1 = axes[0].imshow(self.sim.density, cmap='hot', origin='lower', interpolation='bilinear')
        axes[0].set_title('Density Field')
        axes[0].set_xlabel('X')
        axes[0].set_ylabel('Y')
        plt.colorbar(im1, ax=axes[0])
        
        # 速度大小
        velocity_magnitude = np.sqrt(self.sim.vel_x**2 + self.sim.vel_y**2)
        im2 = axes[1].imshow(velocity_magnitude, cmap='viridis', origin='lower', interpolation='bilinear')
        axes[1].set_title('Velocity Magnitude')
        axes[1].set_xlabel('X')
        axes[1].set_ylabel('Y')
        plt.colorbar(im2, ax=axes[1])
        
        # 速度矢量场（降采样）
        skip = 4
        x_coords = np.arange(0, self.sim.width, skip)
        y_coords = np.arange(0, self.sim.height, skip)
        X, Y = np.meshgrid(x_coords, y_coords)
        
        vel_x_sub = self.sim.vel_x[::skip, ::skip]
        vel_y_sub = self.sim.vel_y[::skip, ::skip]
        
        axes[2].quiver(X, Y, vel_x_sub, vel_y_sub, scale=20, alpha=0.7)
        axes[2].set_title('Velocity Vectors')
        axes[2].set_xlabel('X')
        axes[2].set_ylabel('Y')
        axes[2].set_aspect('equal')
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = "current_state.png"
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Current state saved to: {save_path}")
        plt.close(fig)
    
    def create_animation(self, num_steps, update_interval=5, save_path=None):
        """创建动画"""
        # 记录数据
        frames = []
        for step in range(num_steps):
            self.sim.step()
            if step % update_interval == 0:
                frames.append({
                    'density': self.sim.density.copy(),
                    'vel_mag': np.sqrt(self.sim.vel_x**2 + self.sim.vel_y**2).copy(),
                    'step': step
                })
                print(f"Progress: {step+1}/{num_steps}")
        
        # 创建动画
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 设置图像
        vmax_density = max(f['density'].max() for f in frames)
        vmax_vel = max(f['vel_mag'].max() for f in frames)
        
        im1 = ax1.imshow(frames[0]['density'], cmap='hot', origin='lower', 
                        vmin=0, vmax=vmax_density, interpolation='bilinear')
        ax1.set_title('Density Field')
        
        im2 = ax2.imshow(frames[0]['vel_mag'], cmap='viridis', origin='lower',
                        vmin=0, vmax=vmax_vel, interpolation='bilinear')
        ax2.set_title('Velocity Magnitude')
        
        # 添加颜色条
        plt.colorbar(im1, ax=ax1)
        plt.colorbar(im2, ax=ax2)
        
        # 步数显示
        step_text = fig.suptitle(f'Step: {frames[0]["step"]}')
        
        def animate(frame_idx):
            frame = frames[frame_idx]
            im1.set_array(frame['density'])
            im2.set_array(frame['vel_mag'])
            step_text.set_text(f'Step: {frame["step"]}')
            return [im1, im2, step_text]
        
        anim = animation.FuncAnimation(fig, animate, frames=len(frames),
                                     interval=100, blit=False, repeat=True)
        
        # 保存动画
        if save_path is None:
            save_path = "fluid_animation.gif"
        
        try:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer='pillow', fps=10)
            print("Animation saved successfully!")
        except Exception as e:
            print(f"Failed to save animation: {e}")
            # 保存最终状态图像
            final_path = "final_state.png"
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(frames[-1]['density'], cmap='hot', origin='lower')
            plt.title('Final Density')
            plt.colorbar()
            plt.subplot(1, 2, 2)
            plt.imshow(frames[-1]['vel_mag'], cmap='viridis', origin='lower')
            plt.title('Final Velocity')
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(final_path, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"Final state saved to: {final_path}")
        
        plt.close(fig)
        return anim

# 演示场景
def demo_ink_drop():
    """墨滴扩散演示"""
    print("Demo: Ink Drop Diffusion")
    
    sim = SimpleFluidSim(width=80, height=80, dt=0.1)
    
    # 在中心添加墨滴
    sim.add_source_circle(40, 40, 8, density_amount=100)
    
    # 创建可视化器
    viz = FluidVisualizer(sim)
    
    # 运行动画
    anim = viz.create_animation(num_steps=200, update_interval=5)
    return anim

def demo_smoke_plume():
    """烟羽演示"""
    print("Demo: Smoke Plume")
    
    sim = SimpleFluidSim(width=80, height=80, dt=0.1)
    
    # 底部添加热源（向上的速度）
    for x in range(35, 45):
        sim.add_velocity(x, 75, 0, -2.0)
        sim.add_density(x, 75, 50)
    
    # 创建可视化器
    viz = FluidVisualizer(sim)
    
    # 持续添加源并模拟
    frames = []
    for step in range(300):
        # 持续添加烟雾源
        if step % 3 == 0:
            for x in range(37, 43):
                sim.add_density(x, 75, 20)
                sim.add_velocity(x, 75, 0, -1.5)
        
        sim.step()
        
        if step % 10 == 0:
            frames.append({
                'density': sim.density.copy(),
                'step': step
            })
            print(f"Progress: {step+1}/300")
    
    # 保存动画
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(frames[0]['density'], cmap='hot', origin='lower', interpolation='bilinear')
    ax.set_title('Smoke Plume Simulation')
    plt.colorbar(im)
    
    step_text = ax.text(0.02, 0.95, f'Step: {frames[0]["step"]}', 
                       transform=ax.transAxes, color='white',
                       bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    def animate(frame_idx):
        frame = frames[frame_idx]
        im.set_array(frame['density'])
        step_text.set_text(f'Step: {frame["step"]}')
        return [im, step_text]
    
    anim = animation.FuncAnimation(fig, animate, frames=len(frames),
                                 interval=100, blit=False, repeat=True)
    
    # 保存动画
    try:
        print("Saving smoke plume animation...")
        anim.save("smoke_plume.gif", writer='pillow', fps=10)
        print("Smoke plume animation saved!")
    except Exception as e:
        print(f"Failed to save animation: {e}")
        # 保存几个关键帧
        key_frames = [0, len(frames)//4, len(frames)//2, 3*len(frames)//4, -1]
        fig, axes = plt.subplots(1, len(key_frames), figsize=(20, 4))
        for i, frame_idx in enumerate(key_frames):
            axes[i].imshow(frames[frame_idx]['density'], cmap='hot', origin='lower')
            axes[i].set_title(f'Step: {frames[frame_idx]["step"]}')
        plt.tight_layout()
        plt.savefig("smoke_plume_sequence.png", dpi=150, bbox_inches='tight')
        print("Smoke plume sequence saved!")
        plt.close()
    
    plt.close(fig)
    return anim

def demo_vortex():
    """涡流演示"""
    print("Demo: Vortex Formation")
    
    sim = SimpleFluidSim(width=80, height=80, dt=0.1)
    
    # 创建旋转的速度场
    center_x, center_y = 40, 40
    for y in range(sim.height):
        for x in range(sim.width):
            dx = x - center_x
            dy = y - center_y
            r = np.sqrt(dx*dx + dy*dy)
            
            if r > 0 and r < 25:
                # 切向速度（产生旋转）
                strength = np.exp(-r*r / (2 * 15**2)) * 3
                angle = np.arctan2(dy, dx)
                sim.vel_x[y, x] = -np.sin(angle) * strength
                sim.vel_y[y, x] = np.cos(angle) * strength
    
    # 添加示踪粒子
    sim.add_source_circle(30, 30, 5, density_amount=80)
    sim.add_source_circle(50, 50, 5, density_amount=80)
    
    viz = FluidVisualizer(sim)
    anim = viz.create_animation(num_steps=250, update_interval=5)
    return anim

def main():
    """主程序"""
    print("=" * 50)
    print("Simple Fluid Simulation Demos")
    print("=" * 50)
    
    try:
        print("Choose a demo:")
        print("1. Ink Drop Diffusion")
        print("2. Smoke Plume")
        print("3. Vortex Formation")
        print("4. Run All Demos")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            demo_ink_drop()
        elif choice == '2':
            demo_smoke_plume()
        elif choice == '3':
            demo_vortex()
        elif choice == '4':
            demo_ink_drop()
            input("Press Enter for next demo...")
            demo_smoke_plume()
            input("Press Enter for next demo...")
            demo_vortex()
        else:
            print("Invalid choice, running ink drop demo...")
            demo_ink_drop()
        
        print("Demo completed!")
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
