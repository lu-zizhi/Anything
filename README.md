# 📦 Amazon 商品数据采集与分析系统

## 📝 项目简介

本项目是一个基于 **Python + MySQL + Streamlit** 构建的 **跨境电商商品竞争分析平台**，主要针对 Amazon 商品页面进行爬取与分析。用户可以输入关键词（如 `beer` 或 `book`），系统将自动完成数据采集、清洗、存储、分析与可视化展示。

---

## 🧩 功能模块

| 模块             | 功能描述                            |
|----------------|---------------------------------|
| `crawler.py`   | 爬取 Amazon 指定关键词的商品数据，并存储至 MySQL |
| `analysis.py`  | 从数据库读取数据，清洗后进行统计分析并生成可视化图表      |
| `dashboard.py` | 使用 Streamlit 创建交互式仪表盘，动态展示分析结果  |
| `clear_db.py`  | 清理 MySQL 数据库中指定关键词对应的数据表        |
| `Run.py`       | 一键运行爬虫、分析与仪表盘展示模块（入口脚本）         |

---

## 🛠 环境依赖

请确保本地已安装以下依赖库：

```bash
pip install requests beautifulsoup4 pandas sqlalchemy pymysql matplotlib seaborn streamlit
```

确保本地 MySQL 数据库已创建，名称为 `amazon_data`，并允许 `root` 用户（无密码）连接：

```sql
CREATE DATABASE amazon_data;
```

---

## 🚀 使用方法

### 1. 数据采集

```bash
python crawler.py
```

输入关键词（如 `beer`），系统将从 Amazon 爬取商品信息，并存入数据库 `amazon_data` 的 `beer` 表中。

### 2. 数据分析与图表生成

```bash
python analysis.py
```

输入关键词（如 `beer`），将生成对应关键词的图表，保存在 `charts/beer/` 文件夹中。

### 3. 启动可视化仪表盘

```bash
streamlit run dashboard.py
```

打开浏览器查看交互式数据分析仪表盘，支持价格、评分筛选。

### 4. 清除指定商品类目数据

```bash
python clear_db.py
```

输入关键词（如 `book`），对应表将从数据库中删除。

### 5. 一键运行全流程

```bash
python Run.py
```

依次自动执行爬虫、分析、可视化仪表盘流程。

---

## 📊 数据字段说明

| 字段名      | 含义           |
|-------------|----------------|
| Title       | 商品标题       |
| Price       | 商品价格（美元）|
| Rating      | 用户评分（1~5星） |
| Reviews     | 评论数量       |
| Image_URL   | 商品图片链接    |
| Product_URL | 商品跳转链接    |

---

## 📁 项目目录结构

```
├── crawler.py
├── analysis.py
├── dashboard.py
├── clear_db.py
├── Run.py
├── charts/
│   └── beer/
│       ├── price_distribution.png
│       ├── rating_distribution.png
│       ├── price_vs_rating.png
│       └── reviews_vs_rating.png
├── README.md
```

---

## 🧠 注意事项

- Amazon 有防爬机制，建议降低请求频率或使用代理。
- 推荐在科学上网环境下运行以确保访问 Amazon 页面成功。
- 程序运行日志保存在当前目录下的 `.log` 文件中。
- 图表文件自动保存在 `charts/{关键词}` 文件夹下。

---

## 👨‍💻 作者

本项目由软件工程专业学生开发，旨在提升数据采集、数据库设计、可视化分析能力，服务于跨境电商智能分析场景。

---
