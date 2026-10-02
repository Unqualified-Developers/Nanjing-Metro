# 🚇 南京地铁数据采集项目

<p align="center">

<a href="README.md">English Version</a>

</p>


<p align="center">

<img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python">
<img src="https://img.shields.io/badge/Selenium-浏览器自动化-green?logo=selenium">
<img src="https://img.shields.io/badge/Edge-WebDriver-0078d7?logo=microsoftedge">
<img src="https://img.shields.io/badge/HTML5-网页数据采集-orange?logo=html5">
<img src="https://img.shields.io/badge/动态网页-数据抓取-purple">
<img src="https://img.shields.io/badge/Open%20Source-GitHub-black?logo=github">

</p>


<p align="center">

一个基于 Python + Selenium 的南京地铁数据采集项目。

## 📌 项目简介

南京地铁数据采集项目是一个基于 Python 的网页数据采集项目。

项目使用 Selenium 浏览器自动化技术，模拟用户访问网页、加载动态内容、滚动页面，并保存网页数据用于后续分析。

## ✨ 项目功能

### 网页数据采集

- 自动打开目标网页
- 支持动态网页加载
- 模拟用户滚动操作
- 获取网页 HTML 源码
- 保存采集结果

## 🛠 技术栈

| 技术 | 用途 |
|---|---|
| Python | 主要开发语言 |
| Selenium | 浏览器自动化 |
| Edge WebDriver | 浏览器控制 |
| HTML | 数据存储格式 |
| Git | 项目管理 |

## 📂 项目结构

```
Nanjing-Metro
│
├── get_html.py
│
├── docs
│   └── data
│       └── page.html
│
├── requirements.txt
│
├── README.md
└── README_CN.md
```

## 🚀 安装运行

克隆项目：

```bash
git clone https://github.com/Unqualified-Developers/Nanjing-Metro.git
```

安装依赖：

```bash
pip install -r requirements.txt
```

运行：

```bash
python get_html.py
```

## ⚙️ 工作流程

```
启动程序
   |
   ↓
打开浏览器
   |
   ↓
访问目标网页
   |
   ↓
加载动态内容
   |
   ↓
自动滚动页面
   |
   ↓
获取网页源码
   |
   ↓
保存数据
```

## 📄 输出结果

采集数据保存：

```
docs/data/page.html
```

该文件保存动态加载后的网页 HTML 内容。

## 🔮 后续计划

- [ ] 自动提取地铁客流数据
- [ ] 增加 HTML 数据解析
- [ ] 使用数据库存储数据
- [ ] 增加数据可视化
- [ ] 增加定时采集任务

## ⚠️ 免责声明

本项目仅用于学习和研究用途。

使用数据采集功能时，请遵守网站服务条款以及相关法律法规。

## 👨‍💻 作者

Unqualified Developers

GitHub:

https://github.com/Unqualified-Developers

## 🤝 贡献

欢迎提交 Issue 和 Pull Request，共同完善项目。
```
