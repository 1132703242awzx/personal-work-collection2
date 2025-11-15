"""
北京3D地形图启动器
用户可以选择运行基础版或增强版
"""

import sys
import os

def show_menu():
    """显示菜单选项"""
    print("=" * 60)
    print("🗺️  北京市交互式3D地形图生成器")
    print("=" * 60)
    print()
    print("请选择运行模式:")
    print("1. 基础版 - 快速生成，适合初次体验")
    print("2. 增强版 - 高精度地形，包含地标和分析")
    print("3. 查看项目说明")
    print("4. 退出")
    print()

def show_project_info():
    """显示项目信息"""
    print("\n" + "=" * 60)
    print("📋 项目信息")
    print("=" * 60)
    print("""
🎯 项目目标:
   生成北京市的交互式3D地形图，展现真实的山川地貌

🛠️ 核心技术:
   • PyVista: 3D可视化引擎
   • XArray/Rioxarray: 地理数据处理
   • GeoPandas: 空间数据分析
   • NumPy/SciPy: 科学计算

🌄 地形特征:
   • 西山山脉: 北京西部主要山脉，包括香山、妙峰山
   • 军都山: 北部山区，包括八达岭、居庸关
   • 燕山余脉: 东部和北部山地
   • 北京平原: 城市主要区域
   • 河流水系: 永定河、温榆河等

🎮 交互功能:
   • 鼠标左键: 旋转视角
   • 鼠标右键: 平移地图  
   • 滚轮: 缩放视图
   • 键盘快捷键: r(重置), w(线框), s(表面)

📁 输出文件:
   • 3D地形图: 交互式窗口
   • 2D预览图: PNG格式
   • 地形数据: GeoTIFF格式
   • 分析报告: 综合统计图表

🎨 可视化特色:
   • 真实地形色彩映射
   • 等高线显示
   • 地标标注
   • 坡度分析
   • 地形剖面
""")
    input("\n按回车键返回主菜单...")

def main():
    """主函数"""
    while True:
        try:
            show_menu()
            choice = input("请输入选择 (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 启动基础版地形图生成器...")
                print("-" * 40)
                from main import main as run_basic
                run_basic()
                
            elif choice == "2":
                print("\n🚀 启动增强版地形图生成器...")
                print("-" * 40)
                from enhanced_main import main_enhanced as run_enhanced
                run_enhanced()
                
            elif choice == "3":
                show_project_info()
                
            elif choice == "4":
                print("\n👋 谢谢使用！再见！")
                sys.exit(0)
                
            else:
                print("\n❌ 无效选择，请输入 1-4 之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断程序")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ 程序执行出错: {e}")
            import traceback
            traceback.print_exc()
        
        # 询问是否继续
        print("\n" + "-" * 40)
        continue_choice = input("是否继续使用？(y/n): ").strip().lower()
        if continue_choice in ['n', 'no', '否']:
            print("👋 再见！")
            break

if __name__ == "__main__":
    main()
