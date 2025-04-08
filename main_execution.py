import sys
import subprocess

def run_crawler():
    print("运行爬虫程序...")
    subprocess.run([sys.executable, "crawler.py"], check=True)

def run_analysis():
    print("运行数据分析程序...")
    subprocess.run([sys.executable, "analysis.py"], check=True)

def run_dashboard():
    print("启动数据可视化界面...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], check=True)

if __name__ == "__main__":
    run_crawler()
    run_analysis()
    run_dashboard()
