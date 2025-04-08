#dashboard文件
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
import os

# 设置日志
logging.basicConfig(filename='dashboard.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL 配置（无密码）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "amazon_data"
}

# 连接数据库
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")


# 清理表名（确保合法）
def clean_table_name(keyword):
    return keyword.replace(" ", "_").replace("-", "_").lower()


# 从指定表中读取数据
def fetch_data(keyword):
    table_name = clean_table_name(keyword)
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            logging.warning(f"表 {table_name} 中没有数据")
            st.warning(f"表 {table_name} 中没有数据")
        return df
    except Exception as e:
        logging.error(f"从表 {table_name} 读取数据失败: {e}")
        st.error(f"从表 {table_name} 读取数据失败: {e}")
        return pd.DataFrame()  # 返回空 DataFrame


# 数据预处理
def preprocess_data(df):
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df = df[(df["Price"] > 0) & (df["Rating"] > 0)]
    return df


# 可视化分析
def visualize_data(df, keyword):
    if df.empty:
        return

    df = preprocess_data(df)

    st.subheader("商品数据表")
    st.dataframe(df)

    st.markdown("### 数据筛选")
    price_min, price_max = st.slider("选择价格区间",
                                     int(df["Price"].min()),
                                     int(df["Price"].max()),
                                     (int(df["Price"].min()), int(df["Price"].max())))
    rating_min, rating_max = st.slider("选择评分区间",
                                       float(df["Rating"].min()),
                                       float(df["Rating"].max()),
                                       (float(df["Rating"].min()), float(df["Rating"].max())))

    df_filtered = df[(df["Price"] >= price_min) & (df["Price"] <= price_max) &
                     (df["Rating"] >= rating_min) & (df["Rating"] <= rating_max)]

    st.write(f"筛选后共有 {len(df_filtered)} 条记录")
    st.dataframe(df_filtered)

    st.markdown("### 图表展示")

    # 确定图表存储路径
    chart_dir = f"charts/{keyword}"

    if not os.path.exists(chart_dir):
        st.error(f"未找到 {chart_dir} 目录，请先运行 analysis.py 生成数据。")
        return

    # 预设的图表文件映射
    chart_files = {
        "价格分布直方图": "price_distribution.png",
        "评分分布直方图": "rating_distribution.png",
        "评分与价格散点图": "price_vs_rating.png",
        "评论数与评分散点图": "reviews_vs_rating.png"
    }

    # 选择图表
    chart_option = st.selectbox("选择要查看的图表", list(chart_files.keys()))

    # 计算图表路径
    chart_path = os.path.join(chart_dir, chart_files[chart_option])

    # 显示图表
    if os.path.exists(chart_path):
        st.image(chart_path, caption=chart_option, use_container_width=True)
    else:
        st.warning(f"未找到 {chart_option} 对应的图表文件，请检查 {chart_path} 是否存在。")


# 主程序
def main():
    st.title("Amazon 商品数据分析仪表盘")
    keyword = st.text_input("请输入要分析的商品关键词（例如：beer 或 book）", "beer").strip()

    # 读取数据
    df = fetch_data(keyword)
    if not df.empty:
        visualize_data(df, keyword)
    else:
        st.error("未获取到数据，无法进行分析。")


if __name__ == "__main__":
    main()
