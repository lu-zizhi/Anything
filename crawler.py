#crawler文件
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import time
import random
import logging

# 设置日志
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL 配置
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # 无密码
    "database": "amazon_data"
}

# 连接数据库
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

# 用户输入关键词
keyword = input("请输入要爬取的商品关键词（例如：beer 或 book）：").strip()


# 转换关键词为合法的 SQL 表名
def clean_table_name(keyword):
    # 替换掉不合法的字符，确保表名合法
    return keyword.replace(" ", "_").replace("-", "_").lower()


# 获取页面数据
def fetch_amazon_data(keyword, max_pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    data = []
    for page in range(1, max_pages + 1):
        url = f"https://www.amazon.com/s?k={keyword}&page={page}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logging.error(f"请求失败，状态码: {response.status_code}, URL: {url}")
                continue  # 继续下一个页面爬取
            print(f"成功获取页面: {url}")
            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", {"data-component-type": "s-search-result"})

            if not products:
                logging.warning(f"页面 {url} 没有找到任何商品")

            for product in products:
                title = product.find("h2").get_text(strip=True) if product.find("h2") else "N/A"
                price_tag = product.find("span", class_="a-offscreen")
                price = price_tag.get_text(strip=True).replace("$", "") if price_tag else "N/A"
                rating_tag = product.find("span", class_="a-icon-alt")
                rating = rating_tag.get_text(strip=True).split(" ")[0] if rating_tag else "N/A"
                reviews_tag = product.find("span", class_="a-size-base")
                reviews = reviews_tag.get_text(strip=True).replace(",", "") if reviews_tag else "N/A"
                image_tag = product.find("img", class_="s-image")
                image_url = image_tag["src"] if image_tag else "N/A"
                link_tag = product.find("a", class_="a-link-normal")
                product_url = "https://www.amazon.com" + link_tag["href"] if link_tag else "N/A"

                data.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Reviews": reviews,
                    "Image_URL": image_url,
                    "Product_URL": product_url
                })

            # 随机等待 2-5 秒
            time.sleep(random.randint(2, 5))
        except Exception as e:
            logging.error(f"错误在页面 {url}: {e}")

    return data


# 存储数据到 MySQL
def save_to_mysql(data, keyword):
    if not data:
        print(f"没有获取到 {keyword} 的数据，跳过保存")
        return

    df = pd.DataFrame(data)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

    # 清理表名
    table_name = clean_table_name(keyword)

    try:
        with engine.connect() as conn:
            # 检查表是否存在，若不存在则创建
            if not conn.dialect.has_table(conn, table_name):  # 检查表是否存在
                df.to_sql(table_name, con=engine, index=False, if_exists="replace")
                print(f"表 {table_name} 创建并插入数据成功")
            else:
                for index, row in df.iterrows():
                    title = row["Title"]
                    # 防止重复插入，检查 Title 是否已存在
                    result = conn.execute(f"SELECT COUNT(*) FROM {table_name} WHERE Title = '{title}'").fetchone()
                    if result[0] == 0:  # 该产品没有存在
                        row.to_sql(table_name, con=engine, if_exists="append", index=False)
                        print(f"产品 {title} 插入成功")
                    else:
                        print(f"产品 {title} 已存在，跳过")

        print(f"数据成功存入 MySQL 表: {table_name}")
    except Exception as e:
        logging.error(f"数据插入失败: {e}")
        print(f"插入数据失败：{e}")


# 主程序
def main():
    print("开始爬取数据...")
    data = fetch_amazon_data(keyword, max_pages=5)

    if data:
        save_to_mysql(data, keyword)
    else:
        print("没有获取到数据，退出程序。")


if __name__ == "__main__":
    main()