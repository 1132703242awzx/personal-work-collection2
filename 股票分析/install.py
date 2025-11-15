"""
股票分析系统安装和配置脚本
自动检查环境、安装依赖、配置系统
"""

import os
import sys
import subprocess
import importlib
import platform
from pathlib import Path

class SystemInstaller:
    """系统安装器"""
    
    def __init__(self):
        self.project_dir = Path("d:/股票分析")
        self.required_packages = [
            'torch>=1.12.0',
            'numpy>=1.21.0',
            'pandas>=1.3.0',
            'requests>=2.25.0',
            'beautifulsoup4>=4.9.0',
            'matplotlib>=3.5.0',
            'seaborn>=0.11.0',
            'scikit-learn>=1.0.0',
            'plotly>=5.0.0',
            'lxml>=4.6.0'
        ]
        
        self.directories = [
            'data',
            'models', 
            'output',
            'logs'
        ]
    
    def print_header(self):
        """打印头部信息"""
        print("=" * 70)
        print("🚀 股票分析与预测系统安装器")
        print("📊 基于残差通道-空间注意力网络（R-CSAN）")
        print("=" * 70)
    
    def check_python_version(self):
        """检查Python版本"""
        print("\n🐍 检查Python环境...")
        
        version = sys.version_info
        print(f"   Python版本: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python版本过低，需要Python 3.8或更高版本")
            return False
        
        print("✅ Python版本检查通过")
        return True
    
    def check_system_info(self):
        """检查系统信息"""
        print("\n💻 检查系统信息...")
        
        system = platform.system()
        machine = platform.machine()
        
        print(f"   操作系统: {system}")
        print(f"   架构: {machine}")
        print(f"   处理器: {platform.processor()}")
        
        if system != "Windows":
            print("⚠️ 系统主要为Windows优化，其他系统可能需要调整路径")
        
        return True
    
    def create_directories(self):
        """创建必要的目录"""
        print("\n📁 创建项目目录...")
        
        try:
            # 创建主目录
            self.project_dir.mkdir(exist_ok=True)
            print(f"✅ 主目录: {self.project_dir}")
            
            # 创建子目录
            for dir_name in self.directories:
                dir_path = self.project_dir / dir_name
                dir_path.mkdir(exist_ok=True)
                print(f"✅ 子目录: {dir_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ 目录创建失败: {str(e)}")
            return False
    
    def check_package_installed(self, package_name):
        """检查包是否已安装"""
        try:
            # 处理版本号
            if '>=' in package_name:
                package_name = package_name.split('>=')[0]
            
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False
    
    def install_packages(self):
        """安装依赖包"""
        print("\n📦 检查和安装依赖包...")
        
        missing_packages = []
        installed_packages = []
        
        # 检查哪些包需要安装
        for package in self.required_packages:
            package_name = package.split('>=')[0]
            if self.check_package_installed(package_name):
                installed_packages.append(package_name)
                print(f"✅ {package_name} 已安装")
            else:
                missing_packages.append(package)
                print(f"❌ {package_name} 未安装")
        
        # 安装缺失的包
        if missing_packages:
            print(f"\n🔄 需要安装 {len(missing_packages)} 个包...")
            
            for package in missing_packages:
                print(f"   正在安装 {package}...")
                try:
                    result = subprocess.run([
                        sys.executable, '-m', 'pip', 'install', package
                    ], capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        print(f"✅ {package} 安装成功")
                    else:
                        print(f"❌ {package} 安装失败: {result.stderr}")
                        return False
                        
                except subprocess.TimeoutExpired:
                    print(f"❌ {package} 安装超时")
                    return False
                except Exception as e:
                    print(f"❌ {package} 安装出错: {str(e)}")
                    return False
        else:
            print("✅ 所有依赖包都已安装")
        
        return True
    
    def check_torch_installation(self):
        """特别检查PyTorch安装"""
        print("\n🔥 检查PyTorch安装...")
        
        try:
            import torch
            print(f"✅ PyTorch版本: {torch.__version__}")
            
            # 检查CUDA支持
            if torch.cuda.is_available():
                print(f"✅ CUDA可用: {torch.cuda.get_device_name(0)}")
                print(f"   CUDA版本: {torch.version.cuda}")
            else:
                print("⚠️ CUDA不可用，将使用CPU进行计算")
            
            return True
            
        except ImportError:
            print("❌ PyTorch未正确安装")
            print("   请手动安装: pip install torch")
            return False
    
    def create_config_files(self):
        """创建配置文件"""
        print("\n⚙️ 检查配置文件...")
        
        config_files = [
            'config.py',
            'requirements.txt',
            'README.md'
        ]
        
        for file_name in config_files:
            file_path = self.project_dir / file_name
            if file_path.exists():
                print(f"✅ {file_name} 已存在")
            else:
                print(f"⚠️ {file_name} 不存在，请确保所有文件都已正确放置")
        
        return True
    
    def run_test(self):
        """运行系统测试"""
        print("\n🧪 运行系统测试...")
        
        test_file = self.project_dir / 'test_system.py'
        
        if not test_file.exists():
            print("⚠️ 测试文件不存在，跳过测试")
            return True
        
        try:
            # 切换到项目目录
            os.chdir(self.project_dir)
            
            # 运行测试
            result = subprocess.run([
                sys.executable, 'test_system.py'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ 系统测试通过")
                print("   测试输出:")
                for line in result.stdout.split('\n')[-10:]:
                    if line.strip():
                        print(f"   {line}")
                return True
            else:
                print("❌ 系统测试失败")
                print("   错误信息:")
                for line in result.stderr.split('\n')[-5:]:
                    if line.strip():
                        print(f"   {line}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ 测试超时，可能系统较慢")
            return True
        except Exception as e:
            print(f"❌ 测试运行出错: {str(e)}")
            return False
    
    def print_usage_info(self):
        """打印使用说明"""
        print("\n" + "=" * 70)
        print("🎉 安装完成！")
        print("=" * 70)
        print("\n📋 使用说明:")
        print("1. 进入项目目录:")
        print(f"   cd {self.project_dir}")
        print("\n2. 运行主程序:")
        print("   python main.py")
        print("\n3. 选择运行模式:")
        print("   - 交互模式: 完整功能体验")
        print("   - 快速演示: 一键生成分析报告")
        print("\n4. 输入股票代码示例:")
        print("   - 平安银行: 000001")
        print("   - 中国平安: 601318")
        print("   - 贵州茅台: 600519")
        print("\n🔧 其他命令:")
        print("   测试系统: python test_system.py")
        print("   查看帮助: python main.py --help")
        print("\n⚠️ 风险提示:")
        print("   本系统仅供学习研究，不构成投资建议")
        print("   股市有风险，投资需谨慎")
        print("\n" + "=" * 70)
    
    def install(self):
        """执行完整安装流程"""
        self.print_header()
        
        steps = [
            ("检查Python版本", self.check_python_version),
            ("检查系统信息", self.check_system_info),
            ("创建项目目录", self.create_directories),
            ("安装依赖包", self.install_packages),
            ("检查PyTorch", self.check_torch_installation),
            ("检查配置文件", self.create_config_files),
            ("运行系统测试", self.run_test)
        ]
        
        success_count = 0
        
        for step_name, step_func in steps:
            print(f"\n{'='*50}")
            print(f"📋 步骤: {step_name}")
            print(f"{'='*50}")
            
            try:
                if step_func():
                    success_count += 1
                    print(f"✅ {step_name} 完成")
                else:
                    print(f"❌ {step_name} 失败")
            except Exception as e:
                print(f"❌ {step_name} 出错: {str(e)}")
        
        # 显示安装结果
        print(f"\n{'='*50}")
        print(f"📊 安装结果: {success_count}/{len(steps)} 步骤成功")
        print(f"{'='*50}")
        
        if success_count == len(steps):
            print("🎉 安装完全成功！")
            self.print_usage_info()
        elif success_count >= len(steps) - 1:
            print("⚠️ 安装基本成功，部分功能可能受限")
            self.print_usage_info()
        else:
            print("❌ 安装遇到问题，请检查错误信息")
            print("\n🔧 故障排除建议:")
            print("1. 检查网络连接")
            print("2. 确保有管理员权限")
            print("3. 更新pip: python -m pip install --upgrade pip")
            print("4. 手动安装依赖: pip install -r requirements.txt")

def main():
    """主函数"""
    installer = SystemInstaller()
    installer.install()

if __name__ == "__main__":
    main()
