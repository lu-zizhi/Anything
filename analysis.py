#analysis文件
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import logging
import os

# 设置日志记录
logging.basicConfig(filename='analysis.log', level=logging.INFO,
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

# 用户输入要分析的商品关键词
keyword = input("请输入要分析的商品关键词（例如：beer 或 book）：").strip()

# 清理表名，确保表名合法
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
            print(f"表 {table_name} 中没有数据")
        return df
    except Exception as e:
        logging.error(f"从表 {table_name} 读取数据失败: {e}")
        print(f"从表 {table_name} 读取数据失败: {e}")
        return pd.DataFrame()  # 返回空 DataFrame


# 数据预处理
def preprocess_data(df):
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df = df[df["Price"] > 0]  # 过滤无效价格
    df = df.dropna(subset=["Price", "Rating"])
    return df


# 可视化分析并直接保存图片
def analyze_data(df, keyword):
    if df.empty:
        print("数据为空，无法分析。")
        return

    df = preprocess_data(df)

    # 创建以关键词命名的文件夹，例如 charts/beer/
    keyword_dir = f"charts/{keyword}"
    os.makedirs(keyword_dir, exist_ok=True)

    try:
        sns.set(style="whitegrid", palette="pastel")

        # 1. 价格分布直方图
        plt.figure(figsize=(10, 6))
        sns.histplot(df["Price"], bins=20, kde=True, color="skyblue")
        plt.xlabel("价格 ($)", fontsize=12)
        plt.ylabel("商品数量", fontsize=12)
        plt.title("商品价格分布", fontsize=14)
        plt.tight_layout()
        plt.savefig(f"{keyword_dir}/price_distribution.png")  # 保存到子文件夹
        plt.close()
        logging.info(f"{keyword} 价格分布图已保存")

        # 2. 评分 vs 价格散点图
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df["Price"], y=df["Rating"], size=df["Reviews"], alpha=0.7, legend=False)
        plt.xlabel("价格 ($)", fontsize=12)
        plt.ylabel("评分", fontsize=12)
        plt.title("评分与价格关系", fontsize=14)
        plt.tight_layout()
        plt.savefig(f"{keyword_dir}/price_vs_rating.png")
        plt.close()
        logging.info(f"{keyword} 评分 vs 价格散点图已保存")

        # 3. 评分分布图
        plt.figure(figsize=(10, 6))
        sns.histplot(df["Rating"], bins=10, kde=True, color="lightgreen")
        plt.xlabel("评分", fontsize=12)
        plt.ylabel("频次", fontsize=12)
        plt.title("评分分布", fontsize=14)
        plt.tight_layout()
        plt.savefig(f"{keyword_dir}/rating_distribution.png")
        plt.close()
        logging.info(f"{keyword} 评分分布图已保存")

        # 4. 评论数与评分散点图
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df["Reviews"], y=df["Rating"], alpha=0.7, color="coral")
        plt.xlabel("评论数", fontsize=12)
        plt.ylabel("评分", fontsize=12)
        plt.title("评论数与评分关系", fontsize=14)
        plt.tight_layout()
        plt.savefig(f"{keyword_dir}/reviews_vs_rating.png")
        plt.close()
        logging.info(f"{keyword} 评论数与评分散点图已保存")

        print(f"所有图表已生成并保存至 '{keyword_dir}' 文件夹。")

    except Exception as e:
        logging.error(f"可视化分析失败: {e}")
        print(f"可视化分析失败: {e}")


# 主程序
def main():
    print(f"开始分析 {keyword} 数据...")
    df = fetch_data(keyword)
    if not df.empty:
        analyze_data(df, keyword)


if __name__ == "__main__":
    main()
