#-*- coding:utf-8 -*-
# file:run.py
import subprocess
import sys
from pathlib import Path
import os

def find_streamlit_apps(directory):
    """
    在指定目录中查找以"streamlit"开头的Python文件
    """
    apps = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        return apps
    
    # 查找以"streamlit"开头的Python文件
    for file_path in directory_path.glob("streamlit*.py"):
        apps.append(file_path)
    
    return apps

def select_and_run_app():
    """选择并运行 Streamlit 应用"""
    # 获取当前文件的父目录
    current_dir = Path(__file__).parent
    
    print(f"🔍 正在搜索目录: {current_dir}")
    
    # 查找 Streamlit 应用
    apps = find_streamlit_apps(current_dir)
    
    if not apps:
        print("❌ 未找到任何 Streamlit 应用")
        return
    
    print(f"✅ 找到 {len(apps)} 个 Streamlit 应用:")
    print("-" * 50)
    
    # 显示找到的应用
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app.name}")
    
    print("-" * 50)
    
    # 用户选择
    while True:
        try:
            choice = input(f"请选择要运行的应用 (1-{len(apps)}, 或输入 'q' 退出): ").strip()
            
            if choice.lower() == 'q':
                print("👋 已退出")
                return
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(apps):
                selected_app = apps[choice_num - 1]
                break
            else:
                print(f"❌ 请输入 1 到 {len(apps)} 之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字或 'q'")
        except KeyboardInterrupt:
            print("\n👋 已取消")
            return
    
    # 运行选中的应用
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", str(selected_app)]
        print(f"🚀 启动命令: {' '.join(cmd)}")
        print(f"📂 应用路径: {selected_app}")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Web UI 已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    try:
        select_and_run_app()
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == '__main__':
    # 检查是否在 Streamlit 环境中运行，避免循环调用
    if os.environ.get('STREAMLIT_RUNNING'):
        print("❌ 循环调用被阻止")
    else:
        os.environ['STREAMLIT_RUNNING'] = 'True'
        main()