"""
聚氨酯分子结构绘制程序 - 完整版
使用RDKit库绘制聚氨酯的二维分子结构式

功能特点：
- 支持多种聚氨酯类型的结构绘制
- 详细的分子结构分析
- 高质量图像输出
- 支持批量处理和保存
- 完整的错误处理和用户友好提示

作者: Claude AI
日期: 2025年8月29日
"""

# ============================================================================
# 第一部分：安装与导入
# ============================================================================

# 安装命令（请在命令行中运行）：
# pip install rdkit-pypi matplotlib pillow
# 如果遇到NumPy版本冲突：pip install "numpy<2"

import sys
import os
import warnings
warnings.filterwarnings('ignore')  # 忽略警告信息

def setup_chinese_font():
    """设置中文字体支持"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        
        # 尝试设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        return True
    except:
        return False

def check_and_import_libraries():
    """检查并导入必要的库"""
    required_modules = {
        'rdkit': ['Chem', 'Draw', 'AllChem'],
        'matplotlib': ['pyplot'],
        'PIL': ['Image']
    }
    
    try:
        from rdkit import Chem
        from rdkit.Chem import Draw
        from rdkit.Chem import AllChem
        from rdkit.Chem import rdMolDescriptors
        import matplotlib.pyplot as plt
        from PIL import Image
        import numpy as np
        
        print("✓ 所有必要库导入成功")
        setup_chinese_font()
        
        return True, {
            'Chem': Chem,
            'Draw': Draw, 
            'AllChem': AllChem,
            'rdMolDescriptors': rdMolDescriptors,
            'plt': plt,
            'Image': Image,
            'np': np
        }
    except ImportError as e:
        print(f"❌ 导入库时出错: {e}")
        print("\n📋 安装指南：")
        print("1. pip install rdkit-pypi")
        print("2. pip install matplotlib pillow")
        print("3. pip install \"numpy<2\"  # 解决版本冲突")
        return False, {}

# ============================================================================
# 第二部分：聚氨酯分子结构定义
# ============================================================================

class PolyurethaneStructures:
    """聚氨酯分子结构定义类"""
    
    @staticmethod
    def get_all_structures():
        """获取所有聚氨酯结构的SMILES定义"""
        return {
            # 1. 甲苯二异氰酸酯(TDI) + 乙二醇 聚氨酯
            "TDI_Ethylene_Glycol": {
                "smiles": "Cc1ccc(NC(=O)OCCOC(=O)Nc2ccc(C)cc2)cc1",
                "description": "基于甲苯二异氰酸酯(TDI)和乙二醇的聚氨酯重复单元",
                "raw_materials": "TDI + 乙二醇",
                "applications": "软质泡沫、弹性体"
            },
            
            # 2. 基础氨基甲酸酯官能团
            "Basic_Urethane": {
                "smiles": "CCCCOC(=O)Nc1ccccc1",
                "description": "基本的氨基甲酸酯结构单元",
                "raw_materials": "丁醇 + 苯胺 + 光气",
                "applications": "涂料、胶粘剂"
            },
            
            # 3. 六亚甲基二异氰酸酯(HDI) + 1,4-丁二醇
            "HDI_Butanediol": {
                "smiles": "O=C(NCCCCCCNC(=O)OCCCCOC(=O)NCCCCCCN)OCCCC",
                "description": "基于六亚甲基二异氰酸酯(HDI)和1,4-丁二醇的聚氨酯片段",
                "raw_materials": "HDI + 1,4-丁二醇",
                "applications": "高性能涂料、弹性体"
            },
            
            # 4. 简化聚氨酯重复单元
            "Simple_Repeat_Unit": {
                "smiles": "CCCCOC(=O)Nc1ccc(C)cc1NC(=O)OCCC",
                "description": "简化的聚氨酯重复单元结构",
                "raw_materials": "甲苯二异氰酸酯 + 多元醇",
                "applications": "通用聚氨酯材料"
            },
            
            # 5. 二苯基甲烷二异氰酸酯(MDI) + 乙二醇
            "MDI_Ethylene_Glycol": {
                "smiles": "O=C(Nc1ccc(Cc2ccc(NC(=O)OCCO)cc2)cc1)OCCO",
                "description": "基于二苯基甲烷二异氰酸酯(MDI)和乙二醇的聚氨酯片段",
                "raw_materials": "MDI + 乙二醇",
                "applications": "硬质泡沫、合成革"
            },
            
            # 6. 聚醚型聚氨酯片段
            "Polyether_PU": {
                "smiles": "CCCCOCCCOC(=O)Nc1ccc(C)cc1NC(=O)OCCCOCCCC",
                "description": "聚醚型聚氨酯结构片段",
                "raw_materials": "TDI + 聚醚多元醇",
                "applications": "软质泡沫、弹性体"
            }
        }

# ============================================================================
# 第三部分：分子对象创建与优化
# ============================================================================

class MoleculeProcessor:
    """分子处理类"""
    
    def __init__(self, modules):
        self.Chem = modules['Chem']
        self.AllChem = modules['AllChem']
        self.rdMolDescriptors = modules['rdMolDescriptors']
    
    def create_molecule(self, smiles, name):
        """从SMILES字符串创建分子对象"""
        print(f"\n📍 正在处理: {name}")
        print(f"   SMILES: {smiles}")
        
        # 创建分子对象
        mol = self.Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"❌ 无法创建分子: {name}")
            return None
        
        # 添加氢原子
        mol_with_h = self.Chem.AddHs(mol)
        
        # 生成2D坐标
        self.AllChem.Compute2DCoords(mol_with_h)
        
        # 显示基本信息
        formula = self.rdMolDescriptors.CalcMolFormula(mol_with_h)
        mol_weight = self.rdMolDescriptors.CalcExactMolWt(mol_with_h)
        
        print(f"✓ 成功创建分子: {name}")
        print(f"   分子式: {formula}")
        print(f"   分子量: {mol_weight:.2f}")
        print(f"   原子数: {mol_with_h.GetNumAtoms()}")
        print(f"   键数: {mol_with_h.GetNumBonds()}")
        
        return mol_with_h
    
    def analyze_molecule(self, mol, name, structure_info):
        """分析分子的化学特征"""
        if mol is None:
            return {}
        
        print(f"\n🔍 {name} 结构特征分析")
        print(f"   描述: {structure_info.get('description', 'N/A')}")
        print(f"   原料: {structure_info.get('raw_materials', 'N/A')}")
        print(f"   应用: {structure_info.get('applications', 'N/A')}")
        
        # 分析官能团
        analysis = {}
        
        # 氨基甲酸酯官能团
        urethane_pattern = self.Chem.MolFromSmarts("[NX3][CX3](=[OX1])[OX2]")
        urethane_matches = mol.GetSubstructMatches(urethane_pattern)
        analysis['urethane_groups'] = len(urethane_matches)
        
        # 芳香环
        analysis['aromatic_rings'] = self.rdMolDescriptors.CalcNumAromaticRings(mol)
        
        # 脂肪环
        analysis['aliphatic_rings'] = self.rdMolDescriptors.CalcNumAliphaticRings(mol)
        
        # 氢键
        analysis['hbd'] = self.rdMolDescriptors.CalcNumHBD(mol)  # 氢键供体
        analysis['hba'] = self.rdMolDescriptors.CalcNumHBA(mol)  # 氢键受体
        
        # 旋转键
        analysis['rotatable_bonds'] = self.rdMolDescriptors.CalcNumRotatableBonds(mol)
        
        # 显示分析结果
        print(f"   🔗 氨基甲酸酯官能团: {analysis['urethane_groups']} 个")
        print(f"   🔺 芳香环: {analysis['aromatic_rings']} 个")
        print(f"   ⭕ 脂肪环: {analysis['aliphatic_rings']} 个")
        print(f"   🔸 氢键供体: {analysis['hbd']} 个")
        print(f"   🔹 氢键受体: {analysis['hba']} 个")
        print(f"   🔄 可旋转键: {analysis['rotatable_bonds']} 个")
        
        return analysis

# ============================================================================
# 第四部分：分子结构绘制与可视化
# ============================================================================

class MoleculeVisualizer:
    """分子可视化类"""
    
    def __init__(self, modules):
        self.Draw = modules['Draw']
        self.plt = modules['plt']
        self.Image = modules['Image']
        self.np = modules['np']
    
    def draw_molecule(self, mol, name, structure_info, size=(1000, 800)):
        """绘制分子结构图"""
        if mol is None:
            return False
        
        try:
            # 生成分子图像
            img = self.Draw.MolToImage(mol, size=size, kekulize=True)
            
            # 保存PNG文件
            filename = f"polyurethane_{name}.png"
            img.save(filename)
            print(f"💾 已保存图像: {filename}")
            
            # 创建带详细信息的图形
            self._create_detailed_figure(img, name, structure_info, filename)
            
            return True
            
        except Exception as e:
            print(f"❌ 绘制分子 {name} 时出错: {e}")
            return False
    
    def _create_detailed_figure(self, img, name, structure_info, filename):
        """创建带详细信息的图形"""
        fig, (ax1, ax2) = self.plt.subplots(1, 2, figsize=(16, 8), 
                                           gridspec_kw={'width_ratios': [2, 1]})
        
        # 左侧：分子结构图
        ax1.imshow(img)
        ax1.set_title(f"Polyurethane Structure: {name}", fontsize=16, fontweight='bold', pad=20)
        ax1.axis('off')
        
        # 右侧：详细信息
        info_text = f"""
Structure Information:

Name: {name}

Description:
{structure_info.get('description', 'N/A')}

Raw Materials:
{structure_info.get('raw_materials', 'N/A')}

Applications:
{structure_info.get('applications', 'N/A')}

Key Features:
• Urethane linkage (-NH-CO-O-)
• Formed by polyaddition reaction
• Versatile properties based on components

File: {filename}
        """
        
        ax2.text(0.05, 0.95, info_text, transform=ax2.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", 
                facecolor="lightblue", alpha=0.8))
        ax2.axis('off')
        
        self.plt.tight_layout()
        self.plt.show()
    
    def create_summary_figure(self, successful_molecules):
        """创建汇总图形"""
        if not successful_molecules:
            return
        
        n_mols = len(successful_molecules)
        cols = min(3, n_mols)
        rows = (n_mols + cols - 1) // cols
        
        fig, axes = self.plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        if n_mols == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes.reshape(1, -1)
        
        for i, (name, img_path) in enumerate(successful_molecules.items()):
            row, col = divmod(i, cols)
            ax = axes[row][col] if rows > 1 else axes[col]
            
            try:
                img = self.Image.open(img_path)
                ax.imshow(img)
                ax.set_title(f"{name}", fontsize=12, fontweight='bold')
                ax.axis('off')
            except:
                ax.text(0.5, 0.5, f"Error loading\n{name}", 
                       ha='center', va='center', transform=ax.transAxes)
                ax.axis('off')
        
        # 隐藏多余的子图
        for i in range(n_mols, rows * cols):
            row, col = divmod(i, cols)
            ax = axes[row][col] if rows > 1 else axes[col]
            ax.axis('off')
        
        self.plt.suptitle("Polyurethane Structures Summary", fontsize=16, fontweight='bold')
        self.plt.tight_layout()
        self.plt.show()

# ============================================================================
# 第五部分：主程序控制
# ============================================================================

class PolyurethaneApp:
    """聚氨酯分子结构绘制应用主类"""
    
    def __init__(self):
        self.modules = {}
        self.processor = None
        self.visualizer = None
        self.successful_molecules = {}
    
    def initialize(self):
        """初始化应用"""
        print("=" * 80)
        print("聚氨酯分子结构绘制程序".center(80))
        print("Polyurethane Molecular Structure Visualization".center(80))
        print("=" * 80)
        
        # 检查并导入库
        success, modules = check_and_import_libraries()
        if not success:
            return False
        
        self.modules = modules
        self.processor = MoleculeProcessor(modules)
        self.visualizer = MoleculeVisualizer(modules)
        
        return True
    
    def process_all_structures(self):
        """处理所有聚氨酯结构"""
        structures = PolyurethaneStructures.get_all_structures()
        
        print(f"\n🎯 准备处理 {len(structures)} 种聚氨酯分子结构")
        print("=" * 60)
        
        for structure_name, structure_info in structures.items():
            print(f"\n{'=' * 60}")
            
            # 创建分子对象
            mol = self.processor.create_molecule(
                structure_info['smiles'], 
                structure_name
            )
            
            if mol is None:
                continue
            
            # 分析分子特征
            analysis = self.processor.analyze_molecule(
                mol, 
                structure_name, 
                structure_info
            )
            
            # 绘制分子结构
            if self.visualizer.draw_molecule(mol, structure_name, structure_info):
                self.successful_molecules[structure_name] = f"polyurethane_{structure_name}.png"
            
            print("-" * 60)
    
    def generate_summary(self):
        """生成总结报告"""
        print("\n" + "=" * 80)
        print("📊 处理结果总结")
        print("=" * 80)
        
        total_structures = len(PolyurethaneStructures.get_all_structures())
        successful_count = len(self.successful_molecules)
        
        print(f"✅ 成功处理: {successful_count}/{total_structures} 个分子结构")
        print(f"📁 工作目录: {os.getcwd()}")
        
        if self.successful_molecules:
            print(f"\n📋 生成的图像文件:")
            for name, filename in self.successful_molecules.items():
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename) / 1024  # KB
                    print(f"   📄 {filename} ({file_size:.1f} KB)")
            
            # 创建汇总图形
            print(f"\n🖼️  正在生成汇总图形...")
            self.visualizer.create_summary_figure(self.successful_molecules)
        
        print("\n" + "=" * 80)
        print("🎉 程序执行完成！")
        print("   所有分子结构图已保存，可用于学习和研究目的。")
        print("=" * 80)
    
    def run(self):
        """运行主程序"""
        try:
            if not self.initialize():
                return
            
            self.process_all_structures()
            self.generate_summary()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  程序被用户中断")
        except Exception as e:
            print(f"\n❌ 程序执行出错: {e}")
            print("\n💡 解决建议：")
            print("1. 确保已安装RDKit：pip install rdkit-pypi")
            print("2. 检查NumPy版本：pip install \"numpy<2\"")
            print("3. 确保已安装其他依赖：pip install matplotlib pillow")

# ============================================================================
# 程序入口点
# ============================================================================

def display_welcome_info():
    """显示欢迎信息和聚氨酯基础知识"""
    welcome_text = """
🧪 聚氨酯(Polyurethane)基础知识

💡 什么是聚氨酯？
   聚氨酯是一类重要的聚合物材料，通过二异氰酸酯与多元醇的聚加成反应制得。

🔗 特征官能团：
   氨基甲酸酯键 (-NH-CO-O-) 是聚氨酯的特征官能团

📋 主要原料：
   • 二异氰酸酯：TDI、MDI、HDI等
   • 多元醇：聚醚多元醇、聚酯多元醇、短链醇等

🎯 应用领域：
   • 泡沫塑料（软泡、硬泡）
   • 弹性体和橡胶
   • 涂料和胶粘剂
   • 合成革和纤维
   • 密封剂和弹性密封材料

本程序将为您绘制多种典型的聚氨酯分子结构，帮助理解其化学组成和特点。
    """
    print(welcome_text)

if __name__ == "__main__":
    # 显示欢迎信息
    display_welcome_info()
    
    # 创建并运行应用
    app = PolyurethaneApp()
    app.run()
