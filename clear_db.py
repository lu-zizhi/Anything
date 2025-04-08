# -*- coding: utf-8 -*-
import sys
from sqlalchemy import create_engine, text
import logging

# 设置日志
logging.basicConfig(filename='db_cleanup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL 配置（无密码）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "amazon_data"
}

# 创建数据库连接引擎
engine = create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

# 将关键词转换为合法的表名
def clean_table_name(keyword):
    return keyword.replace(" ", "_").replace("-", "_").lower()

# 删除指定表
def drop_table(keyword):
    table_name = clean_table_name(keyword)
    try:
        with engine.connect() as conn:
            if conn.dialect.has_table(conn, table_name):
                drop_query = text(f"DROP TABLE {table_name}")
                conn.execute(drop_query)
                conn.commit()
                print(f"表 '{table_name}' 已成功删除。")
                logging.info(f"表 '{table_name}' 删除成功。")
            else:
                print(f"表 '{table_name}' 不存在。")
                logging.warning(f"表 '{table_name}' 不存在。")
    except Exception as e:
        print(f"删除表 '{table_name}' 失败: {e}")
        logging.error(f"删除表 '{table_name}' 失败: {e}")

if __name__ == "__main__":
    keyword = input("请输入要删除的商品关键词对应的表（例如：beer 或 book）：").strip()
    drop_table(keyword)
