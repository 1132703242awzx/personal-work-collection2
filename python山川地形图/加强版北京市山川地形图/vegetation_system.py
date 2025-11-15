"""
生态系统植被分布系统
Ecological Vegetation Distribution System

功能:
1. 程序化植被生成
2. 基于地形参数的智能分布
3. 自然集群模式
4. 多种植被类型模拟
"""

import numpy as np
import pyvista as pv
from typing import Dict, List, Tuple, Optional
from scipy.spatial import distance_matrix
from sklearn.cluster import DBSCAN
import random


class VegetationSystem:
    """
    植被系统
    
    基于地形参数程序化生成和分布植被
    """
    
    def __init__(self):
        """初始化植被系统"""
        self.vegetation_types = self._create_vegetation_library()
        self.random_seed = 42
        
    def _create_vegetation_library(self) -> Dict:
        """
        创建植被库
        """
        return {
            'tree_cluster_deciduous': {
                'name': '落叶乔木丛',
                'height_range': (5.0, 15.0),  # 米
                'radius_range': (2.0, 6.0),   # 米
                'density': 0.3,               # 分布密度
                'elevation_range': (200, 1200),
                'slope_range': (5, 35),
                'moisture_preference': 'high',  # 喜湿润
                'aspect_preference': 'north',   # 偏好北坡
                'color': [0.2, 0.6, 0.2],      # 深绿色
                'cluster_size': (3, 8)         # 集群大小
            },
            
            'tree_cluster_coniferous': {
                'name': '针叶乔木丛',
                'height_range': (8.0, 20.0),
                'radius_range': (1.5, 4.0),
                'density': 0.25,
                'elevation_range': (400, 1500),
                'slope_range': (10, 45),
                'moisture_preference': 'medium',
                'aspect_preference': 'north',
                'color': [0.1, 0.4, 0.1],      # 深绿偏暗
                'cluster_size': (5, 12)
            },
            
            'bush_01': {
                'name': '灌木',
                'height_range': (1.0, 4.0),
                'radius_range': (0.8, 2.5),
                'density': 0.4,
                'elevation_range': (50, 1000),
                'slope_range': (0, 50),
                'moisture_preference': 'medium',
                'aspect_preference': 'any',
                'color': [0.3, 0.5, 0.2],      # 中绿色
                'cluster_size': (2, 6)
            },
            
            'grass_patch': {
                'name': '草簇',
                'height_range': (0.2, 1.0),
                'radius_range': (0.5, 1.5),
                'density': 0.6,
                'elevation_range': (20, 800),
                'slope_range': (0, 40),
                'moisture_preference': 'any',
                'aspect_preference': 'any',
                'color': [0.4, 0.7, 0.3],      # 浅绿色
                'cluster_size': (5, 15)
            }
        }
    
    def calculate_vegetation_suitability(self, elevation: np.ndarray, 
                                       slope: np.ndarray, 
                                       aspect: np.ndarray) -> Dict[str, np.ndarray]:
        """
        计算各类植被的适宜性
        
        Args:
            elevation: 高程数据
            slope: 坡度数据
            aspect: 坡向数据
            
        Returns:
            各植被类型的适宜性权重字典
        """
        print("   🌱 计算植被生态适宜性...")
        
        suitability = {}
        
        # 计算水分指数 (基于坡向和高程)
        north_facing = np.cos(np.radians(aspect))  # 北坡系数
        moisture_index = (north_facing + 1) / 2 * (1 + elevation / 2000)  # 0-1范围
        
        for veg_type, veg_props in self.vegetation_types.items():
            # 基础适宜性
            suit = np.ones_like(elevation) * 0.1
            
            # 高程适宜性
            elev_min, elev_max = veg_props['elevation_range']
            elev_suit = np.where(
                (elevation >= elev_min) & (elevation <= elev_max),
                1.0 - abs(elevation - (elev_min + elev_max) / 2) / (elev_max - elev_min),
                0.1
            )
            
            # 坡度适宜性
            slope_min, slope_max = veg_props['slope_range']
            slope_suit = np.where(
                (slope >= slope_min) & (slope <= slope_max),
                1.0 - abs(slope - (slope_min + slope_max) / 2) / (slope_max - slope_min),
                0.1
            )
            
            # 水分偏好
            if veg_props['moisture_preference'] == 'high':
                moisture_suit = moisture_index ** 0.5
            elif veg_props['moisture_preference'] == 'medium':
                moisture_suit = 1.0 - abs(moisture_index - 0.5) * 2
            else:  # any
                moisture_suit = np.ones_like(moisture_index)
            
            # 坡向偏好
            if veg_props['aspect_preference'] == 'north':
                aspect_suit = (north_facing + 1) / 2
            else:  # any
                aspect_suit = np.ones_like(aspect)
            
            # 排除陡峭岩石区域
            rock_exclusion = np.where((slope > 60) | (elevation > 1400), 0.1, 1.0)
            
            # 综合适宜性
            suit = elev_suit * slope_suit * moisture_suit * aspect_suit * rock_exclusion
            suit = np.clip(suit, 0, 1)
            
            suitability[veg_type] = suit
        
        print(f"      ✅ 植被适宜性计算完成，共{len(suitability)}种植被类型")
        return suitability
    
    def generate_vegetation_clusters(self, grid: pv.StructuredGrid, 
                                   suitability: Dict[str, np.ndarray]) -> List[Dict]:
        """
        生成植被集群
        
        Args:
            grid: 地形网格
            suitability: 植被适宜性数据
            
        Returns:
            植被实例列表
        """
        print("   🌳 生成植被集群分布...")
        
        vegetation_instances = []
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
        
        # 获取网格信息
        points = grid.points
        bounds = grid.bounds
        width = bounds[1] - bounds[0]
        height = bounds[3] - bounds[2]
        
        for veg_type, suit_map in suitability.items():
            veg_props = self.vegetation_types[veg_type]
            
            # 根据适宜性和密度确定采样点数量
            total_suitability = np.sum(suit_map)
            target_count = int(total_suitability * veg_props['density'] * 0.001)  # 缩放因子
            
            if target_count < 5:
                continue
                
            print(f"      🌿 生成 {veg_props['name']}: 目标数量 {target_count}")
            
            # 使用加权随机采样选择位置
            flat_suit = suit_map.flatten()
            valid_indices = np.where(flat_suit > 0.3)[0]  # 只考虑适宜性较高的区域
            
            if len(valid_indices) < target_count:
                sample_indices = valid_indices
            else:
                # 加权采样
                weights = flat_suit[valid_indices]
                weights = weights / np.sum(weights)
                
                sample_indices = np.random.choice(
                    valid_indices, 
                    size=min(target_count, len(valid_indices)), 
                    replace=False, 
                    p=weights
                )
            
            # 对采样点进行聚类以形成自然分布
            sampled_points = points[sample_indices]
            
            if len(sampled_points) > 1:
                # 使用DBSCAN进行聚类
                clustering = DBSCAN(eps=width*0.02, min_samples=2).fit(sampled_points[:, :2])
                
                # 为每个聚类生成植被实例
                unique_labels = set(clustering.labels_)
                
                for label in unique_labels:
                    if label == -1:  # 噪声点，单独处理
                        noise_mask = clustering.labels_ == -1
                        noise_points = sampled_points[noise_mask]
                        
                        for point in noise_points:
                            instance = self._create_vegetation_instance(
                                veg_type, point, veg_props, is_cluster=False
                            )
                            vegetation_instances.append(instance)
                    else:
                        # 聚类中心
                        cluster_mask = clustering.labels_ == label
                        cluster_points = sampled_points[cluster_mask]
                        cluster_center = np.mean(cluster_points, axis=0)
                        
                        # 在聚类中心周围生成多个实例
                        cluster_size = random.randint(*veg_props['cluster_size'])
                        cluster_size = min(cluster_size, len(cluster_points) * 2)
                        
                        for i in range(cluster_size):
                            # 在聚类中心周围随机偏移
                            offset_distance = np.random.exponential(width * 0.01)
                            offset_angle = np.random.uniform(0, 2 * np.pi)
                            
                            offset_x = offset_distance * np.cos(offset_angle)
                            offset_y = offset_distance * np.sin(offset_angle)
                            
                            instance_pos = cluster_center.copy()
                            instance_pos[0] += offset_x
                            instance_pos[1] += offset_y
                            
                            # 确保位置在有效范围内
                            if (bounds[0] <= instance_pos[0] <= bounds[1] and 
                                bounds[2] <= instance_pos[1] <= bounds[3]):
                                
                                instance = self._create_vegetation_instance(
                                    veg_type, instance_pos, veg_props, is_cluster=True
                                )
                                vegetation_instances.append(instance)
        
        print(f"      ✅ 植被生成完成，共{len(vegetation_instances)}个实例")
        return vegetation_instances
    
    def _create_vegetation_instance(self, veg_type: str, position: np.ndarray, 
                                  veg_props: Dict, is_cluster: bool = False) -> Dict:
        """
        创建单个植被实例
        """
        # 随机化尺寸
        height = random.uniform(*veg_props['height_range'])
        radius = random.uniform(*veg_props['radius_range'])
        
        # 随机旋转
        rotation = random.uniform(0, 360)
        
        # 聚类中的实例稍小一些
        if is_cluster:
            height *= random.uniform(0.7, 1.0)
            radius *= random.uniform(0.7, 1.0)
        
        return {
            'type': veg_type,
            'position': position,
            'height': height,
            'radius': radius,
            'rotation': rotation,
            'color': veg_props['color'],
            'properties': veg_props
        }
    
    def add_vegetation_to_scene(self, plotter: pv.Plotter, 
                              vegetation_instances: List[Dict]) -> None:
        """
        将植被添加到3D场景中
        """
        print("   🌲 添加植被到3D场景...")
        
        # 按类型分组以优化渲染
        type_groups = {}
        for instance in vegetation_instances:
            veg_type = instance['type']
            if veg_type not in type_groups:
                type_groups[veg_type] = []
            type_groups[veg_type].append(instance)
        
        for veg_type, instances in type_groups.items():
            if not instances:
                continue
                
            veg_props = self.vegetation_types[veg_type]
            print(f"      🌿 添加 {veg_props['name']}: {len(instances)} 个实例")
            
            # 创建代表性几何体
            if 'tree' in veg_type:
                # 树木：圆锥体或圆柱体
                base_mesh = pv.Cone(radius=1.0, height=2.0, resolution=8)
            elif 'bush' in veg_type:
                # 灌木：球体
                base_mesh = pv.Sphere(radius=1.0, phi_resolution=8, theta_resolution=8)
            else:
                # 草簇：扁平椭球
                base_mesh = pv.Sphere(radius=1.0, phi_resolution=6, theta_resolution=6)
                base_mesh.points[:, 2] *= 0.3  # 压扁
            
            # 批量添加实例
            for i, instance in enumerate(instances):
                if i % 20 == 0:  # 减少渲染负载，每20个显示一个
                    mesh = base_mesh.copy()
                    
                    # 缩放
                    scale = [instance['radius'], instance['radius'], instance['height']]
                    mesh.scale(scale)
                    
                    # 旋转
                    mesh.rotate_z(instance['rotation'])
                    
                    # 平移
                    mesh.translate(instance['position'])
                    
                    # 添加到场景
                    color = [int(c * 255) for c in instance['color']]
                    plotter.add_mesh(
                        mesh,
                        color=color,
                        opacity=0.8,
                        show_edges=False,
                        lighting=True
                    )
        
        print("      ✅ 植被场景构建完成")
