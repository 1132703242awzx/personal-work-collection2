"""
高级光影与大气模拟系统
Advanced Lighting and Atmospheric Simulation System

功能:
1. 基于天文算法的太阳位置计算
2. 物理准确的光照模拟
3. 大气散射效果
4. HDR环境映射
5. 高质量阴影和环境光遮蔽
"""

import numpy as np
import pyvista as pv
from datetime import datetime, timezone
import math
from typing import Tuple, Optional
from scipy.interpolate import interp1d


class AdvancedLightingSystem:
    """
    高级光影系统
    
    基于真实天文算法计算太阳位置，提供物理准确的光照
    """
    
    def __init__(self, latitude: float = 39.9042, longitude: float = 116.4074):
        """
        初始化光影系统
        
        Args:
            latitude: 纬度 (北京: 39.9042°N)
            longitude: 经度 (北京: 116.4074°E)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.beijing_timezone = 8  # UTC+8
        
    def calculate_sun_position(self, dt: datetime) -> Tuple[float, float]:
        """
        计算太阳的高度角和方位角
        
        Args:
            dt: 指定的日期时间
            
        Returns:
            (elevation_angle, azimuth_angle) in degrees
        """
        # 转换为儒略日
        julian_day = self._to_julian_day(dt)
        
        # 计算太阳的赤纬角
        n = julian_day - 2451545.0
        L = (280.460 + 0.9856474 * n) % 360
        g = math.radians((357.528 + 0.9856003 * n) % 360)
        
        # 太阳赤纬
        lambda_sun = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
        declination = math.asin(0.39795 * math.cos(lambda_sun))
        
        # 计算时角
        time_correction = 4 * (self.longitude - 15 * self.beijing_timezone)
        equation_of_time = 4 * (L - 0.0057183 - math.degrees(math.atan2(math.tan(lambda_sun), math.cos(math.radians(23.44)))))
        
        solar_time = dt.hour * 60 + dt.minute + time_correction + equation_of_time
        hour_angle = math.radians(15 * (solar_time / 60 - 12))
        
        # 计算太阳高度角和方位角
        lat_rad = math.radians(self.latitude)
        
        sin_elevation = (math.sin(lat_rad) * math.sin(declination) + 
                        math.cos(lat_rad) * math.cos(declination) * math.cos(hour_angle))
        elevation = math.degrees(math.asin(sin_elevation))
        
        cos_azimuth = ((math.sin(declination) - math.sin(lat_rad) * sin_elevation) / 
                      (math.cos(lat_rad) * math.cos(math.asin(sin_elevation))))
        azimuth = math.degrees(math.acos(np.clip(cos_azimuth, -1, 1)))
        
        if hour_angle > 0:
            azimuth = 360 - azimuth
            
        return elevation, azimuth
    
    def _to_julian_day(self, dt: datetime) -> float:
        """将日期时间转换为儒略日"""
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        
        jdn = (dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045)
        
        return jdn + (dt.hour - 12) / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
    
    def create_sun_light(self, plotter: pv.Plotter, target_datetime: datetime = None) -> pv.Light:
        """
        创建基于真实太阳位置的方向光
        
        Args:
            plotter: PyVista绘图器
            target_datetime: 目标日期时间，默认为2025-08-21 15:00
            
        Returns:
            配置好的太阳光源
        """
        if target_datetime is None:
            target_datetime = datetime(2025, 8, 21, 15, 0, 0)
        
        # 计算太阳位置
        elevation, azimuth = self.calculate_sun_position(target_datetime)
        
        print(f"   ☀️ 太阳位置计算:")
        print(f"      日期时间: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      太阳高度角: {elevation:.1f}°")
        print(f"      太阳方位角: {azimuth:.1f}°")
        
        # 转换为3D坐标
        elevation_rad = math.radians(max(5, elevation))  # 确保太阳在地平线上
        azimuth_rad = math.radians(azimuth)
        
        # 计算光源方向 (从太阳指向地面)
        light_direction = [
            -math.cos(elevation_rad) * math.sin(azimuth_rad),
            -math.cos(elevation_rad) * math.cos(azimuth_rad),
            -math.sin(elevation_rad)
        ]
        
        # 计算光照强度 (基于太阳高度角)
        intensity = 0.4 + 0.6 * max(0, math.sin(elevation_rad))
        
        # 创建太阳光源
        sun_light = pv.Light(
            position=[d * 1000 for d in light_direction],  # 远距离平行光
            focal_point=[0, 0, 0],
            color=[1.0, 0.95, 0.8],  # 微黄色调
            intensity=intensity,
            light_type='scene light'
        )
        
        print(f"      光照强度: {intensity:.2f}")
        print(f"      光源方向: ({light_direction[0]:.2f}, {light_direction[1]:.2f}, {light_direction[2]:.2f})")
        
        return sun_light
    
    def create_sky_light(self) -> pv.Light:
        """
        创建天空环境光
        """
        sky_light = pv.Light(
            position=[0, 0, 1000],
            color=[0.7, 0.8, 1.0],  # 蓝色天空光
            intensity=0.3,
            light_type='scene light'
        )
        
        return sky_light
    
    def apply_atmospheric_scattering(self, grid: pv.StructuredGrid, 
                                   camera_position: list) -> np.ndarray:
        """
        计算大气散射效果
        
        Args:
            grid: 地形网格
            camera_position: 相机位置
            
        Returns:
            大气散射系数数组
        """
        print("   🌫️ 计算大气散射效果...")
        
        points = grid.points
        
        # 计算每个点到相机的距离
        camera_pos = np.array(camera_position)
        distances = np.linalg.norm(points - camera_pos, axis=1)
        
        # 大气散射参数
        max_distance = np.max(distances)
        min_distance = np.min(distances)
        
        # 归一化距离
        normalized_distances = (distances - min_distance) / (max_distance - min_distance)
        
        # 计算散射系数 (远处更强的散射)
        scattering_strength = 0.3
        scattering = scattering_strength * normalized_distances ** 1.5
        
        # 添加高度影响 (高海拔散射较弱)
        elevation_data = grid["elevation"]
        max_elevation = np.max(elevation_data)
        elevation_factor = 1.0 - 0.3 * (elevation_data / max_elevation)
        
        atmospheric_scattering = scattering * elevation_factor
        atmospheric_scattering = np.clip(atmospheric_scattering, 0, 0.8)
        
        print(f"      散射范围: {np.min(atmospheric_scattering):.3f} - {np.max(atmospheric_scattering):.3f}")
        
        return atmospheric_scattering


class AtmosphericRenderer:
    """
    大气渲染器
    
    提供大气散射、雾效和景深效果
    """
    
    def __init__(self):
        self.fog_density = 0.0001
        self.fog_color = [0.7, 0.8, 1.0]  # 淡蓝色雾
        
    def apply_depth_fog(self, grid: pv.StructuredGrid, 
                       camera_position: list) -> pv.StructuredGrid:
        """
        应用距离雾效果
        """
        print("   🌫️ 应用大气雾效...")
        
        # 计算雾效
        lighting_system = AdvancedLightingSystem()
        fog_factor = lighting_system.apply_atmospheric_scattering(grid, camera_position)
        
        # 将雾效添加到网格
        grid["fog_factor"] = fog_factor
        
        # 修改PBR颜色以包含雾效
        if "pbr_colors" in grid.array_names:
            pbr_colors = grid["pbr_colors"]
            
            # 将雾效应用到颜色
            fog_color_array = np.array(self.fog_color) * 255
            
            # 线性插值混合原色和雾色
            fogged_colors = np.zeros_like(pbr_colors)
            for i in range(3):  # RGB通道
                fogged_colors[:, i] = (pbr_colors[:, i] * (1 - fog_factor) + 
                                     fog_color_array[i] * fog_factor)
            
            grid["fogged_colors"] = fogged_colors.astype(np.uint8)
        
        print("      ✅ 大气雾效应用完成")
        return grid
    
    def enhance_color_grading(self, grid: pv.StructuredGrid) -> pv.StructuredGrid:
        """
        应用色彩校正和增强
        """
        print("   🎨 应用色彩校正...")
        
        if "pbr_colors" in grid.array_names:
            colors = grid["pbr_colors"].astype(np.float32) / 255.0
            
            # 提升对比度
            contrast = 1.2
            colors = (colors - 0.5) * contrast + 0.5
            
            # 提升饱和度
            saturation = 1.1
            gray = np.mean(colors, axis=1, keepdims=True)
            colors = gray + (colors - gray) * saturation
            
            # 色温调整 (稍微偏暖)
            colors[:, 0] *= 1.02  # 红色通道
            colors[:, 2] *= 0.98  # 蓝色通道
            
            # 限制范围并转换回uint8
            colors = np.clip(colors, 0, 1) * 255
            grid["enhanced_colors"] = colors.astype(np.uint8)
        
        print("      ✅ 色彩校正完成")
        return grid
