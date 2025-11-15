"""
北京3D地形PBR材质系统
Physical Based Rendering Materials for Beijing Terrain

作者: 高级3D材质艺术家
功能: 基于物理渲染的智能材质分配系统
"""

import numpy as np
import pyvista as pv
from typing import Dict, Tuple, Optional
import matplotlib.pyplot as plt
from scipy import ndimage


class TerrainPBRMaterials:
    """
    地形PBR材质系统
    
    基于高程、坡度、坡向等地形参数自动分配真实感材质
    """
    
    def __init__(self):
        """初始化PBR材质库"""
        self.material_library = self._create_material_library()
        self.noise_cache = {}
        
    def _create_material_library(self) -> Dict[str, Dict]:
        """
        创建PBR材质库
        
        每个材质包含颜色、粗糙度、金属度等PBR属性
        """
        return {
            'rock_01': {
                'name': '裸露岩石',
                'base_color': np.array([0.4, 0.35, 0.3]),      # 灰褐色岩石
                'roughness': 0.9,                              # 高粗糙度
                'metallic': 0.0,                               # 非金属
                'normal_strength': 1.2,                        # 强法线贴图
                'height_range': (800, 2000),                   # 适用高程范围
                'slope_range': (25, 90),                       # 适用坡度范围
                'scatter_color': 0.15                          # 颜色散射
            },
            
            'grass_dense': {
                'name': '茂密草甸',
                'base_color': np.array([0.2, 0.5, 0.15]),      # 深绿色
                'roughness': 0.7,                              # 中等粗糙度
                'metallic': 0.0,                               # 非金属
                'normal_strength': 0.8,                        # 中等法线强度
                'height_range': (200, 1200),                   # 适用高程范围
                'slope_range': (0, 30),                        # 适用坡度范围
                'scatter_color': 0.2                           # 颜色散射
            },
            
            'grass_dry': {
                'name': '干燥草地',
                'base_color': np.array([0.6, 0.5, 0.2]),       # 黄褐色
                'roughness': 0.8,                              # 较高粗糙度
                'metallic': 0.0,                               # 非金属
                'normal_strength': 0.6,                        # 较弱法线强度
                'height_range': (50, 800),                     # 适用高程范围
                'slope_range': (0, 35),                        # 适用坡度范围
                'scatter_color': 0.25                          # 颜色散射
            },
            
            'forest_floor': {
                'name': '林地表面',
                'base_color': np.array([0.25, 0.2, 0.1]),      # 深褐色
                'roughness': 0.85,                             # 高粗糙度
                'metallic': 0.0,                               # 非金属
                'normal_strength': 1.0,                        # 标准法线强度
                'height_range': (300, 1000),                   # 适用高程范围
                'slope_range': (5, 40),                        # 适用坡度范围
                'scatter_color': 0.3                           # 颜色散射
            },
            
            'dirt': {
                'name': '泥土',
                'base_color': np.array([0.35, 0.25, 0.15]),    # 土褐色
                'roughness': 0.75,                             # 中高粗糙度
                'metallic': 0.0,                               # 非金属
                'normal_strength': 0.5,                        # 较弱法线强度
                'height_range': (10, 500),                     # 适用高程范围
                'slope_range': (0, 20),                        # 适用坡度范围
                'scatter_color': 0.2                           # 颜色散射
            },
            
            'urban_area': {
                'name': '城市区域',
                'base_color': np.array([0.45, 0.45, 0.5]),     # 灰色
                'roughness': 0.4,                              # 较低粗糙度
                'metallic': 0.1,                               # 轻微金属感
                'normal_strength': 0.3,                        # 弱法线强度
                'height_range': (20, 200),                     # 适用高程范围
                'slope_range': (0, 10),                        # 适用坡度范围
                'scatter_color': 0.1                           # 颜色散射
            }
        }
    
    def generate_perlin_noise(self, shape: Tuple[int, int], scale: float = 100.0, 
                             octaves: int = 4, persistence: float = 0.5, 
                             lacunarity: float = 2.0, seed: int = 42) -> np.ndarray:
        """
        生成Perlin噪声用于材质混合
        
        Args:
            shape: 噪声图尺寸
            scale: 噪声比例
            octaves: 噪声层数
            persistence: 持续性
            lacunarity: 间隙度
            seed: 随机种子
            
        Returns:
            归一化的噪声图 [0, 1]
        """
        cache_key = f"{shape}_{scale}_{octaves}_{persistence}_{lacunarity}_{seed}"
        if cache_key in self.noise_cache:
            return self.noise_cache[cache_key]
        
        np.random.seed(seed)
        noise = np.zeros(shape)
        frequency = 1.0
        amplitude = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            # 简化的噪声生成
            x_coords = np.arange(shape[1]) / scale * frequency
            y_coords = np.arange(shape[0]) / scale * frequency
            X, Y = np.meshgrid(x_coords, y_coords)
            
            # 使用正弦波模拟噪声
            layer_noise = (np.sin(X * 2 * np.pi) * np.cos(Y * 2 * np.pi) + 
                          np.sin(X * 4 * np.pi) * np.cos(Y * 4 * np.pi) * 0.5)
            
            noise += layer_noise * amplitude
            max_value += amplitude
            
            amplitude *= persistence
            frequency *= lacunarity
        
        # 归一化到 [0, 1]
        noise = (noise / max_value + 1) / 2
        noise = np.clip(noise, 0, 1)
        
        self.noise_cache[cache_key] = noise
        return noise
    
    def calculate_material_weights(self, elevation: np.ndarray, slope: np.ndarray, 
                                 aspect: np.ndarray) -> Dict[str, np.ndarray]:
        """
        计算各材质的权重
        
        基于地形参数智能分配材质权重
        """
        print("   🎨 计算智能材质权重...")
        
        shape = elevation.shape
        material_weights = {}
        
        # 生成混合噪声
        noise_large = self.generate_perlin_noise(shape, scale=50.0, seed=42)
        noise_medium = self.generate_perlin_noise(shape, scale=25.0, seed=123)
        noise_small = self.generate_perlin_noise(shape, scale=10.0, seed=456)
        
        # 计算阴坡阳坡
        north_facing = np.cos(np.radians(aspect - 0))    # 北坡（阴坡）
        south_facing = np.cos(np.radians(aspect - 180))  # 南坡（阳坡）
        north_facing = np.clip(north_facing, 0, 1)
        south_facing = np.clip(south_facing, 0, 1)
        
        for material_name, material_props in self.material_library.items():
            # 基础权重
            weight = np.ones(shape) * 0.1
            
            # 高程适应性
            elev_min, elev_max = material_props['height_range']
            elev_factor = np.exp(-((elevation - (elev_min + elev_max) / 2) / (elev_max - elev_min * 0.3))**2)
            
            # 坡度适应性
            slope_min, slope_max = material_props['slope_range']
            slope_factor = np.where(
                (slope >= slope_min) & (slope <= slope_max),
                1.0 - abs(slope - (slope_min + slope_max) / 2) / (slope_max - slope_min),
                0.1
            )
            
            # 特殊规则
            if material_name == 'rock_01':
                # 岩石：高海拔 + 陡坡
                weight = elev_factor * slope_factor * (1 + noise_large * 0.3)
                weight *= (elevation > 600) * (slope > 20)
                
            elif material_name == 'grass_dense':
                # 茂密草甸：中海拔 + 北坡（湿润）
                weight = elev_factor * slope_factor * north_facing
                weight *= (1 + noise_medium * 0.4)
                weight *= (elevation > 300) * (elevation < 1000)
                
            elif material_name == 'grass_dry':
                # 干燥草地：低中海拔 + 南坡（干燥）
                weight = elev_factor * slope_factor * south_facing
                weight *= (1 + noise_large * 0.3)
                weight *= (elevation < 800)
                
            elif material_name == 'forest_floor':
                # 林地：中海拔 + 北坡 + 中等坡度
                weight = elev_factor * slope_factor * north_facing
                weight *= (1 + noise_small * 0.5)
                weight *= (elevation > 400) * (elevation < 900) * (slope > 10) * (slope < 35)
                
            elif material_name == 'dirt':
                # 泥土：低海拔 + 平缓地区
                weight = elev_factor * slope_factor
                weight *= (1 + noise_medium * 0.2)
                weight *= (elevation < 400) * (slope < 15)
                
            elif material_name == 'urban_area':
                # 城市：极低海拔 + 平地
                weight = elev_factor * slope_factor
                weight *= (elevation < 150) * (slope < 5)
            
            # 应用噪声进行自然混合
            weight *= (0.7 + noise_large * 0.3)
            weight = np.clip(weight, 0, 1)
            
            material_weights[material_name] = weight
        
        # 权重归一化
        total_weight = sum(material_weights.values())
        for material_name in material_weights:
            material_weights[material_name] /= (total_weight + 1e-8)
        
        print(f"      ✅ 材质权重计算完成，共{len(material_weights)}种材质")
        return material_weights
    
    def blend_materials(self, material_weights: Dict[str, np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        混合材质生成最终颜色、粗糙度和金属度贴图
        
        Returns:
            (color_map, roughness_map, metallic_map)
        """
        print("   🎨 混合PBR材质...")
        
        shape = list(material_weights.values())[0].shape
        
        # 初始化贴图
        color_map = np.zeros((*shape, 3))
        roughness_map = np.zeros(shape)
        metallic_map = np.zeros(shape)
        
        # 加权混合
        for material_name, weight in material_weights.items():
            material = self.material_library[material_name]
            
            # 颜色混合
            base_color = material['base_color']
            scatter = material['scatter_color']
            
            # 添加颜色变化
            color_variation = np.random.normal(0, scatter, (*shape, 3))
            material_color = base_color + color_variation
            material_color = np.clip(material_color, 0, 1)
            
            # 权重混合
            weight_3d = np.stack([weight, weight, weight], axis=2)
            color_map += material_color * weight_3d
            
            # 物理属性混合
            roughness_map += material['roughness'] * weight
            metallic_map += material['metallic'] * weight
        
        # 确保值在合理范围内
        color_map = np.clip(color_map, 0, 1)
        roughness_map = np.clip(roughness_map, 0, 1)
        metallic_map = np.clip(metallic_map, 0, 1)
        
        print("      ✅ PBR材质混合完成")
        return color_map, roughness_map, metallic_map
    
    def apply_pbr_materials(self, grid: pv.StructuredGrid) -> pv.StructuredGrid:
        """
        将PBR材质应用到网格
        """
        print("   🎨 应用PBR材质到3D网格...")
        
        # 获取地形数据
        elevation = grid["elevation"].reshape(grid.dimensions[:2][::-1])
        slope = grid["slope"].reshape(grid.dimensions[:2][::-1])
        aspect = grid["aspect"].reshape(grid.dimensions[:2][::-1])
        
        # 计算材质权重
        material_weights = self.calculate_material_weights(elevation, slope, aspect)
        
        # 混合材质
        color_map, roughness_map, metallic_map = self.blend_materials(material_weights)
        
        # 添加到网格
        grid["pbr_color_r"] = color_map[:, :, 0].flatten()
        grid["pbr_color_g"] = color_map[:, :, 1].flatten()
        grid["pbr_color_b"] = color_map[:, :, 2].flatten()
        grid["pbr_roughness"] = roughness_map.flatten()
        grid["pbr_metallic"] = metallic_map.flatten()
        
        # 创建组合的RGB颜色
        rgb_colors = np.column_stack([
            grid["pbr_color_r"],
            grid["pbr_color_g"], 
            grid["pbr_color_b"]
        ]) * 255
        grid["pbr_colors"] = rgb_colors.astype(np.uint8)
        
        print("      ✅ PBR材质应用完成")
        return grid
    
    def create_material_preview(self, material_weights: Dict[str, np.ndarray], 
                              save_path: str = None) -> None:
        """
        创建材质分布预览图
        """
        print("   📊 生成材质分布预览...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Beijing Terrain PBR Materials Distribution\n北京地形PBR材质分布', fontsize=16)
        
        materials = list(self.material_library.keys())
        
        for i, material_name in enumerate(materials):
            row, col = i // 3, i % 3
            ax = axes[row, col]
            
            weight = material_weights[material_name]
            material = self.material_library[material_name]
            
            im = ax.imshow(weight, cmap='viridis', aspect='equal')
            ax.set_title(f"{material['name']}\n({material_name})", fontsize=12)
            ax.axis('off')
            
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"      💾 材质预览保存至: {save_path}")
        
        plt.show()
        print("      ✅ 材质分布预览完成")


def create_smart_camera_view(grid: pv.StructuredGrid) -> Tuple[list, list]:
    """
    创建智能相机视角，确保地形在视图中央
    
    Args:
        grid: PyVista网格对象
        
    Returns:
        (camera_position, focal_point)
    """
    bounds = grid.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]
    
    # 计算几何中心
    center_x = (bounds[0] + bounds[1]) / 2
    center_y = (bounds[2] + bounds[3]) / 2
    center_z = (bounds[4] + bounds[5]) / 2
    
    # 计算地形尺寸
    width = bounds[1] - bounds[0]
    height = bounds[3] - bounds[2]
    depth = bounds[5] - bounds[4]
    
    # 计算合适的相机距离
    max_dimension = max(width, height, depth)
    camera_distance = max_dimension * 1.5
    
    # 设置相机位置（从西南方向俯视）
    camera_position = [
        center_x - camera_distance * 0.7,
        center_y - camera_distance * 0.7,
        center_z + camera_distance * 0.8
    ]
    
    focal_point = [center_x, center_y, center_z]
    
    return camera_position, focal_point
