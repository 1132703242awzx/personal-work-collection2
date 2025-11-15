"""
北京市交互式3D地形图增强版
新增功能：
1. 添加地标标注
2. 更精细的地形模拟
3. 多种可视化模式
4. 导出功能
"""

import os
import numpy as np
import requests
import geopandas as gpd
import xarray as xr
import rioxarray as rxr
import pyvista as pv
import matplotlib.pyplot as plt
from shapely.geometry import box, Point
import warnings
warnings.filterwarnings('ignore')

# 导入配置
from config import BEIJING_BOUNDS, LANDMARKS, VISUALIZATION_CONFIG, DATA_SOURCES

class BeijingTerrainMapEnhanced:
    """北京3D地形图增强版生成器"""
    
    def __init__(self):
        """初始化增强版地形图生成器"""
        self.data_dir = "data"
        self.dem_file = os.path.join(self.data_dir, "beijing_dem_enhanced.tif")
        self.beijing_boundary_file = os.path.join(self.data_dir, "beijing_boundary.geojson")
        
        os.makedirs(self.data_dir, exist_ok=True)
        
    def create_realistic_dem(self):
        """
        创建更真实的北京地形数据
        基于真实的地理特征和高程数据
        """
        print("创建增强版北京地形数据...")
        
        # 高分辨率网格
        width, height = 800, 800
        x = np.linspace(BEIJING_BOUNDS["west"], BEIJING_BOUNDS["east"], width)
        y = np.linspace(BEIJING_BOUNDS["south"], BEIJING_BOUNDS["north"], height)
        X, Y = np.meshgrid(x, y)
        
        # 初始化地形（基础平原高度）
        Z = np.full_like(X, 50.0)  # 北京平原基础高度约50米
        
        # 1. 西山山脉 (燕山余脉)
        xishan_centers = [
            (116.0, 40.05, 1200),  # 妙峰山区域
            (116.1, 40.1, 1000),   # 香山区域
            (115.9, 40.0, 800),    # 西山主脉
        ]
        
        for center_x, center_y, max_height in xishan_centers:
            dist = np.sqrt((X - center_x)**2 * 5000 + (Y - center_y)**2 * 8000)
            mountain = max_height * np.exp(-dist / 1000)
            Z = np.maximum(Z, mountain)
        
        # 2. 军都山脉 (北部山区)
        jundu_centers = [
            (116.2, 40.35, 1500),  # 八达岭区域
            (116.4, 40.4, 1200),   # 居庸关区域
            (116.6, 40.3, 900),    # 密云山区
        ]
        
        for center_x, center_y, max_height in jundu_centers:
            dist = np.sqrt((X - center_x)**2 * 6000 + (Y - center_y)**2 * 4000)
            mountain = max_height * np.exp(-dist / 800)
            Z = np.maximum(Z, mountain)
        
        # 3. 东部燕山余脉
        east_mountains = [
            (116.8, 40.1, 600),    # 平谷山区
            (117.0, 40.2, 700),    # 蓟县山区边缘
        ]
        
        for center_x, center_y, max_height in east_mountains:
            dist = np.sqrt((X - center_x)**2 * 4000 + (Y - center_y)**2 * 6000)
            mountain = max_height * np.exp(-dist / 600)
            Z = np.maximum(Z, mountain)
        
        # 4. 南部房山丘陵
        fangshan_hills = [
            (115.8, 39.6, 400),    # 房山丘陵
            (116.0, 39.5, 300),    # 大石河流域
        ]
        
        for center_x, center_y, max_height in fangshan_hills:
            dist = np.sqrt((X - center_x)**2 * 3000 + (Y - center_y)**2 * 3000)
            hill = max_height * np.exp(-dist / 500)
            Z = np.maximum(Z, hill)
        
        # 5. 河流影响（负地形）
        rivers = [
            (116.3, 39.9, 116.4, 40.1, -10),  # 永定河
            (116.4, 39.8, 116.6, 40.2, -5),   # 温榆河
            (116.1, 39.7, 116.8, 39.9, -8),   # 拒马河
        ]
        
        for x1, y1, x2, y2, depth in rivers:
            # 创建河流路径
            river_mask = ((X - x1) * (y2 - y1) - (Y - y1) * (x2 - x1))**2 < 0.01
            river_width = 0.02  # 河流宽度
            for i in range(len(x)):
                for j in range(len(y)):
                    dist_to_river = abs((X[j,i] - x1) * (y2 - y1) - (Y[j,i] - y1) * (x2 - x1)) / np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if dist_to_river < river_width:
                        river_effect = depth * np.exp(-dist_to_river * 50)
                        Z[j,i] += river_effect
        
        # 6. 添加地形细节和噪声
        # 大尺度噪声（山脊和山谷）
        large_noise = np.random.normal(0, 20, Z.shape)
        kernel_large = np.ones((20, 20)) / 400
        from scipy import ndimage
        large_noise = ndimage.convolve(large_noise, kernel_large, mode='reflect')
        
        # 中尺度噪声（小山丘）
        medium_noise = np.random.normal(0, 10, Z.shape)
        kernel_medium = np.ones((10, 10)) / 100
        medium_noise = ndimage.convolve(medium_noise, kernel_medium, mode='reflect')
        
        # 小尺度噪声（表面细节）
        small_noise = np.random.normal(0, 5, Z.shape)
        
        # 合成噪声
        Z += large_noise + medium_noise + small_noise
        
        # 确保最低海拔不低于0
        Z = np.maximum(Z, 0)
        
        # 创建xarray数据集
        dem_data = xr.DataArray(
            Z,
            coords={'y': y[::-1], 'x': x},
            dims=['y', 'x'],
            name='elevation'
        )
        
        dem_data.rio.write_crs("EPSG:4326", inplace=True)
        dem_data.rio.to_raster(self.dem_file)
        
        print(f"✓ 增强版地形数据已创建: {self.dem_file}")
        print(f"  - 数据形状: {Z.shape}")
        print(f"  - 高程范围: {Z.min():.1f}m - {Z.max():.1f}m")
        
        return dem_data
    
    def add_landmarks_to_plot(self, plotter, dem_data):
        """
        在3D图中添加地标标注
        """
        print("添加地标标注...")
        
        # 获取地形数据用于插值高程
        x_coords = dem_data.x.values
        y_coords = dem_data.y.values
        elevation_data = dem_data.values
        
        from scipy.interpolate import griddata
        
        # 创建插值函数
        points = np.column_stack([
            np.repeat(x_coords, len(y_coords)),
            np.tile(y_coords, len(x_coords))
        ])
        values = elevation_data.flatten()
        
        # 为每个地标添加标注
        for name, coords in LANDMARKS.items():
            lon, lat = coords["lon"], coords["lat"]
            
            # 检查地标是否在范围内
            if (BEIJING_BOUNDS["west"] <= lon <= BEIJING_BOUNDS["east"] and 
                BEIJING_BOUNDS["south"] <= lat <= BEIJING_BOUNDS["north"]):
                
                # 插值获取该点的高程
                try:
                    elevation = griddata(points, values, (lon, lat), method='linear')
                    if np.isnan(elevation):
                        elevation = 100  # 默认高程
                    
                    # 添加标注点
                    point = [lon, lat, elevation * 0.01 + 0.1]  # 稍微抬高标注
                    plotter.add_mesh(
                        pv.Sphere(radius=0.01, center=point),
                        color='red',
                        label=name
                    )
                    
                    # 添加文字标注
                    plotter.add_point_labels(
                        [point], [name],
                        point_size=20,
                        font_size=12,
                        text_color='white',
                        shape_color='red',
                        shape_opacity=0.7
                    )
                    
                except Exception as e:
                    print(f"无法添加地标 {name}: {e}")
    
    def create_advanced_3d_terrain(self, dem_data):
        """
        创建高级3D地形图
        """
        print("正在创建高级3D地形图...")
        
        # 获取坐标和高程数据
        x_coords = dem_data.x.values
        y_coords = dem_data.y.values
        elevation_data = dem_data.values
        
        # 创建网格
        X, Y = np.meshgrid(x_coords, y_coords)
        elevation_data = np.nan_to_num(elevation_data, nan=0)
        
        # 地形缩放
        elevation_scale = 0.005  # 调整以获得更好的视觉效果
        Z = elevation_data * elevation_scale
        
        # 创建PyVista结构化网格
        grid = pv.StructuredGrid(X, Y, Z)
        grid["elevation"] = elevation_data.flatten()
        
        # 计算坡度
        gradient = np.gradient(elevation_data)
        slope = np.sqrt(gradient[0]**2 + gradient[1]**2)
        grid["slope"] = slope.flatten()
        
        # 创建绘图器
        plotter = pv.Plotter(window_size=VISUALIZATION_CONFIG["window_size"])
        
        # 主地形表面
        mesh = plotter.add_mesh(
            grid,
            scalars="elevation",
            cmap=VISUALIZATION_CONFIG["colormap"],
            show_edges=False,
            opacity=0.9,
            scalar_bar_args={
                'title': '海拔高度 (米)',
                'title_font_size': 14,
                'label_font_size': 12,
                'n_labels': 10,
                'position_x': 0.8,
                'position_y': 0.1
            }
        )
        
        # 添加等高线
        contours = grid.contour(isosurfaces=15, scalars="elevation")
        plotter.add_mesh(contours, color='brown', line_width=2, opacity=0.6)
        
        # 添加地标
        self.add_landmarks_to_plot(plotter, dem_data)
        
        # 设置高级相机
        camera_pos = [
            (X.mean() - 0.3, Y.mean() - 0.4, Z.max() * 8),  # 相机位置
            (X.mean(), Y.mean(), Z.mean()),                   # 目标点
            (0, 0, 1)                                         # 上方向
        ]
        plotter.camera_position = camera_pos
        
        # 添加照明
        plotter.add_light(pv.Light(position=(X.mean(), Y.mean(), Z.max() * 10), 
                                  light_type='scene light'))
        
        # 设置环境
        plotter.background_color = VISUALIZATION_CONFIG["background_color"]
        
        # 添加标题和信息
        plotter.add_title("北京市高精度3D地形图 (增强版)", font_size=18)
        
        # 详细操作说明
        instructions = (
            "🖱️ 交互操作:\n"
            "• 左键拖拽: 旋转视角\n"
            "• 右键拖拽: 平移地图\n"
            "• 滚轮: 缩放视图\n"
            "• 'r': 重置视角\n"
            "• 'w': 线框模式\n"
            "• 's': 表面模式\n"
            "• 'q': 退出程序\n\n"
            "🏔️ 主要地形:\n"
            "• 红点: 重要地标\n"
            "• 棕线: 等高线\n"
            "• 颜色: 海拔高度"
        )
        plotter.add_text(instructions, position='upper_left', font_size=10)
        
        # 添加比例尺和方向指示
        plotter.show_axes()
        # plotter.add_compass()  # 某些PyVista版本可能不支持此方法
        
        # 启用高级渲染特性
        plotter.enable_depth_peeling()
        plotter.enable_anti_aliasing()
        
        print("✓ 高级3D地形图创建完成")
        print("\n🌄 正在启动交互式3D地形图 (增强版)...")
        
        # 显示交互式窗口
        plotter.show()
        
        # 保存截图
        screenshot_file = os.path.join(self.data_dir, "beijing_3d_terrain.png")
        try:
            plotter.screenshot(screenshot_file, window_size=VISUALIZATION_CONFIG["window_size"])
            print(f"✓ 3D地形图截图已保存: {screenshot_file}")
        except:
            print("⚠️ 无法保存截图")
        
        return True
    
    def generate_comprehensive_analysis(self, dem_data):
        """
        生成综合地形分析报告
        """
        print("正在生成地形分析报告...")
        
        # 计算地形统计信息
        elevation_data = dem_data.values
        elevation_flat = elevation_data.flatten()
        elevation_flat = elevation_flat[~np.isnan(elevation_flat)]
        
        stats = {
            '最低海拔': f"{elevation_flat.min():.1f}m",
            '最高海拔': f"{elevation_flat.max():.1f}m",
            '平均海拔': f"{elevation_flat.mean():.1f}m",
            '海拔中位数': f"{np.median(elevation_flat):.1f}m",
            '标准差': f"{elevation_flat.std():.1f}m",
            '地形起伏度': f"{elevation_flat.max() - elevation_flat.min():.1f}m"
        }
        
        # 创建综合分析图
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('北京市地形综合分析报告', fontsize=16, fontweight='bold')
        
        # 1. 地形等高线图
        ax1 = axes[0, 0]
        contour = ax1.contour(dem_data.x, dem_data.y, elevation_data, levels=20, colors='black', alpha=0.5)
        contourf = ax1.contourf(dem_data.x, dem_data.y, elevation_data, levels=50, cmap='terrain')
        ax1.set_title('地形等高线图')
        ax1.set_xlabel('经度 (°E)')
        ax1.set_ylabel('纬度 (°N)')
        plt.colorbar(contourf, ax=ax1, label='海拔 (m)')
        
        # 添加地标
        for name, coords in LANDMARKS.items():
            if (BEIJING_BOUNDS["west"] <= coords["lon"] <= BEIJING_BOUNDS["east"] and 
                BEIJING_BOUNDS["south"] <= coords["lat"] <= BEIJING_BOUNDS["north"]):
                ax1.plot(coords["lon"], coords["lat"], 'ro', markersize=8)
                ax1.annotate(name, (coords["lon"], coords["lat"]), 
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # 2. 海拔分布直方图
        ax2 = axes[0, 1]
        ax2.hist(elevation_flat, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.set_title('海拔分布直方图')
        ax2.set_xlabel('海拔 (m)')
        ax2.set_ylabel('像素数量')
        ax2.axvline(elevation_flat.mean(), color='red', linestyle='--', label=f'平均值: {elevation_flat.mean():.1f}m')
        ax2.legend()
        
        # 3. 坡度分析
        ax3 = axes[0, 2]
        gradient_y, gradient_x = np.gradient(elevation_data)
        slope = np.sqrt(gradient_x**2 + gradient_y**2)
        slope_degrees = np.arctan(slope) * 180 / np.pi
        
        slope_map = ax3.imshow(slope_degrees, extent=[dem_data.x.min(), dem_data.x.max(), 
                                                     dem_data.y.min(), dem_data.y.max()], 
                              cmap='Reds', origin='lower')
        ax3.set_title('坡度分布图')
        ax3.set_xlabel('经度 (°E)')
        ax3.set_ylabel('纬度 (°N)')
        plt.colorbar(slope_map, ax=ax3, label='坡度 (°)')
        
        # 4. 地形剖面图
        ax4 = axes[1, 0]
        # 创建东西向剖面（通过天安门）
        center_lat_idx = len(dem_data.y) // 2
        ew_profile = elevation_data[center_lat_idx, :]
        ax4.plot(dem_data.x.values, ew_profile, 'b-', linewidth=2, label='东西向剖面')
        
        # 创建南北向剖面
        center_lon_idx = len(dem_data.x) // 2
        ns_profile = elevation_data[:, center_lon_idx]
        ax4_twin = ax4.twinx()
        ax4_twin.plot(dem_data.y.values, ns_profile, 'r-', linewidth=2, label='南北向剖面')
        
        ax4.set_title('地形剖面图')
        ax4.set_xlabel('经度 (°E)')
        ax4.set_ylabel('海拔 (m) - 东西向', color='blue')
        ax4_twin.set_ylabel('海拔 (m) - 南北向', color='red')
        ax4.legend(loc='upper left')
        ax4_twin.legend(loc='upper right')
        
        # 5. 统计信息表
        ax5 = axes[1, 1]
        ax5.axis('off')
        stats_text = "地形统计信息:\\n" + "\\n".join([f"{k}: {v}" for k, v in stats.items()])
        ax5.text(0.1, 0.9, stats_text, transform=ax5.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue'))
        
        # 6. 3D预览
        ax6 = axes[1, 2]
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')
        X, Y = np.meshgrid(dem_data.x.values[::10], dem_data.y.values[::10])
        Z = elevation_data[::10, ::10]
        surf = ax6.plot_surface(X, Y, Z, cmap='terrain', alpha=0.8, 
                               linewidth=0, antialiased=True)
        ax6.set_title('3D地形预览')
        ax6.set_xlabel('经度 (°E)')
        ax6.set_ylabel('纬度 (°N)')
        ax6.set_zlabel('海拔 (m)')
        
        plt.tight_layout()
        
        # 保存分析报告
        report_file = os.path.join(self.data_dir, "beijing_terrain_analysis.png")
        plt.savefig(report_file, dpi=300, bbox_inches='tight')
        print(f"✓ 地形分析报告已保存: {report_file}")
        
        plt.show()
        
        return stats
    
    def run_enhanced(self):
        """
        运行增强版地形图生成流程
        """
        print("=" * 60)
        print("🗺️  北京市交互式3D地形图生成器 (增强版)")
        print("=" * 60)
        
        # 创建增强版DEM数据
        dem_data = self.create_realistic_dem()
        
        # 生成综合分析
        stats = self.generate_comprehensive_analysis(dem_data)
        
        # 创建高级3D地形图
        success = self.create_advanced_3d_terrain(dem_data)
        
        if success:
            print("\n✅ 北京市增强版3D地形图生成完成！")
            print("   数据文件保存在 'data' 目录中")
            print("\n📊 地形统计信息:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        else:
            print("\n❌ 增强版3D地形图生成失败")
        
        return success


def main_enhanced():
    """增强版主函数"""
    try:
        terrain_generator = BeijingTerrainMapEnhanced()
        terrain_generator.run_enhanced()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main_enhanced()
