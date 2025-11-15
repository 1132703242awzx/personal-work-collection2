# 聚氨酯分子结构绘制程序使用说明

## 📋 程序概述

本程序使用专业的化学信息学库 RDKit 来绘制聚氨酯（Polyurethane）的分子结构式。程序提供了多种不同类型的聚氨酯结构，包括基于不同原料组合的重复单元和片段。

## 🛠️ 环境要求

### Python版本
- Python 3.7 或更高版本

### 必需的库
```bash
# 核心化学信息学库
pip install rdkit-pypi

# 图像处理和可视化
pip install matplotlib pillow

# 数值计算（注意版本兼容性）
pip install "numpy<2"
```

## 📁 文件结构

项目包含以下主要文件：

1. **`聚氨酯.py`** - 原始完整版本
2. **`聚氨酯_简化版.py`** - 简化版本，更稳定
3. **`聚氨酯_完整版.py`** - 最终完整版本，功能最全面

## 🚀 运行程序

### 方法1：直接运行完整版（推荐）
```bash
python 聚氨酯_完整版.py
```

### 方法2：运行简化版
```bash
python 聚氨酯_简化版.py
```

## 📊 程序功能

### 核心功能
1. **分子结构创建** - 从SMILES字符串创建分子对象
2. **结构优化** - 生成2D坐标，优化分子布局
3. **特征分析** - 分析氨基甲酸酯官能团、芳香环等
4. **高质量绘图** - 生成清晰的分子结构图
5. **批量处理** - 一次性处理多种聚氨酯类型
6. **文件保存** - 自动保存PNG格式的图像文件

### 支持的聚氨酯类型

| 类型 | 原料组合 | 应用领域 |
|------|----------|----------|
| TDI_Ethylene_Glycol | TDI + 乙二醇 | 软质泡沫、弹性体 |
| Basic_Urethane | 丁醇 + 苯胺 + 光气 | 涂料、胶粘剂 |
| HDI_Butanediol | HDI + 1,4-丁二醇 | 高性能涂料、弹性体 |
| Simple_Repeat_Unit | 甲苯二异氰酸酯 + 多元醇 | 通用聚氨酯材料 |
| MDI_Ethylene_Glycol | MDI + 乙二醇 | 硬质泡沫、合成革 |
| Polyether_PU | TDI + 聚醚多元醇 | 软质泡沫、弹性体 |

## 📈 输出结果

### 控制台输出
- ✅ 库导入状态检查
- 📍 分子创建过程信息
- 🔍 详细的结构特征分析
- 💾 文件保存状态
- 📊 最终处理结果总结

### 生成的文件
程序会在当前目录生成以下PNG图像文件：
- `polyurethane_TDI_Ethylene_Glycol.png`
- `polyurethane_Basic_Urethane.png`
- `polyurethane_HDI_Butanediol.png`
- `polyurethane_Simple_Repeat_Unit.png`
- `polyurethane_MDI_Ethylene_Glycol.png`
- `polyurethane_Polyether_PU.png`

### 图形显示
- 📱 单个分子结构的详细视图
- 📋 包含分子信息的说明面板
- 🖼️ 所有结构的汇总视图

## 🔧 常见问题解决

### 问题1：RDKit导入失败
```bash
# 解决方案
pip install rdkit-pypi

# 如果仍有问题，尝试conda安装
conda install -c conda-forge rdkit
```

### 问题2：NumPy版本冲突
```bash
# 错误信息：AttributeError: _ARRAY_API not found
# 解决方案：降级NumPy
pip install "numpy<2"
```

### 问题3：中文字体显示问题
程序已内置中文字体支持，如果仍有问题：
- Windows：确保系统有SimHei或Microsoft YaHei字体
- 其他系统：安装中文字体包

### 问题4：图像显示问题
如果matplotlib无法显示图形：
```bash
# 安装tkinter支持
sudo apt-get install python3-tk  # Ubuntu/Debian
# 或
yum install tkinter  # CentOS/RHEL
```

## 📚 聚氨酯基础知识

### 什么是聚氨酯？
聚氨酯是一类重要的聚合物材料，通过二异氰酸酯与多元醇的聚加成反应制得。

### 特征官能团
氨基甲酸酯键 (-NH-CO-O-) 是聚氨酯的特征官能团。

### 主要原料
- **二异氰酸酯**：TDI（甲苯二异氰酸酯）、MDI（二苯基甲烷二异氰酸酯）、HDI（六亚甲基二异氰酸酯）
- **多元醇**：聚醚多元醇、聚酯多元醇、短链醇等

### 应用领域
- 泡沫塑料（软泡、硬泡）
- 弹性体和橡胶
- 涂料和胶粘剂
- 合成革和纤维
- 密封剂和弹性密封材料

## 🎯 程序特色

1. **专业性** - 使用行业标准的RDKit库
2. **教育性** - 提供详细的化学结构分析
3. **实用性** - 生成高质量的可发表图像
4. **完整性** - 覆盖多种典型聚氨酯类型
5. **用户友好** - 清晰的输出和错误处理

## 👨‍💻 技术细节

### SMILES字符串设计
程序中的SMILES字符串都经过精心设计，准确表示了聚氨酯的化学结构：
- 包含氨基甲酸酯官能团
- 反映真实的化学键连接
- 适合2D可视化展示

### 分子优化
- 自动添加氢原子
- 生成合理的2D坐标
- 优化分子布局以提高可读性

### 图像质量
- 高分辨率输出（1000x800像素）
- 清晰的原子标记和键连接
- 专业的化学结构绘图风格

---

📧 如有问题或建议，请联系开发者。

🎉 祝您使用愉快！
