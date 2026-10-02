
# 🚇 Nanjing Metro Data Collection Project

<p align="center">

<a href="README_CN.md">中文版本</a>

</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python">
<img src="https://img.shields.io/badge/Selenium-Web_Automation-green?logo=selenium">
<img src="https://img.shields.io/badge/Microsoft%20Edge-WebDriver-0078d7?logo=microsoftedge">
<img src="https://img.shields.io/badge/HTML5-Data_Collection-orange?logo=html5">
<img src="https://img.shields.io/badge/Web%20Scraping-Dynamic_Page-purple">
<img src="https://img.shields.io/badge/GitHub-Open_Source-black?logo=github">

</p>

<p align="center">
A Python-based web data collection project for Nanjing Metro information.
</p>


## 📌 Overview

Nanjing Metro Data Collection Project is a Python-based web data collection project.

This project uses Selenium browser automation technology to collect dynamic web page information related to Nanjing Metro, simulate user operations, and save collected HTML data for further analysis.

## ✨ Features

### Web Data Collection

- Automatically open target webpages
- Support dynamic webpage loading
- Simulate scrolling behavior
- Capture webpage HTML source code
- Save collected data locally

## 🛠 Technology Stack

| Technology | Description |
|---|---|
| Python | Main programming language |
| Selenium | Browser automation |
| Edge WebDriver | Browser control |
| HTML | Data storage format |
| Git | Version control |

## 📂 Project Structure

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

## 🚀 Installation

Clone repository:

```bash
git clone https://github.com/Unqualified-Developers/Nanjing-Metro.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python get_html.py
```

## ⚙️ Workflow

```
Start Program
      |
      ↓
Open Browser
      |
      ↓
Load Website
      |
      ↓
Dynamic Content Loading
      |
      ↓
Automatic Scrolling
      |
      ↓
Collect HTML
      |
      ↓
Save Data
```

## 📄 Output

Collected webpage data will be saved:

```
docs/data/page.html
```

## 🔮 Future Plans

- [ ] Automatically extract metro passenger flow data
- [ ] Add HTML parser
- [ ] Store data in database
- [ ] Build visualization dashboard
- [ ] Add scheduled data collection

## ⚠️ Disclaimer

This project is for learning and research purposes only.

Please follow website terms of service and related regulations when collecting data.

## 👨‍💻 Author

Unqualified Developers

GitHub:
https://github.com/Unqualified-Developers

## 🤝 Contribution

Issues and Pull Requests are welcome.
```
