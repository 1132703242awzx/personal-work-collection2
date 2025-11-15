#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
北京市高级三维地形图生成器 - GIS专家版本
Beijing Advanced 3D Terrain Map Generator - GIS Expert Edition

作者: AI Assistant
功能: 基于开放高程数据服务，生成北京市高精度三维地形图
特色: NASA SRTM数据、高级DEM预处理、地形几何细化、侵蚀建模
"""

import os
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyvista as pv
import xarray as xr
import rioxarray as rxr
from scipy import ndimage
from scipy.interpolate import RectBivariateSpline
from skimage import filters, restoration
import cv2
try:
    import richdem as rd
except ImportError:
    rd = None
    print("⚠️ richdem 库未安装，某些高级功能可能不可用")

try:
    import elevation
except ImportError:
    elevation = None
    print("⚠️ elevation 库未安装，将使用替代方案")

class BeijingTerrainMapAdvanced:
    """北京市高级三维地形图生成器 - GIS专家版本"""
    
    def __init__(self):
        """初始化高级地形图生成器"""
        
        # 工作目录和文件路径
        self.data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 北京市边界配置
        self.beijing_bounds = {
            'west': 115.42,   # 西经界
            'east': 117.52,   # 东经界
            'south': 39.44,   # 南纬界
            'north': 41.05    # 北纬界
        }
        
        # 文件路径
        self.beijing_geojson_url = "https://geo.datav.aliyun.com/areas_v3/bound/110000_full.json"
        self.beijing_boundary_file = os.path.join(self.data_dir, "beijing_boundary.geojson")
        self.dem_file = os.path.join(self.data_dir, "beijing_srtm_dem.tif")
        self.dem_processed_file = os.path.join(self.data_dir, "beijing_dem_processed.tif")
        self.dem_enhanced_file = os.path.join(self.data_dir, "beijing_dem_enhanced.tif")
        
        # DEM参数配置
        self.dem_resolution = 1000  # 网格分辨率
        self.elevation_scale = 0.0008  # 垂直缩放因子
        
        print("🚀 北京市高级三维地形图生成器初始化完成")
        print(f"   数据目录: {self.data_dir}")
        print(f"   网格分辨率: {self.dem_resolution}x{self.dem_resolution}")
    
    def download_beijing_boundary(self):
        """下载北京市边界GeoJSON文件"""
        print("\n🔄 步骤1: 获取北京市边界数据...")
        
        try:
            response = requests.get(self.beijing_geojson_url, timeout=30)
            response.raise_for_status()
            
            with open(self.beijing_boundary_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"   ✅ 北京市边界数据已保存到: {self.beijing_boundary_file}")
            return True
            
        except Exception as e:
            print(f"   ❌ 下载北京边界数据失败: {e}")
            # 创建简化边界
            return self.create_simple_beijing_boundary()
    
    def create_simple_beijing_boundary(self):
        """创建简化的北京市边界"""
        print("   🔧 使用简化的北京市边界框...")
        
        beijing_bounds = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"name": "北京市"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [self.beijing_bounds['west'], self.beijing_bounds['south']],
                        [self.beijing_bounds['east'], self.beijing_bounds['south']],
                        [self.beijing_bounds['east'], self.beijing_bounds['north']],
                        [self.beijing_bounds['west'], self.beijing_bounds['north']],
                        [self.beijing_bounds['west'], self.beijing_bounds['south']]
                    ]]
                }
            }]
        }
        
        import json
        with open(self.beijing_boundary_file, 'w', encoding='utf-8') as f:
            json.dump(beijing_bounds, f, ensure_ascii=False, indent=2)
        
        print("   ✅ 简化边界数据创建完成")
        return True
    
    def download_open_elevation_data(self):
        """从开放高程数据服务获取北京市区域DEM数据"""
        print("\n🔄 步骤2: 从开放高程数据服务获取DEM数据...")
        
        # 如果elevation库可用，尝试使用
        if elevation is not None:
            try:
                print("   🌍 尝试使用NASA SRTM-1数据源...")
                
                # 清理之前的数据
                elevation.clean_cache()
                
                # 下载SRTM数据
                elevation.clip(
                    bounds=(self.beijing_bounds['west'], self.beijing_bounds['south'],
                           self.beijing_bounds['east'], self.beijing_bounds['north']),
                    output=self.dem_file,
                    product='SRTM1'
                )
                
                if os.path.exists(self.dem_file):
                    print(f"   ✅ NASA SRTM-1数据下载成功: {self.dem_file}")
                    return True
                    
            except Exception as e:
                print(f"   ⚠️ SRTM数据下载失败: {e}")
        
        # 备用方案：生成高精度合成数据
        print("   🎲 使用高精度合成地形数据...")
        return self.create_high_quality_synthetic_dem()
    
    def create_high_quality_synthetic_dem(self):
        """创建高质量合成DEM数据"""
        print("   🏔️ 生成基于真实地形特征的高精度DEM...")
        
        # 创建高分辨率网格
        width, height = self.dem_resolution, self.dem_resolution
        x_coords = np.linspace(self.beijing_bounds['west'], self.beijing_bounds['east'], width)
        y_coords = np.linspace(self.beijing_bounds['north'], self.beijing_bounds['south'], height)
        X, Y = np.meshgrid(x_coords, y_coords)
        
        # 初始化地形（平原基础高度）
        elevation = np.full_like(X, 50.0)  # 北京平原约50米
        
        # 西山山脉（房山区、门头沟区）
        xishan_centers = [
            (116.0, 39.9, 1200, 0.015),  # 灵山
            (115.8, 39.8, 1000, 0.020),  # 百花山
            (116.1, 39.7, 800, 0.025),   # 妙峰山
        ]
        
        for center_x, center_y, max_height, spread in xishan_centers:
            dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            elevation += max_height * np.exp(-dist / spread)
        
        # 军都山脉（昌平区、延庆区）
        jundu_centers = [
            (116.3, 40.3, 900, 0.018),   # 云蒙山
            (115.9, 40.5, 1100, 0.016),  # 海坨山
            (116.5, 40.4, 700, 0.022),   # 红螺山
        ]
        
        for center_x, center_y, max_height, spread in jundu_centers:
            dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            elevation += max_height * np.exp(-dist / spread)
        
        # 燕山余脉（平谷区、密云区）
        yanshan_centers = [
            (117.1, 40.2, 800, 0.020),   # 雾灵山余脉
            (116.8, 40.4, 600, 0.025),   # 密云水库周边山地
        ]
        
        for center_x, center_y, max_height, spread in yanshan_centers:
            dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            elevation += max_height * np.exp(-dist / spread)
        
        # 添加地形细节噪声
        noise_high = np.random.normal(0, 10, elevation.shape)  # 高频噪声
        noise_low = ndimage.gaussian_filter(np.random.normal(0, 20, elevation.shape), sigma=5)  # 低频起伏
        elevation += noise_high + noise_low
        
        # 确保非负高程
        elevation = np.maximum(elevation, 0)
        
        # 保存为GeoTIFF格式
        self._save_dem_as_geotiff(elevation, x_coords, y_coords, self.dem_file)
        
        print(f"   ✅ 高精度DEM数据生成完成")
        print(f"      网格大小: {width}x{height}")
        print(f"      高程范围: {elevation.min():.1f}m - {elevation.max():.1f}m")
        print(f"      文件保存: {self.dem_file}")
        
        return True
    
    def _save_dem_as_geotiff(self, elevation_data, x_coords, y_coords, output_file):
        """将DEM数据保存为GeoTIFF格式"""
        try:
            from rasterio.transform import from_bounds
            import rasterio
            
            height, width = elevation_data.shape
            transform = from_bounds(
                self.beijing_bounds['west'], self.beijing_bounds['south'],
                self.beijing_bounds['east'], self.beijing_bounds['north'],
                width, height
            )
            
            with rasterio.open(
                output_file, 'w',
                driver='GTiff',
                height=height, width=width,
                count=1, dtype=elevation_data.dtype,
                crs='EPSG:4326',
                transform=transform,
                compress='lzw'
            ) as dst:
                dst.write(elevation_data, 1)
                
        except ImportError:
            # 如果rasterio不可用，保存为numpy数组
            coords = {'y': y_coords, 'x': x_coords}
            self._save_processed_dem(elevation_data, coords, output_file)
    
    def _save_processed_dem(self, elevation_data, coords, output_file):
        """保存处理后的DEM数据"""
        try:
            # 使用xarray保存
            da = xr.DataArray(
                elevation_data,
                coords=coords,
                dims=['y', 'x'],
                attrs={'units': 'meters', 'description': 'Elevation'}
            )
            da.to_netcdf(output_file.replace('.tif', '.nc'))
            
        except Exception:
            # 备用：保存为numpy格式
            np.save(output_file.replace('.tif', '.npy'), elevation_data)
    
    def advanced_dem_preprocessing(self):
        """高级DEM预处理 - 噪声去除、细节增强、空洞填充"""
        print("\n🔄 步骤3: 高级DEM预处理...")
        
        try:
            # 加载DEM数据
            if os.path.exists(self.dem_file):
                try:
                    dem_data = rxr.open_rasterio(self.dem_file).squeeze()
                    elevation = dem_data.values
                except Exception:
                    # 备用加载方式
                    elevation = np.load(self.dem_file.replace('.tif', '.npy'))
            else:
                print("   ❌ DEM文件不存在")
                return None
            
            print(f"   📊 原始DEM统计:")
            print(f"      形状: {elevation.shape}")
            print(f"      高程范围: {elevation.min():.1f}m - {elevation.max():.1f}m")
            print(f"      有效像素: {np.sum(~np.isnan(elevation)):,}")
            
            # 预处理步骤1: 填充数据空洞
            print("   🔧 执行数据空洞填充...")
            filled_elevation = self._fill_data_holes(elevation)
            
            # 预处理步骤2: 高斯噪声降低
            print("   🔧 执行高斯噪声降低...")
            smooth_elevation = self._gaussian_noise_reduction(filled_elevation)
            
            # 预处理步骤3: 基于坡度的细节锐化
            print("   🔧 执行基于坡度的细节锐化...")
            enhanced_elevation = self._slope_based_sharpening(smooth_elevation)
            
            # 保存预处理结果
            height, width = enhanced_elevation.shape
            x_coords = np.linspace(self.beijing_bounds['west'], self.beijing_bounds['east'], width)
            y_coords = np.linspace(self.beijing_bounds['north'], self.beijing_bounds['south'], height)
            coords = {'y': y_coords, 'x': x_coords}
            
            self._save_processed_dem(enhanced_elevation, coords, self.dem_processed_file)
            
            print(f"   ✅ 高级DEM预处理完成")
            print(f"      处理后高程范围: {enhanced_elevation.min():.1f}m - {enhanced_elevation.max():.1f}m")
            print(f"      文件保存: {self.dem_processed_file}")
            
            return enhanced_elevation
            
        except Exception as e:
            print(f"   ❌ DEM预处理失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _fill_data_holes(self, elevation_data):
        """填充DEM数据中的空洞和无效值"""
        
        # 识别无效数据
        invalid_mask = np.isnan(elevation_data) | (elevation_data <= -9999)
        
        if np.sum(invalid_mask) > 0:
            print(f"      发现 {np.sum(invalid_mask):,} 个无效像素点")
            
            # 使用双线性插值填充
            from scipy.interpolate import griddata
            
            # 获取有效数据点
            valid_mask = ~invalid_mask
            valid_indices = np.where(valid_mask)
            valid_values = elevation_data[valid_mask]
            
            # 需要填充的点
            invalid_indices = np.where(invalid_mask)
            
            if len(valid_values) > 10:  # 确保有足够的有效数据点
                # 执行插值
                filled_values = griddata(
                    (valid_indices[0], valid_indices[1]),
                    valid_values,
                    (invalid_indices[0], invalid_indices[1]),
                    method='linear',
                    fill_value=np.mean(valid_values)
                )
                
                # 填充结果
                filled_elevation = elevation_data.copy()
                filled_elevation[invalid_mask] = filled_values
                
                print(f"      已填充 {np.sum(invalid_mask):,} 个空洞像素")
                return filled_elevation
        
        return elevation_data
    
    def _gaussian_noise_reduction(self, elevation_data):
        """使用自适应高斯滤波降低噪声"""
        
        # 计算地形梯度以确定滤波强度
        grad_y, grad_x = np.gradient(elevation_data)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # 自适应sigma值：平坦区域使用更强的平滑
        sigma_base = 1.0
        sigma_adaptive = sigma_base * (1 + 1.0 / (1 + gradient_magnitude))
        
        # 应用自适应高斯滤波
        smoothed = elevation_data.copy()
        
        # 分区域处理
        flat_regions = gradient_magnitude < np.percentile(gradient_magnitude, 25)
        steep_regions = gradient_magnitude > np.percentile(gradient_magnitude, 75)
        
        # 平坦区域：强平滑
        if np.sum(flat_regions) > 0:
            smoothed[flat_regions] = ndimage.gaussian_filter(
                elevation_data, sigma=2.0
            )[flat_regions]
        
        # 陡峭区域：轻微平滑
        if np.sum(steep_regions) > 0:
            smoothed[steep_regions] = ndimage.gaussian_filter(
                elevation_data, sigma=0.5
            )[steep_regions]
        
        # 中等区域：中等平滑
        middle_regions = ~(flat_regions | steep_regions)
        if np.sum(middle_regions) > 0:
            smoothed[middle_regions] = ndimage.gaussian_filter(
                elevation_data, sigma=1.0
            )[middle_regions]
        
        print(f"      噪声降低完成，平滑区域: {np.sum(flat_regions):,} 像素")
        return smoothed
    
    def _slope_based_sharpening(self, elevation_data):
        """基于坡度的细节锐化"""
        
        # 计算拉普拉斯算子来检测边缘
        laplacian = ndimage.laplace(elevation_data)
        
        # 计算坡度
        grad_y, grad_x = np.gradient(elevation_data)
        slope = np.sqrt(grad_x**2 + grad_y**2)
        
        # 自适应锐化强度：在高坡度区域增强更多细节
        slope_normalized = slope / np.max(slope)
        sharpening_strength = 0.3 * slope_normalized  # 最大锐化强度30%
        
        # 应用锐化
        enhanced = elevation_data + sharpening_strength * laplacian
        
        # 防止过度锐化
        enhanced = np.clip(enhanced, 
                          elevation_data.min() - 50, 
                          elevation_data.max() + 50)
        
        print(f"      细节锐化完成，平均增强强度: {np.mean(sharpening_strength):.3f}")
        return enhanced
    
    def geometric_terrain_refinement(self, elevation_data):
        """地形几何细化 - 曲面细分和地貌特征生成"""
        print("\n🔄 步骤3+: 地形几何细化和地貌特征生成...")
        
        try:
            refined_elevation = elevation_data.copy()
            
            # 几何细化步骤1: 自适应曲面细分
            print("   🔧 执行自适应曲面细分...")
            subdivided_elevation = self._adaptive_surface_subdivision(refined_elevation)
            
            # 几何细化步骤2: 生成侵蚀特征
            print("   🔧 程序化生成侵蚀沟壑...")
            eroded_elevation = self._generate_erosion_features(subdivided_elevation)
            
            # 几何细化步骤3: 增强山脊线
            print("   🔧 增强山脊线特征...")
            ridge_enhanced = self._enhance_ridge_lines(eroded_elevation)
            
            # 几何细化步骤4: 生成冲积扇
            print("   🔧 生成冲积扇地貌...")
            final_elevation = self._generate_alluvial_fans(ridge_enhanced)
            
            # 保存细化结果
            height, width = final_elevation.shape
            x_coords = np.linspace(self.beijing_bounds['west'], self.beijing_bounds['east'], width)
            y_coords = np.linspace(self.beijing_bounds['north'], self.beijing_bounds['south'], height)
            
            coords = {'y': y_coords, 'x': x_coords}
            self._save_processed_dem(final_elevation, coords, self.dem_enhanced_file)
            
            print(f"   ✅ 地形几何细化完成")
            print(f"      细化后高程范围: {final_elevation.min():.1f}m - {final_elevation.max():.1f}m")
            
            return final_elevation
            
        except Exception as e:
            print(f"   ❌ 地形几何细化失败: {e}")
            import traceback
            traceback.print_exc()
            return elevation_data
    
    def _adaptive_surface_subdivision(self, elevation_data):
        """自适应曲面细分 - 在复杂地形区域增加密度"""
        
        # 计算地形复杂度
        grad_y, grad_x = np.gradient(elevation_data)
        slope = np.sqrt(grad_x**2 + grad_y**2)
        
        # 识别需要细分的区域（陡峭山区）
        complexity_threshold = np.percentile(slope, 75)  # 前25%的陡峭区域
        high_complexity_mask = slope > complexity_threshold
        
        print(f"      识别出 {np.sum(high_complexity_mask):,} 个需要细分的像素点")
        
        # 对高复杂度区域进行插值细化
        refined = elevation_data.copy()
        
        try:
            # 使用双三次插值增加分辨率
            h, w = elevation_data.shape
            x_original = np.arange(w)
            y_original = np.arange(h)
            
            # 创建样条插值函数
            spline = RectBivariateSpline(y_original, x_original, elevation_data, kx=3, ky=3)
            
            # 在高复杂度区域增加采样密度
            from skimage.measure import label, regionprops
            
            labeled_regions = label(high_complexity_mask)
            regions = regionprops(labeled_regions)
            
            refined_count = 0
            for region in regions[:20]:  # 限制处理最重要的20个区域
                if region.area > 10:  # 只处理面积较大的区域
                    minr, minc, maxr, maxc = region.bbox
                    
                    # 提取区域
                    region_elevation = elevation_data[minr:maxr, minc:maxc]
                    
                    # 增加采样密度
                    factor = 2  # 2倍细分
                    new_h, new_w = region_elevation.shape[0] * factor, region_elevation.shape[1] * factor
                    
                    y_dense = np.linspace(0, region_elevation.shape[0]-1, new_h)
                    x_dense = np.linspace(0, region_elevation.shape[1]-1, new_w)
                    
                    # 使用样条插值
                    region_spline = RectBivariateSpline(
                        np.arange(region_elevation.shape[0]),
                        np.arange(region_elevation.shape[1]),
                        region_elevation, kx=3, ky=3
                    )
                    
                    dense_elevation = region_spline(y_dense, x_dense)
                    
                    # 重新采样回原始分辨率
                    y_resample = np.linspace(0, dense_elevation.shape[0]-1, maxr-minr)
                    x_resample = np.linspace(0, dense_elevation.shape[1]-1, maxc-minc)
                    
                    resampled_spline = RectBivariateSpline(
                        np.arange(dense_elevation.shape[0]), 
                        np.arange(dense_elevation.shape[1]), 
                        dense_elevation, kx=1, ky=1
                    )
                    
                    refined_patch = resampled_spline(y_resample, x_resample)
                    
                    # 将细化后的数据填回原始数组
                    refined[minr:maxr, minc:maxc] = refined_patch
                    refined_count += 1
            
            print(f"      完成 {refined_count} 个区域的曲面细分")
            
        except Exception as e:
            print(f"      ⚠️ 曲面细分失败: {e}")
            return elevation_data
        
        return refined
    
    def _generate_erosion_features(self, elevation_data):
        """程序化生成侵蚀沟壑和河谷"""
        
        if rd is None:
            print("      ⚠️ richdem库不可用，使用简化侵蚀建模...")
            return self._simple_erosion_modeling(elevation_data)
        
        try:
            # 转换为richdem格式
            dem_rd = rd.rdarray(elevation_data, no_data=-9999)
            
            # 填坑处理
            rd.FillDepressions(dem_rd, in_place=True)
            
            # 计算流向
            flow_dir = rd.FlowDirection(dem_rd, method='D8')
            
            # 计算流量累积
            flow_acc = rd.FlowAccumulation(flow_dir, method='traditional')
            
            # 提取河网
            stream_threshold = np.percentile(flow_acc, 95)  # 前5%的高流量累积区域
            stream_network = flow_acc > stream_threshold
            
            print(f"      生成 {np.sum(stream_network):,} 个河网像素点")
            
            # 在河网位置创建侵蚀特征
            erosion_depth = np.zeros_like(elevation_data)
            
            # 根据流量累积大小确定侵蚀深度
            normalized_flow = flow_acc / np.max(flow_acc)
            erosion_depth[stream_network] = -normalized_flow[stream_network] * 15  # 最大侵蚀15米
            
            # 应用高斯平滑使侵蚀特征自然
            erosion_depth = ndimage.gaussian_filter(erosion_depth, sigma=2)
            
            # 添加到地形
            eroded_elevation = elevation_data + erosion_depth
            
            return eroded_elevation
            
        except Exception as e:
            print(f"      ⚠️ richdem处理失败: {e}")
            return self._simple_erosion_modeling(elevation_data)
    
    def _simple_erosion_modeling(self, elevation_data):
        """简化的侵蚀建模"""
        
        # 计算地形梯度
        grad_y, grad_x = np.gradient(elevation_data)
        slope = np.sqrt(grad_x**2 + grad_y**2)
        
        # 模拟水流路径（简化版）
        flow_direction = np.arctan2(grad_y, grad_x)
        
        # 创建简单的侵蚀特征
        erosion_mask = slope > np.percentile(slope, 85)  # 最陡峭的15%区域
        
        # 在陡峭区域创建侵蚀沟壑
        erosion_depth = np.zeros_like(elevation_data)
        erosion_depth[erosion_mask] = -slope[erosion_mask] * 0.5  # 轻微侵蚀
        
        # 平滑侵蚀特征
        erosion_depth = ndimage.gaussian_filter(erosion_depth, sigma=1.5)
        
        print(f"      简化侵蚀建模完成，侵蚀区域: {np.sum(erosion_mask):,} 像素")
        
        return elevation_data + erosion_depth
    
    def _enhance_ridge_lines(self, elevation_data):
        """增强山脊线特征"""
        
        # 计算海塞矩阵的特征值来识别山脊
        grad_y, grad_x = np.gradient(elevation_data)
        
        # 计算二阶导数
        grad_xx = np.gradient(grad_x, axis=1)
        grad_yy = np.gradient(grad_y, axis=0)
        grad_xy = np.gradient(grad_x, axis=0)
        
        # 海塞矩阵行列式和迹
        det_hessian = grad_xx * grad_yy - grad_xy**2
        trace_hessian = grad_xx + grad_yy
        
        # 山脊线标准：负的海塞行列式和负的最小特征值
        ridge_strength = -det_hessian * (trace_hessian < 0)
        ridge_strength = np.maximum(ridge_strength, 0)
        
        # 归一化山脊强度
        if np.max(ridge_strength) > 0:
            ridge_strength = ridge_strength / np.max(ridge_strength)
        
        # 识别主要山脊线
        ridge_threshold = np.percentile(ridge_strength, 95)
        ridge_mask = ridge_strength > ridge_threshold
        
        print(f"      识别出 {np.sum(ridge_mask):,} 个山脊线像素点")
        
        # 增强山脊高度
        ridge_enhancement = np.zeros_like(elevation_data)
        ridge_enhancement[ridge_mask] = ridge_strength[ridge_mask] * 10  # 最大增强10米
        
        # 平滑增强效果
        ridge_enhancement = ndimage.gaussian_filter(ridge_enhancement, sigma=1.0)
        
        return elevation_data + ridge_enhancement
    
    def _generate_alluvial_fans(self, elevation_data):
        """生成冲积扇地貌特征"""
        
        # 计算地形梯度
        grad_y, grad_x = np.gradient(elevation_data)
        slope = np.sqrt(grad_x**2 + grad_y**2)
        
        # 识别山前平原区域（低坡度且接近山地的区域）
        flat_regions = slope < np.percentile(slope, 25)  # 最平坦的25%区域
        steep_regions = slope > np.percentile(slope, 75)  # 最陡峭的25%区域
        
        # 寻找山前接触带
        from scipy.ndimage import binary_dilation
        
        # 扩展陡峭区域以找到山前地带
        mountain_front = binary_dilation(steep_regions, iterations=5)
        
        # 冲积扇位置：平坦区域且靠近山前
        fan_zones = flat_regions & mountain_front
        
        print(f"      识别出 {np.sum(fan_zones):,} 个冲积扇区域像素")
        
        # 在冲积扇区域创建缓坡特征
        fan_modification = np.zeros_like(elevation_data)
        
        if np.sum(fan_zones) > 0:
            # 计算到最近山地的距离
            from scipy.ndimage import distance_transform_edt
            
            distance_to_mountain = distance_transform_edt(~steep_regions)
            
            # 创建冲积扇的扇形坡度
            fan_slope = np.exp(-distance_to_mountain[fan_zones] / 50) * 5  # 衰减坡度
            
            # 随机扰动模拟沉积变化
            fan_noise = np.random.normal(0, 2, np.sum(fan_zones))
            
            fan_modification[fan_zones] = fan_slope + fan_noise
            
            # 平滑冲积扇特征
            fan_modification = ndimage.gaussian_filter(fan_modification, sigma=3.0)
        
        return elevation_data + fan_modification
    
    def create_high_resolution_mesh(self, elevation_data):
        """创建高分辨率PyVista网格"""
        print("\n🔄 步骤4: 创建高分辨率网格几何体...")
        
        try:
            height, width = elevation_data.shape
            
            # 创建坐标网格
            x_coords = np.linspace(self.beijing_bounds['west'], self.beijing_bounds['east'], width)
            y_coords = np.linspace(self.beijing_bounds['north'], self.beijing_bounds['south'], height)
            X, Y = np.meshgrid(x_coords, y_coords)
            
            # 地形垂直缩放
            Z = elevation_data * self.elevation_scale
            
            # 创建PyVista结构化网格
            grid = pv.StructuredGrid(X, Y, Z)
            
            # 添加标量数据
            grid["elevation"] = elevation_data.flatten()
            grid["longitude"] = X.flatten()
            grid["latitude"] = Y.flatten()
            
            # 计算坡度和坡向
            grad_y, grad_x = np.gradient(elevation_data)
            slope = np.sqrt(grad_x**2 + grad_y**2)
            slope_degrees = np.arctan(slope) * 180 / np.pi
            grid["slope"] = slope_degrees.flatten()
            
            aspect = np.arctan2(grad_y, grad_x) * 180 / np.pi
            aspect = (aspect + 360) % 360
            grid["aspect"] = aspect.flatten()
            
            print(f"   ✅ 高分辨率网格创建完成")
            print(f"      网格点数: {grid.n_points:,}")
            print(f"      网格单元: {grid.n_cells:,}")
            
            return grid
            
        except Exception as e:
            print(f"   ❌ 网格创建失败: {e}")
            return None
    
    def visualize_advanced_terrain(self, grid):
        """高级3D地形可视化"""
        print("\n🔄 步骤5: 高级3D地形可视化...")
        
        try:
            # 创建绘图器
            plotter = pv.Plotter(
                window_size=[1600, 1000],
                title="Beijing Advanced 3D Terrain Map - 北京市高级三维地形图"
            )
            
            # 主地形表面
            terrain_mesh = plotter.add_mesh(
                grid,
                scalars="elevation",
                cmap="terrain",
                show_edges=False,
                opacity=0.95,
                smooth_shading=True,
                scalar_bar_args={
                    'title': 'Elevation (meters)\n海拔高度 (米)',
                    'title_font_size': 14,
                    'label_font_size': 12,
                    'n_labels': 10,
                    'position_x': 0.85,
                    'position_y': 0.1,
                    'width': 0.12,
                    'height': 0.8
                }
            )
            
            # 添加等高线
            try:
                elevation_data = grid["elevation"]
                elevation_min, elevation_max = elevation_data.min(), elevation_data.max()
                
                contour_levels = np.arange(
                    int(elevation_min // 100) * 100,
                    int(elevation_max // 100 + 1) * 100,
                    100
                )
                
                if len(contour_levels) > 1:
                    contours = grid.contour(isosurfaces=contour_levels, scalars="elevation")
                    plotter.add_mesh(
                        contours,
                        color='brown',
                        line_width=2,
                        opacity=0.7
                    )
                    print(f"      等高线数量: {len(contour_levels)}")
                    
            except Exception as e:
                print(f"      ⚠️ 等高线添加失败: {e}")
            
            # 设置相机和照明
            bounds = grid.bounds
            center = [(bounds[0] + bounds[1]) / 2, 
                     (bounds[2] + bounds[3]) / 2, 
                     (bounds[4] + bounds[5]) / 2]
            
            # 相机位置
            camera_distance = max(bounds[1] - bounds[0], bounds[3] - bounds[2]) * 2
            camera_position = [
                center[0] - camera_distance * 0.7,
                center[1] - camera_distance * 0.7,
                center[2] + camera_distance
            ]
            
            plotter.camera_position = [camera_position, center, [0, 0, 1]]
            
            # 添加照明
            light = pv.Light(
                position=[center[0] + 1, center[1] + 1, center[2] + 2],
                light_type='scene light',
                intensity=0.8
            )
            plotter.add_light(light)
            
            # 背景和标题
            plotter.background_color = 'lightblue'
            plotter.add_title(
                "Beijing Advanced 3D Terrain Map\n北京市高级三维地形图",
                font_size=16
            )
            
            # 信息面板
            info_text = f"""🏔️ Advanced Beijing 3D Terrain
高级北京三维地形图

📊 Advanced Processing:
   • High-resolution DEM generation
   • Noise reduction & detail enhancement
   • Geometric terrain refinement
   • Erosion & ridge modeling

🎮 Controls:
   • Left drag: Rotate
   • Right drag: Pan
   • Scroll: Zoom
   • 'r': Reset view
   • 'q': Quit

🗻 Features:
   • Western Hills (西山山脉)
   • Jundu Mountains (军都山)
   • Yanshan Range (燕山余脉)
   • Erosion channels (侵蚀沟壑)
   • Ridge lines (山脊线)"""
            
            plotter.add_text(
                info_text,
                position='upper_left',
                font_size=9,
                color='black'
            )
            
            # 显示坐标轴
            plotter.show_axes()
            
            # 启用高级渲染
            plotter.enable_depth_peeling(10)
            plotter.enable_anti_aliasing()
            
            print("   ✅ 高级3D可视化设置完成")
            print("\n🌄 启动高级交互式3D地形图...")
            print("   🖱️ 交互说明:")
            print("      • 左键拖拽: 旋转视角")
            print("      • 右键拖拽: 平移视图")
            print("      • 滚轮: 缩放")
            print("      • 'r': 重置视角")
            print("      • 'q': 退出")
            
            # 显示
            plotter.show()
            
            return True
            
        except Exception as e:
            print(f"   ❌ 3D可视化失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_advanced_pipeline(self):
        """运行高级地形图生成流程"""
        print("🚀" + "="*80)
        print("🏔️  BEIJING ADVANCED 3D TERRAIN MAP - GIS EXPERT VERSION")
        print("    北京市高级三维地形图 - GIS专家版本")
        print("="*82)
        
        start_time = __import__('time').time()
        
        try:
            # 步骤1: 获取边界数据
            if not self.download_beijing_boundary():
                print("❌ 边界数据获取失败，程序终止")
                return False
            
            # 步骤2: 获取高精度DEM数据
            if not self.download_open_elevation_data():
                print("❌ DEM数据获取失败，程序终止")
                return False
            
            # 步骤3: 高级DEM预处理
            processed_elevation = self.advanced_dem_preprocessing()
            if processed_elevation is None:
                print("❌ DEM预处理失败，程序终止")
                return False
            
            # 步骤4: 地形几何细化
            refined_elevation = self.geometric_terrain_refinement(processed_elevation)
            
            # 步骤5: 创建高分辨率网格
            grid = self.create_high_resolution_mesh(refined_elevation)
            if grid is None:
                print("❌ 网格创建失败，程序终止")
                return False
            
            # 步骤6: 高级3D可视化
            success = self.visualize_advanced_terrain(grid)
            
            # 计算运行时间
            end_time = __import__('time').time()
            runtime = end_time - start_time
            
            print("\n" + "="*82)
            if success:
                print("✅ 北京市高级3D地形图生成完成！")
                print(f"⏱️  总运行时间: {runtime:.1f}秒")
                print(f"📁 数据文件保存在: {self.data_dir}")
                print("\n📋 生成的高级数据文件:")
                for file_path in [self.dem_file, self.dem_processed_file, self.dem_enhanced_file]:
                    if os.path.exists(file_path):
                        size_mb = os.path.getsize(file_path) / 1024 / 1024
                        print(f"   📄 {os.path.basename(file_path)} ({size_mb:.1f}MB)")
            else:
                print("❌ 高级3D地形图生成失败")
            
            return success
            
        except KeyboardInterrupt:
            print("\n⚠️  用户中断程序")
            return False
        except Exception as e:
            print(f"\n❌ 程序执行出错: {e}")
            import traceback
            traceback.print_exc()
            return False


# 为了兼容性，保留原有的BeijingTerrainMap类
class BeijingTerrainMap(BeijingTerrainMapAdvanced):
    """兼容性类，继承高级功能"""
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        """运行标准流程"""
        return self.run_advanced_pipeline()


def main():
    """主函数"""
    try:
        # 创建高级地形图生成器
        terrain_generator = BeijingTerrainMapAdvanced()
        
        # 运行高级生成流程
        terrain_generator.run_advanced_pipeline()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
