"""
人文细节融入系统
Cultural and Human Details Integration System

功能:
1. 历史遗迹建模 (长城)
2. 路径网络生成
3. 人类活动痕迹
4. 建筑与基础设施
"""

import numpy as np
import pyvista as pv
from typing import Dict, List, Tuple, Optional
import requests
import json
from pathlib import Path


class CulturalHeritageSysstem:
    """
    文化遗产系统
    
    集成长城、古建筑等人文地标
    """
    
    def __init__(self):
        """初始化文化遗产系统"""
        self.great_wall_segments = self._define_great_wall_segments()
        self.ancient_sites = self._define_ancient_sites()
        
    def _define_great_wall_segments(self) -> List[Dict]:
        """
        定义北京地区的长城段落
        """
        return [
            {
                'name': '慕田峪长城',
                'coordinates': [
                    [116.5699, 40.4319],  # 起点
                    [116.5756, 40.4331],
                    [116.5834, 40.4356],
                    [116.5912, 40.4389],
                    [116.5987, 40.4425],  # 终点
                ],
                'elevation_offset': 20.0,  # 相对地面高度
                'wall_height': 8.0,
                'wall_width': 6.0,
                'condition': 'restored'  # 修复状态
            },
            {
                'name': '箭扣长城',
                'coordinates': [
                    [116.4523, 40.4712],
                    [116.4598, 40.4745],
                    [116.4687, 40.4823],
                    [116.4756, 40.4891],
                    [116.4834, 40.4967],
                ],
                'elevation_offset': 15.0,
                'wall_height': 6.0,
                'wall_width': 4.0,
                'condition': 'ruins'  # 废墟状态
            },
            {
                'name': '居庸关长城',
                'coordinates': [
                    [116.0934, 40.2987],
                    [116.0987, 40.3023],
                    [116.1043, 40.3067],
                    [116.1098, 40.3112],
                ],
                'elevation_offset': 25.0,
                'wall_height': 10.0,
                'wall_width': 8.0,
                'condition': 'restored'
            },
            {
                'name': '八达岭长城',
                'coordinates': [
                    [116.0134, 40.3598],
                    [116.0189, 40.3634],
                    [116.0245, 40.3678],
                    [116.0312, 40.3723],
                    [116.0387, 40.3789],
                ],
                'elevation_offset': 30.0,
                'wall_height': 12.0,
                'wall_width': 10.0,
                'condition': 'restored'
            }
        ]
    
    def _define_ancient_sites(self) -> List[Dict]:
        """
        定义古代遗址和建筑
        """
        return [
            {
                'name': '十三陵',
                'position': [116.2170, 40.2914],
                'type': 'imperial_tomb',
                'size': 500.0,  # 范围半径（米）
                'structures': ['tomb', 'spirit_way', 'gate']
            },
            {
                'name': '颐和园',
                'position': [116.2734, 39.9999],
                'type': 'imperial_garden',
                'size': 300.0,
                'structures': ['palace', 'pavilion', 'bridge']
            },
            {
                'name': '香山',
                'position': [116.1889, 39.9956],
                'type': 'scenic_area',
                'size': 200.0,
                'structures': ['temple', 'pagoda']
            }
        ]
    
    def create_great_wall_models(self, grid: pv.StructuredGrid) -> List[pv.PolyData]:
        """
        创建长城3D模型
        """
        print("   🏯 构建长城3D模型...")
        
        wall_models = []
        bounds = grid.bounds
        
        for segment in self.great_wall_segments:
            coordinates = segment['coordinates']
            
            # 检查是否在当前地形范围内
            in_bounds = any(
                bounds[0] <= coord[0] <= bounds[1] and bounds[2] <= coord[1] <= bounds[3]
                for coord in coordinates
            )
            
            if not in_bounds:
                continue
                
            print(f"      🧱 构建 {segment['name']}...")
            
            # 获取长城路径上的地形高程
            wall_points = []
            for lon, lat in coordinates:
                # 在网格中找到最近的点
                grid_points = grid.points
                distances = np.sqrt((grid_points[:, 0] - lon)**2 + (grid_points[:, 1] - lat)**2)
                nearest_idx = np.argmin(distances)
                
                terrain_elevation = grid.points[nearest_idx, 2]
                wall_elevation = terrain_elevation + segment['elevation_offset'] * 0.0008  # 缩放
                
                wall_points.append([lon, lat, wall_elevation])
            
            wall_points = np.array(wall_points)
            
            # 创建长城几何体
            wall_mesh = self._create_wall_geometry(
                wall_points, 
                segment['wall_width'] * 0.0001,  # 缩放到地理坐标系
                segment['wall_height'] * 0.0008,
                segment['condition']
            )
            
            if wall_mesh:
                wall_models.append(wall_mesh)
        
        print(f"      ✅ 长城模型构建完成，共{len(wall_models)}段")
        return wall_models
    
    def _create_wall_geometry(self, path_points: np.ndarray, width: float, 
                            height: float, condition: str) -> Optional[pv.PolyData]:
        """
        创建长城几何体
        """
        if len(path_points) < 2:
            return None
            
        try:
            # 创建路径样条
            spline = pv.Spline(path_points, 1000)
            
            # 为样条添加厚度
            wall_base = spline.tube(radius=width/2, n_sides=4)
            
            # 创建城垛（根据状态调整）
            if condition == 'restored':
                # 完整的城垛
                battlements = self._create_battlements(path_points, width, height)
                if battlements:
                    wall_complete = wall_base.boolean_union(battlements)
                    return wall_complete
            else:
                # 废墟状态，添加破损效果
                wall_base = self._add_ruins_effect(wall_base)
            
            return wall_base
            
        except Exception as e:
            print(f"        ⚠️ 长城几何体创建失败: {e}")
            return None
    
    def _create_battlements(self, path_points: np.ndarray, width: float, 
                          height: float) -> Optional[pv.PolyData]:
        """
        创建城垛
        """
        try:
            battlements_list = []
            
            for i in range(0, len(path_points)-1, 3):  # 每3个点创建一个城垛
                point = path_points[i]
                
                # 创建城垛几何体
                battlement = pv.Box(
                    bounds=[
                        point[0] - width/4, point[0] + width/4,
                        point[1] - width/4, point[1] + width/4,
                        point[2], point[2] + height
                    ]
                )
                battlements_list.append(battlement)
            
            if battlements_list:
                # 合并所有城垛
                combined = battlements_list[0]
                for battlement in battlements_list[1:]:
                    combined = combined.boolean_union(battlement)
                return combined
                
        except Exception as e:
            print(f"        ⚠️ 城垛创建失败: {e}")
            
        return None
    
    def _add_ruins_effect(self, wall_mesh: pv.PolyData) -> pv.PolyData:
        """
        添加废墟效果
        """
        # 随机移除一些点以模拟破损
        points = wall_mesh.points
        n_points = len(points)
        
        # 随机选择70%的点保留
        keep_indices = np.random.choice(n_points, int(n_points * 0.7), replace=False)
        
        # 创建新的网格
        try:
            ruins_mesh = wall_mesh.extract_points(keep_indices)
            return ruins_mesh
        except:
            return wall_mesh


class PathwaySystem:
    """
    路径网络系统
    
    生成古道、小径等人类活动痕迹
    """
    
    def __init__(self):
        """初始化路径系统"""
        self.path_types = {
            'mountain_trail': {
                'name': '山径',
                'width': 2.0,
                'color': [0.6, 0.4, 0.2],  # 土黄色
                'slope_preference': (5, 25),
                'elevation_range': (300, 1200)
            },
            'ridge_path': {
                'name': '山脊小道',
                'width': 1.0,
                'color': [0.5, 0.3, 0.1],  # 深土色
                'slope_preference': (0, 15),
                'elevation_range': (500, 1500)
            },
            'valley_road': {
                'name': '谷地道路',
                'width': 3.0,
                'color': [0.4, 0.3, 0.2],  # 褐色
                'slope_preference': (0, 10),
                'elevation_range': (50, 500)
            }
        }
    
    def generate_pathways(self, grid: pv.StructuredGrid) -> Dict[str, np.ndarray]:
        """
        生成路径网络
        """
        print("   🛤️ 生成历史路径网络...")
        
        elevation = grid["elevation"].reshape(grid.dimensions[:2][::-1])
        slope = grid["slope"].reshape(grid.dimensions[:2][::-1])
        
        pathways = {}
        
        # 山脊路径检测
        ridge_paths = self._detect_ridges(elevation, slope)
        if ridge_paths is not None:
            pathways['ridge_paths'] = ridge_paths
        
        # 谷地路径检测  
        valley_paths = self._detect_valleys(elevation, slope)
        if valley_paths is not None:
            pathways['valley_paths'] = valley_paths
        
        print(f"      ✅ 路径生成完成，共{len(pathways)}类路径")
        return pathways
    
    def _detect_ridges(self, elevation: np.ndarray, slope: np.ndarray) -> Optional[np.ndarray]:
        """
        检测山脊线
        """
        try:
            from skimage import feature
            
            # 使用Hessian检测山脊
            ridges = feature.hessian_matrix_eigvals(elevation)
            ridge_strength = ridges[0]  # 第一个特征值
            
            # 阈值化
            ridge_mask = (ridge_strength > np.percentile(ridge_strength, 85)) & (slope < 30)
            
            return ridge_mask.astype(np.float32)
            
        except Exception as e:
            print(f"        ⚠️ 山脊检测失败: {e}")
            return None
    
    def _detect_valleys(self, elevation: np.ndarray, slope: np.ndarray) -> Optional[np.ndarray]:
        """
        检测谷地线
        """
        try:
            from scipy import ndimage
            
            # 使用形态学操作检测谷地
            kernel = np.ones((5, 5))
            valleys = ndimage.grey_erosion(elevation, structure=kernel) - elevation
            
            # 阈值化
            valley_mask = (valleys > np.percentile(valleys, 75)) & (slope < 20)
            
            return valley_mask.astype(np.float32)
            
        except Exception as e:
            print(f"        ⚠️ 谷地检测失败: {e}")
            return None
    
    def apply_pathway_textures(self, grid: pv.StructuredGrid, 
                             pathways: Dict[str, np.ndarray]) -> pv.StructuredGrid:
        """
        应用路径纹理效果
        """
        print("   🎨 应用路径纹理效果...")
        
        # 获取PBR颜色
        if "pbr_colors" in grid.array_names:
            colors = grid["pbr_colors"].astype(np.float32)
            
            for path_type, path_mask in pathways.items():
                if path_type == 'ridge_paths':
                    path_color = np.array([0.5, 0.3, 0.1]) * 255  # 深土色
                else:  # valley_paths
                    path_color = np.array([0.4, 0.3, 0.2]) * 255  # 褐色
                
                # 将路径颜色混合到原颜色
                flat_mask = path_mask.flatten()
                
                for i in range(3):  # RGB通道
                    colors[:, i] = colors[:, i] * (1 - flat_mask * 0.3) + path_color[i] * flat_mask * 0.3
            
            grid["pathway_colors"] = colors.astype(np.uint8)
        
        print("      ✅ 路径纹理应用完成")
        return grid


class HumanActivitySystem:
    """
    人类活动系统
    
    整合各种人文要素
    """
    
    def __init__(self):
        """初始化人类活动系统"""
        self.cultural_system = CulturalHeritageSysstem()
        self.pathway_system = PathwaySystem()
    
    def integrate_human_elements(self, grid: pv.StructuredGrid, 
                                plotter: pv.Plotter) -> pv.StructuredGrid:
        """
        集成所有人文要素
        """
        print("   🏛️ 集成人文历史要素...")
        
        # 1. 生成路径网络
        pathways = self.pathway_system.generate_pathways(grid)
        grid = self.pathway_system.apply_pathway_textures(grid, pathways)
        
        # 2. 创建长城模型
        wall_models = self.cultural_system.create_great_wall_models(grid)
        
        # 3. 添加长城到场景
        for wall_model in wall_models:
            plotter.add_mesh(
                wall_model,
                color=[0.6, 0.5, 0.4],  # 灰褐色石材
                opacity=0.9,
                show_edges=False,
                lighting=True,
                metallic=0.1,
                roughness=0.8
            )
        
        print("      ✅ 人文要素集成完成")
        return grid
