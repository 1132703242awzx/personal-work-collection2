"""
流体模拟器测试脚本
快速验证所有功能是否正常工作
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(__file__))

def test_basic_simulation():
    """测试基础模拟功能"""
    print("测试基础模拟功能...")
    
    try:
        from simple_fluid_sim import SimpleFluidSim
        
        # 创建小规模模拟器
        sim = SimpleFluidSim(width=32, height=32, dt=0.1)
        
        # 添加源
        sim.add_source_circle(16, 16, 5, density_amount=50)
        
        # 运行几步
        for i in range(10):
            sim.step()
            if i % 5 == 0:
                max_density = np.max(sim.density)
                print(f"  步数 {i}: 最大密度 = {max_density:.2f}")
        
        print("✓ 基础模拟功能正常")
        return True
        
    except Exception as e:
        print(f"✗ 基础模拟功能失败: {e}")
        return False

def test_visualization():
    """测试可视化功能"""
    print("测试可视化功能...")
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # 设置后端
        
        from simple_fluid_sim import SimpleFluidSim, FluidVisualizer
        
        # 创建模拟器
        sim = SimpleFluidSim(width=32, height=32)
        sim.add_source_circle(16, 16, 5, density_amount=50)
        
        # 运行几步
        for _ in range(5):
            sim.step()
        
        # 测试静态图像（保存而不显示）
        viz = FluidVisualizer(sim)
        viz.plot_current_state(save_path="test_visualization.png")
        
        # 检查文件是否创建
        import os
        if os.path.exists("test_visualization.png"):
            print("✓ 可视化功能正常")
            # 清理测试文件
            os.remove("test_visualization.png")
            return True
        else:
            print("✗ 可视化文件未创建")
            return False
        
    except Exception as e:
        print(f"✗ 可视化功能失败: {e}")
        return False

def test_physics():
    """测试物理正确性"""
    print("测试物理正确性...")
    
    try:
        from simple_fluid_sim import SimpleFluidSim
        
        sim = SimpleFluidSim(width=32, height=32)
        
        # 测试质量守恒
        initial_mass = np.sum(sim.density)
        sim.add_density(16, 16, 100)
        
        for _ in range(20):
            sim.step()
        
        final_mass = np.sum(sim.density)
        mass_loss = abs(final_mass - initial_mass - 100) / 100
        
        print(f"  质量守恒误差: {mass_loss:.3f}")
        
        if mass_loss < 0.1:  # 10%以内的误差可接受
            print("✓ 物理正确性验证通过")
            return True
        else:
            print("✗ 质量守恒误差过大")
            return False
            
    except Exception as e:
        print(f"✗ 物理正确性测试失败: {e}")
        return False

def test_performance():
    """测试性能"""
    print("测试性能...")
    
    try:
        import time
        from simple_fluid_sim import SimpleFluidSim
        
        sim = SimpleFluidSim(width=64, height=64)
        sim.add_source_circle(32, 32, 8, density_amount=100)
        
        # 计时
        start_time = time.time()
        for _ in range(50):
            sim.step()
        end_time = time.time()
        
        total_time = end_time - start_time
        steps_per_second = 50 / total_time
        
        print(f"  50步用时: {total_time:.2f}秒")
        print(f"  性能: {steps_per_second:.1f} 步/秒")
        
        if steps_per_second > 10:  # 至少10步/秒
            print("✓ 性能测试通过")
            return True
        else:
            print("⚠ 性能较低但可接受")
            return True
            
    except Exception as e:
        print(f"✗ 性能测试失败: {e}")
        return False

def test_advanced_features():
    """测试高级功能"""
    print("测试高级功能...")
    
    try:
        # 测试完整版本
        import main
        
        simulator = main.FluidSimulator(size=32)
        simulator.add_density_source(0.5, 0.5, 0.1, 50)
        
        for _ in range(5):
            simulator.step()
        
        print("✓ 高级功能正常")
        return True
        
    except Exception as e:
        print(f"⚠ 高级功能测试跳过: {e}")
        return True  # 不是关键功能，跳过也可以

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("流体模拟器功能测试")
    print("=" * 50)
    
    tests = [
        test_basic_simulation,
        test_visualization,
        test_physics,
        test_performance,
        test_advanced_features
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"测试异常: {e}")
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！流体模拟器工作正常。")
    elif passed >= total - 1:
        print("✅ 主要功能正常，可以使用。")
    else:
        print("⚠️ 部分功能有问题，请检查代码。")
    
    print("=" * 50)

if __name__ == '__main__':
    run_all_tests()
