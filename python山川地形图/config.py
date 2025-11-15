# 北京3D地形图项目配置文件

# 北京市地理边界（经纬度）
BEIJING_BOUNDS = {
    "west": 115.4,   # 西经
    "east": 117.5,   # 东经  
    "south": 39.4,   # 南纬
    "north": 41.1    # 北纬
}

# 主要地标坐标
LANDMARKS = {
    "天安门": {"lon": 116.3974, "lat": 39.9093},
    "西山": {"lon": 116.1, "lat": 40.1},
    "军都山": {"lon": 116.3, "lat": 40.3},
    "香山": {"lon": 116.1889, "lat": 39.9956},
    "八达岭": {"lon": 116.0176, "lat": 40.3598}
}

# 可视化设置
VISUALIZATION_CONFIG = {
    "window_size": [1200, 800],
    "elevation_scale": 0.01,
    "colormap": "gist_earth",
    "background_color": "lightblue"
}

# 数据源URL
DATA_SOURCES = {
    "beijing_boundary": "https://hjwhwang.github.io/geoJson-Data/beijing.json",
    "backup_boundary": "https://raw.githubusercontent.com/hxkj/china-administrative-division/master/dist/city/110000.json"
}
