import subprocess
import sys
def run_streamlit():
    print("正在启动 Streamlit 应用...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "UI.py"], check=True)

if __name__ == "__main__":
    run_streamlit()
