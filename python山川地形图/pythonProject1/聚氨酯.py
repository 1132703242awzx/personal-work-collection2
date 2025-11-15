"""
聚氨酯分子结构绘制程序
使用RDKit库绘制聚氨酯的二维分子结构式

作者: Claude AI
日期: 2025年8月29日
"""

# ============================================================================
# 第一部分：安装与导入
# ============================================================================

# 请先安装RDKit库：
# pip install rdkit-pypi
# 如果上述命令失败，可以尝试：
# conda install -c conda-forge rdkit

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdMolDraw2D
from rdkit.Chem import AllChem
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import os
import sys

def check_rdkit_installation():
    """检查RDKit是否正确安装"""
    try:
        from rdkit import Chem
        print("✓ RDKit库已成功导入")
        return True
    except ImportError:
        print("❌ RDKit库未安装！")
        print("请运行以下命令安装：")
        print("pip install rdkit-pypi")
        print("或者：")
        print("conda install -c conda-forge rdkit")
        return False

# ============================================================================
# 第二部分：定义分子结构
# ============================================================================

def create_polyurethane_structures():
    """
    创建不同类型的聚氨酯分子结构
    返回包含多种聚氨酯结构的字典
    """
    
    # 定义不同的聚氨酯SMILES字符串
    polyurethane_smiles = {
        # 基于甲苯二异氰酸酯(TDI)和1,4-丁二醇(BDO)的聚氨酯重复单元
        "TDI_BDO_repeat": "O=C(NCCCCOC(=O)Nc1ccc(C)cc1)Nc1ccc(C)cc1",
        
        # 基于二苯基甲烷二异氰酸酯(MDI)和乙二醇的聚氨酯重复单元
        "MDI_EG_repeat": "O=C(NCCOC(=O)Nc1ccc(Cc2ccc(NC(=O)O)cc2)cc1)Nc1ccc(Cc2ccc(N)cc2)cc1",
        
        # 简化的聚氨酯重复单元（更清晰的结构）
        "simple_repeat": "CCCCOC(=O)Nc1ccc(C)cc1NC(=O)OCCCC",
        
        # 氨基甲酸酯基本官能团
        "urethane_group": "CCOC(=O)Nc1ccccc1",
        
        # 基于六亚甲基二异氰酸酯(HDI)和1,4-丁二醇的聚氨酯
        "HDI_BDO": "O=C(NCCCCCCNC(=O)OCCCCOC(=O)NCCCCCCN)OCCCCOC(=O)NCCCCCCNC(=O)O"
    }
    
    return polyurethane_smiles

def create_molecule_from_smiles(smiles, name):
    """
    从SMILES字符串创建分子对象
    
    参数:
        smiles: SMILES字符串
        name: 分子名称
    
    返回:
        mol: RDKit分子对象
    """
    print(f"\n正在创建分子: {name}")
    print(f"SMILES: {smiles}")
    
    # 从SMILES字符串创建分子对象
    mol = Chem.MolFromSmiles(smiles)
    
    if mol is None:
        print(f"❌ 无法从SMILES创建分子: {name}")
        return None
    
    # 添加氢原子（可选，使结构更完整）
    mol_with_h = Chem.AddHs(mol)
    
    # 生成2D坐标，确保分子布局合理
    AllChem.Compute2DCoords(mol_with_h)
    
    print(f"✓ 成功创建分子: {name}")
    print(f"  - 原子数: {mol_with_h.GetNumAtoms()}")
    print(f"  - 键数: {mol_with_h.GetNumBonds()}")
    
    return mol_with_h

# ============================================================================
# 第三部分：生成与调整分子对象
# ============================================================================

def optimize_molecule_2d(mol):
    """
    优化分子的2D布局
    
    参数:
        mol: RDKit分子对象
    
    返回:
        优化后的分子对象
    """
    if mol is None:
        return None
    
    # 生成更好的2D坐标
    AllChem.Compute2DCoords(mol)
    
    # 可选：使用力场优化2D结构（如果需要更精细的布局）
    try:
        AllChem.MMFFOptimizeMolecule(mol, confId=0)
    except:
        pass  # 如果优化失败，继续使用基本坐标
    
    return mol

# ============================================================================
# 第四部分：绘制与显示分子
# ============================================================================

def draw_molecule_high_quality(mol, name, size=(800, 600)):
    """
    使用高质量设置绘制分子
    
    参数:
        mol: RDKit分子对象
        name: 分子名称
        size: 图像尺寸 (width, height)
    
    返回:
        图像对象
    """
    if mol is None:
        return None
    
    # 创建高质量的2D绘图对象
    drawer = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
    
    # 设置绘图选项
    opts = drawer.drawOptions()
    opts.bondLineWidth = 2
    opts.atomLabelFontSize = 14
    opts.bondLineWidth = 3
    opts.highlightBondWidthMultiplier = 8
    
    # 绘制分子
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    
    # 获取PNG格式的图像数据
    img_data = drawer.GetDrawingText()
    
    # 保存为PNG文件
    filename = f"{name}_structure.png"
    with open(filename, 'wb') as f:
        f.write(img_data)
    
    print(f"✓ 已保存高质量图像: {filename}")
    
    return filename

def draw_molecule_simple(mol, name, size=(800, 600)):
    """
    使用简单方法绘制分子
    
    参数:
        mol: RDKit分子对象
        name: 分子名称
        size: 图像尺寸
    
    返回:
        PIL图像对象
    """
    if mol is None:
        return None
    
    # 使用RDKit的基本绘图功能
    img = Draw.MolToImage(mol, size=size, kekulize=True)
    
    # 保存图像
    filename = f"{name}_simple.png"
    img.save(filename)
    
    print(f"✓ 已保存简单图像: {filename}")
    
    return img

def display_molecule_with_matplotlib(image_path, title):
    """
    使用matplotlib显示分子图像
    
    参数:
        image_path: 图像文件路径
        title: 图像标题
    """
    try:
        # 读取图像
        img = mpimg.imread(image_path)
        
        # 创建图形
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        plt.title(f"聚氨酯分子结构: {title}", fontsize=16, fontweight='bold')
        plt.axis('off')  # 不显示坐标轴
        
        # 添加说明文字
        plt.figtext(0.5, 0.02, 
                   "聚氨酯特征官能团：氨基甲酸酯（-NH-CO-O-）", 
                   ha='center', fontsize=12)
        
        plt.tight_layout()
        plt.show()
        
        print(f"✓ 已显示分子结构: {title}")
        
    except Exception as e:
        print(f"❌ 显示图像时出错: {e}")

# ============================================================================
# 第五部分：主程序与注释说明
# ============================================================================

def analyze_polyurethane_structure(mol, name):
    """
    分析聚氨酯分子结构的化学特征
    
    参数:
        mol: RDKit分子对象
        name: 分子名称
    """
    if mol is None:
        return
    
    print(f"\n=== {name} 结构分析 ===")
    
    # 基本信息
    print(f"分子式: {Chem.rdMolDescriptors.CalcMolFormula(mol)}")
    print(f"分子量: {Chem.rdMolDescriptors.CalcExactMolWt(mol):.2f}")
    print(f"原子数: {mol.GetNumAtoms()}")
    print(f"键数: {mol.GetNumBonds()}")
    
    # 查找氨基甲酸酯官能团
    urethane_pattern = Chem.MolFromSmarts("[NX3][CX3](=[OX1])[OX2]")
    if urethane_pattern:
        matches = mol.GetSubstructMatches(urethane_pattern)
        print(f"氨基甲酸酯官能团数量: {len(matches)}")
    
    # 查找芳香环
    aromatic_rings = Chem.rdMolDescriptors.CalcNumAromaticRings(mol)
    print(f"芳香环数量: {aromatic_rings}")

def main():
    """主程序"""
    print("=" * 70)
    print("聚氨酯分子结构绘制程序".center(70))
    print("=" * 70)
    
    # 检查RDKit安装
    if not check_rdkit_installation():
        return
    
    # 获取聚氨酯结构定义
    pu_structures = create_polyurethane_structures()
    
    print(f"\n共找到 {len(pu_structures)} 种聚氨酯结构类型")
    
    # 遍历每种结构类型
    for structure_name, smiles in pu_structures.items():
        print("\n" + "=" * 50)
        
        # 创建分子对象
        mol = create_molecule_from_smiles(smiles, structure_name)
        
        if mol is None:
            continue
        
        # 优化分子2D布局
        mol = optimize_molecule_2d(mol)
        
        # 分析分子结构
        analyze_polyurethane_structure(mol, structure_name)
        
        # 绘制高质量图像
        try:
            img_path = draw_molecule_high_quality(mol, structure_name)
            if img_path and os.path.exists(img_path):
                # 显示图像
                display_molecule_with_matplotlib(img_path, structure_name)
        except Exception as e:
            print(f"高质量绘图失败，尝试简单绘图: {e}")
            
            # 备选：使用简单绘图方法
            try:
                img = draw_molecule_simple(mol, structure_name)
                if img:
                    img.show()  # 直接显示PIL图像
            except Exception as e2:
                print(f"❌ 绘图完全失败: {e2}")
        
        # 添加分隔符，便于观察
        print("\n" + "-" * 50)
    
    print("\n" + "=" * 70)
    print("程序执行完成！")
    print("所有生成的图像文件已保存在当前目录中。")
    print("=" * 70)

# 程序入口点
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        print("请检查RDKit是否正确安装，或联系开发者获取帮助。")
