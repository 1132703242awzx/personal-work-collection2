"""
聚氨酯分子结构绘制程序 - 简化版
使用RDKit库绘制聚氨酯的二维分子结构式

作者: Claude AI
日期: 2025年8月29日
"""

# ============================================================================
# 第一部分：安装与导入
# ============================================================================

# 请先安装RDKit库：
# pip install rdkit-pypi
# 注意：如果遇到NumPy版本问题，请运行：
# pip install "numpy<2"

import sys
import os

def check_and_import_libraries():
    """检查并导入必要的库"""
    try:
        from rdkit import Chem
        from rdkit.Chem import Draw
        from rdkit.Chem import AllChem
        import matplotlib.pyplot as plt
        from PIL import Image
        print("✓ 所有必要库导入成功")
        return True, Chem, Draw, AllChem, plt, Image
    except ImportError as e:
        print(f"❌ 导入库时出错: {e}")
        print("\n请按以下步骤安装依赖：")
        print("1. pip install rdkit-pypi")
        print("2. pip install matplotlib pillow")
        print("3. pip install \"numpy<2\"  # 如果有NumPy版本冲突")
        return False, None, None, None, None, None

# ============================================================================
# 第二部分：定义分子结构
# ============================================================================

def create_polyurethane_smiles():
    """
    创建聚氨酯分子的SMILES字符串集合
    返回包含不同聚氨酯结构的字典
    """
    
    polyurethane_smiles = {
        # 1. 基于甲苯二异氰酸酯(TDI)和乙二醇的简化聚氨酯重复单元
        "TDI_EG_simple": "Cc1ccc(NC(=O)OCCOC(=O)Nc2ccc(C)cc2)cc1",
        
        # 2. 氨基甲酸酯基本官能团示例
        "urethane_basic": "CCCCOC(=O)Nc1ccccc1",
        
        # 3. 基于六亚甲基二异氰酸酯(HDI)和1,4-丁二醇的片段
        "HDI_BDO_fragment": "O=C(NCCCCCCNC(=O)OCCCCOC(=O)NCCCCCCN)OCCCC",
        
        # 4. 简化的聚氨酯重复单元（最清晰的结构）
        "simple_repeat": "CCCCOC(=O)Nc1ccc(C)cc1NC(=O)OCCC",
        
        # 5. 二苯基甲烷二异氰酸酯(MDI)基聚氨酯片段
        "MDI_fragment": "O=C(Nc1ccc(Cc2ccc(NC(=O)OCCO)cc2)cc1)OCCO"
    }
    
    return polyurethane_smiles

def create_molecule_from_smiles(smiles, name, Chem, AllChem):
    """
    从SMILES字符串创建并优化分子对象
    
    参数:
        smiles: SMILES字符串
        name: 分子名称
        Chem: RDKit Chem模块
        AllChem: RDKit AllChem模块
    
    返回:
        mol: 优化后的RDKit分子对象
    """
    print(f"\n正在处理: {name}")
    print(f"SMILES: {smiles}")
    
    # 从SMILES字符串创建分子对象
    mol = Chem.MolFromSmiles(smiles)
    
    if mol is None:
        print(f"❌ 无法创建分子: {name}")
        return None
    
    # 添加氢原子以获得完整结构
    mol_with_h = Chem.AddHs(mol)
    
    # 生成2D坐标
    AllChem.Compute2DCoords(mol_with_h)
    
    print(f"✓ 成功创建分子: {name}")
    print(f"  - 分子式: {Chem.rdMolDescriptors.CalcMolFormula(mol_with_h)}")
    print(f"  - 分子量: {Chem.rdMolDescriptors.CalcExactMolWt(mol_with_h):.2f}")
    print(f"  - 原子数: {mol_with_h.GetNumAtoms()}")
    print(f"  - 键数: {mol_with_h.GetNumBonds()}")
    
    return mol_with_h

# ============================================================================
# 第三部分：分析分子结构特征
# ============================================================================

def analyze_polyurethane_features(mol, name, Chem):
    """
    分析聚氨酯分子的化学特征
    
    参数:
        mol: RDKit分子对象
        name: 分子名称
        Chem: RDKit Chem模块
    """
    if mol is None:
        return
    
    print(f"\n=== {name} 结构特征分析 ===")
    
    # 查找氨基甲酸酯官能团 (-NH-CO-O-)
    urethane_pattern = Chem.MolFromSmarts("[NX3][CX3](=[OX1])[OX2]")
    urethane_matches = mol.GetSubstructMatches(urethane_pattern)
    print(f"氨基甲酸酯官能团 (-NH-CO-O-) 数量: {len(urethane_matches)}")
    
    # 查找芳香环
    aromatic_rings = Chem.rdMolDescriptors.CalcNumAromaticRings(mol)
    print(f"芳香环数量: {aromatic_rings}")
    
    # 查找脂肪链
    aliphatic_rings = Chem.rdMolDescriptors.CalcNumAliphaticRings(mol)
    print(f"脂肪环数量: {aliphatic_rings}")
    
    # 计算其他描述符
    hbd = Chem.rdMolDescriptors.CalcNumHBD(mol)  # 氢键供体
    hba = Chem.rdMolDescriptors.CalcNumHBA(mol)  # 氢键受体
    print(f"氢键供体数: {hbd}")
    print(f"氢键受体数: {hba}")

# ============================================================================
# 第四部分：绘制与保存分子
# ============================================================================

def draw_and_save_molecule(mol, name, Draw, plt, size=(800, 600)):
    """
    绘制分子结构并保存为图片
    
    参数:
        mol: RDKit分子对象
        name: 分子名称
        Draw: RDKit Draw模块
        plt: matplotlib.pyplot
        size: 图像尺寸
    
    返回:
        成功绘制则返回True，否则返回False
    """
    if mol is None:
        return False
    
    try:
        # 使用RDKit绘制分子
        img = Draw.MolToImage(mol, size=size, kekulize=True)
        
        # 保存为PNG文件
        filename = f"polyurethane_{name}.png"
        img.save(filename)
        print(f"✓ 已保存图像: {filename}")
        
        # 使用matplotlib显示
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        plt.title(f"聚氨酯分子结构: {name}", fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        # 添加说明文字
        description = f"特征官能团：氨基甲酸酯（-NH-CO-O-）\n文件名：{filename}"
        plt.figtext(0.5, 0.02, description, ha='center', fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return True
        
    except Exception as e:
        print(f"❌ 绘制分子 {name} 时出错: {e}")
        return False

# ============================================================================
# 第五部分：主程序
# ============================================================================

def main():
    """主程序入口"""
    print("=" * 80)
    print("聚氨酯分子结构绘制程序".center(80))
    print("使用RDKit库绘制聚氨酯的二维分子结构式".center(80))
    print("=" * 80)
    
    # 检查并导入库
    success, Chem, Draw, AllChem, plt, Image = check_and_import_libraries()
    if not success:
        return
    
    # 获取聚氨酯SMILES定义
    pu_smiles = create_polyurethane_smiles()
    
    print(f"\n准备绘制 {len(pu_smiles)} 种聚氨酯分子结构")
    
    successful_drawings = 0
    
    # 处理每种聚氨酯结构
    for structure_name, smiles in pu_smiles.items():
        print("\n" + "=" * 60)
        
        # 创建分子对象
        mol = create_molecule_from_smiles(smiles, structure_name, Chem, AllChem)
        
        if mol is None:
            continue
        
        # 分析分子特征
        analyze_polyurethane_features(mol, structure_name, Chem)
        
        # 绘制并保存分子
        if draw_and_save_molecule(mol, structure_name, Draw, plt):
            successful_drawings += 1
        
        print("-" * 60)
    
    # 总结
    print("\n" + "=" * 80)
    print(f"程序执行完成！")
    print(f"成功绘制了 {successful_drawings}/{len(pu_smiles)} 个分子结构")
    print(f"所有图像文件已保存在当前目录：{os.getcwd()}")
    print("=" * 80)
    
    # 列出生成的文件
    png_files = [f for f in os.listdir('.') if f.startswith('polyurethane_') and f.endswith('.png')]
    if png_files:
        print("\n生成的图像文件：")
        for file in png_files:
            print(f"  📁 {file}")

def display_polyurethane_info():
    """显示聚氨酯相关信息"""
    info = """
    聚氨酯(Polyurethane)基本信息：
    
    🧪 化学组成：
    - 主要由二异氰酸酯和多元醇反应形成
    - 特征官能团：氨基甲酸酯键 (-NH-CO-O-)
    
    🔗 常见原料：
    - 二异氰酸酯：TDI(甲苯二异氰酸酯)、MDI(二苯基甲烷二异氰酸酯)、HDI(六亚甲基二异氰酸酯)
    - 多元醇：聚醚多元醇、聚酯多元醇、乙二醇、1,4-丁二醇等
    
    📊 应用领域：
    - 泡沫材料、弹性体、涂料、胶粘剂、合成革等
    """
    print(info)

if __name__ == "__main__":
    try:
        display_polyurethane_info()
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        print("\n💡 解决建议：")
        print("1. 确保已安装RDKit：pip install rdkit-pypi")
        print("2. 检查NumPy版本：pip install \"numpy<2\"")
        print("3. 确保已安装其他依赖：pip install matplotlib pillow")
