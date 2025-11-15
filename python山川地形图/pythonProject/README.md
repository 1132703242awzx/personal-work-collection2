# 流体力学模拟器使用指南

## 项目概述

本项目实现了一个基于Navier-Stokes方程的二维流体力学模拟器，包含三个不同复杂度的版本：

1. **main.py** - 完整功能版本，包含详细注释和高级功能
2. **simple_fluid_sim.py** - 简化版本，专注于性能和易理解性
3. **fluid_sim_enhanced.py** - 增强版本，包含热对流、涡度分析等高级特性

## 物理原理

### Navier-Stokes方程
流体模拟基于不可压缩流体的Navier-Stokes方程：

```
∂u/∂t + (u·∇)u = -∇p/ρ + ν∇²u + f
∇·u = 0
```

其中：
- u: 速度场
- p: 压力
- ρ: 密度
- ν: 动力学粘度
- f: 外力

### 数值求解方法

1. **扩散步骤** - 使用隐式方法求解扩散方程
2. **平流步骤** - 使用半拉格朗日方法处理对流项
3. **压力投影** - 使用Helmholtz-Hodge分解确保速度场无散度

## 文件说明

### main.py - 完整版本
**特性：**
- 完整的Navier-Stokes求解器
- 密度场和速度场模拟
- 静态和动态可视化
- 详细的物理注释

**使用方法：**
```python
python main.py
```

**核心类和方法：**
- `FluidSimulator`: 主模拟器类
- `FluidVisualizer`: 可视化工具
- `add_density_source()`: 添加密度源
- `add_velocity_source()`: 添加速度源
- `step()`: 执行一个时间步
- `simulate()`: 运行完整模拟

### simple_fluid_sim.py - 简化版本
**特性：**
- 优化的性能
- 简洁的代码结构
- 多种演示场景
- 交互式选择

**使用方法：**
```python
python simple_fluid_sim.py
```

**演示场景：**
1. 墨滴扩散 - 演示基本的扩散过程
2. 烟羽 - 模拟向上流动的烟雾
3. 涡流 - 展示旋转流体动力学

### fluid_sim_enhanced.py - 增强版本
**特性：**
- 热对流模拟
- 涡度场分析
- 多物理场耦合
- 高精度数值方法

**使用方法：**
```python
python fluid_sim_enhanced.py
```

## 参数说明

### 模拟参数
- `size`: 网格大小 (推荐: 64-128)
- `dt`: 时间步长 (推荐: 0.1)
- `diffusion`: 扩散率 (推荐: 0.0001-0.001)
- `viscosity`: 粘度 (推荐: 0.00001-0.0001)

### 性能优化建议
1. **网格大小**: 较小的网格(64x64)运行更快
2. **时间步长**: 较大的dt可能导致不稳定
3. **迭代次数**: 增加求解器迭代次数提高精度但降低速度

## 自定义场景

### 添加密度源
```python
# 在模拟器中添加圆形密度源
simulator.add_density_source(x=0.5, y=0.5, radius=0.1, intensity=100.0)
```

### 添加速度源
```python
# 创建涡流
simulator.add_velocity_source(x=0.3, y=0.3, radius=0.15, vx=2.0, vy=1.0)
```

### 创建障碍物
```python
# 在增强版本中添加圆形障碍物
simulator.add_circular_obstacle(x=0.5, y=0.5, radius=0.1)
```

## 可视化选项

### 静态图像
- 密度场热图
- 速度矢量场
- 流线图

### 动画
- 密度场演化
- 速度场变化
- 涡度分析（增强版）

## 常见问题

### Q: 模拟不稳定怎么办？
A: 减小时间步长dt或增加粘度viscosity

### Q: 如何提高模拟精度？
A: 增加网格分辨率或求解器迭代次数

### Q: 动画太慢怎么办？
A: 减小网格大小或增加保存间隔

### Q: 中文字体显示问题？
A: 程序会自动处理字体问题，使用英文标签避免显示错误

## 物理现象解释

### 扩散
分子热运动导致的物质传播，遵循Fick定律：
```
∂c/∂t = D∇²c
```

### 平流
流体运动导致的物质输运：
```
∂c/∂t + u·∇c = 0
```

### 压力投影
确保流体不可压缩性(∇·u = 0)的数学技术，通过求解泊松方程计算压力梯度。

## 扩展建议

1. **添加边界条件**: 实现不同类型的壁面条件
2. **多相流**: 模拟油水混合等多相系统
3. **温度场**: 包含热传导和对流换热
4. **湍流模型**: 实现LES或RANS湍流模型
5. **GPU加速**: 使用CUDA或OpenCL加速计算

## 参考资料

1. Jos Stam, "Real-Time Fluid Dynamics for Games" (GDC 2003)
2. Bridson, Robert. "Fluid simulation for computer graphics." (2015)
3. Chorin, A. J. "Numerical solution of the Navier-Stokes equations." (1968)

## 许可证

此项目仅供学习和研究使用。

---

**作者**: 用户  
**日期**: 2025年8月29日  
**版本**: 1.0
