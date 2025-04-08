# -*- coding: utf-8 -*-
import streamlit as st
import subprocess
import sys
import time


# 运行爬虫程序，新增错误检测和友好的 UI 提示
def run_crawler(pages, keyword):
    estimated_time = pages * 4  # 估算等待时间（每页约 4 秒）
    st.write(f"预计爬取 {pages} 页，预计耗时 {estimated_time} 秒，请稍等...")

    progress_bar = st.progress(0)

    # 模拟爬取进度
    for i in range(pages):
        time.sleep(4)  # 每页大约 4 秒
        progress_bar.progress((i + 1) / pages)

    st.write(f"爬虫运行中, 关键词: {keyword}...")

    try:
        # 使用 Popen 以支持流式输入
        process = subprocess.Popen(
            [sys.executable, "crawler.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 向爬虫程序传递关键词
        output, error = process.communicate(input=keyword, timeout=300)  # 超时 300 秒

        if "没有获取到数据" in output:
            st.error("爬虫运行完成，但没有获取到数据。请检查关键词或网络连接！")
        elif "已存在" in output:
            st.warning("数据已存在，未进行插入。")
        elif "插入数据失败" in output:
            st.error("数据已存在，未进行插入！")
        else:
            st.success(f"爬虫程序运行完成，预计爬取的 {pages} 页数据已成功获取！")

        st.text_area("详细日志", output + "\n" + error, height=200)

    except subprocess.TimeoutExpired:
        st.error("爬虫程序运行超时，请检查网络或代码逻辑！")
    except Exception as e:
        st.error(f"运行爬虫时发生错误: {e}")


# 运行数据分析程序，仅显示是否成功
def run_analysis(keyword):
    st.write(f"运行数据分析程序，关键词: {keyword}...")
    with st.spinner("数据分析中..."):
        result = subprocess.run([sys.executable, "analysis.py"], input=keyword, text=True, capture_output=True)

    if result.returncode == 0:
        st.success("数据分析图表生成成功！")
    else:
        st.error("数据分析图表生成失败，请检查程序。")


# 启动可视化仪表盘
def run_dashboard():
    st.write("启动数据可视化界面...")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    st.success("仪表盘已启动，请在浏览器中查看。")


# Streamlit UI
def main():
    st.title("跨境电商数据分析系统")

    keyword = st.text_input("请输入商品关键词 (如: beer, book)", "beer")
    pages = st.number_input("请输入爬取的页数", min_value=1, max_value=100, value=5)

    if st.button("运行爬虫"):
        run_crawler(pages, keyword)

    if st.button("运行数据分析"):
        run_analysis(keyword)

    if st.button("启动可视化仪表盘"):
        run_dashboard()


if __name__ == "__main__":
    main()