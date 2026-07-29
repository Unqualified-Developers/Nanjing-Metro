#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import io
from datetime import datetime, timedelta

import pandas as pd

# ========== 修复 Windows 控制台中文编码问题 ==========
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# ===================================================


def generate_html_report():
    """生成 HTML 报告（中文版）"""

    # 初始化变量
    df = pd.DataFrame()
    latest_date = "N/A"
    latest_total = "N/A"
    avg_total = 0
    max_total = 0
    min_total = 0
    day_change_pct = 0
    day_change_amount = 0
    week_change_pct = 0
    week_change_amount = 0

    # 尝试从多个位置读取数据
    possible_files = [
        'docs/data/recent_passenger_data.csv',
        'recent_passenger_data.csv',
        'docs/data/latest_data.json'
    ]

    # 优先读取 CSV 数据
    for file_path in possible_files:
        if os.path.exists(file_path):
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding='utf-8')
                    if not df.empty:
                        # 确保 'total' 列为数值，无效值转为 NaN 再填 0
                        if 'total' in df.columns:
                            df['total'] = pd.to_numeric(df['total'], errors='coerce').fillna(0)
                        else:
                            print(f"警告: 文件 {file_path} 中未找到 'total' 列")
                            continue

                        # 提取最新日期和最新总客流量
                        if 'date' in df.columns and 'total' in df.columns:
                            latest_date = df['date'].iloc[0]
                            latest_total = df['total'].iloc[0]
                            print(f"数据已从 {file_path} 加载")
                            break
                elif file_path.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    latest_date = json_data.get('latest_date', 'N/A')
                    latest_total = json_data.get('latest_total', 'N/A')
                    # 确保 latest_total 是数值
                    try:
                        latest_total = float(latest_total)
                    except (ValueError, TypeError):
                        latest_total = 0.0
                    print(f"JSON 数据已从 {file_path} 加载")
                    break
            except Exception as e:
                print(f"读取 {file_path} 时出错: {e}")
                continue

    # 计算统计数据（如果存在数据）
    if not df.empty and 'total' in df.columns:
        avg_total = df['total'].mean()
        max_total = df['total'].max()
        min_total = df['total'].min()

        # 计算日环比
        if len(df) > 1:
            day_change_amount = df['total'].iloc[0] - df['total'].iloc[1]
            day_change_pct = (day_change_amount / df['total'].iloc[1] * 100) if df['total'].iloc[1] != 0 else 0

        # 计算周同比（假设数据连续）
        if len(df) > 7:
            week_change_amount = df['total'].iloc[0] - df['total'].iloc[7]
            week_change_pct = (week_change_amount / df['total'].iloc[7] * 100) if df['total'].iloc[7] != 0 else 0

        # 最后才将列名改为中文，用于表格显示
        df = df.rename(columns={
            'date': '日期',
            'total': '总客流量（万）'
        })
    else:
        # 如果没有 CSV 数据，尝试从日志文件提取
        log_file = 'metro_analysis.log'
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in reversed(lines[-20:]):
                        if '总客流量:' in line:
                            parts = line.split('总客流量:')
                            if len(parts) > 1:
                                total_str = parts[1].strip().split(' ')[0].replace('万', '')
                                try:
                                    latest_total = float(total_str)
                                    print(f"从日志提取总客流量: {latest_total}")
                                except:
                                    pass
                        if '最新数据日期:' in line:
                            parts = line.split('最新数据日期:')
                            if len(parts) > 1:
                                latest_date = parts[1].strip()
            except Exception as e:
                print(f"读取日志文件出错: {e}")

    # 读取 config.json 获取线路信息
    with open("config.json", 'r', encoding='utf-8') as f:
        config_data = json.load(f)
        lines = config_data["lines"]
        quantity = len(lines)
        total_stations = sum(line.get("stations", 0) for line in lines)

    # 计算站点客流强度（单位：人次/站，原计算保持 *10000）
    station_intensity = 0
    if latest_total != "N/A" and total_stations > 0:
        try:
            latest_total_num = float(latest_total)
            station_intensity = int((latest_total_num * 10000) / total_stations)
        except (ValueError, TypeError):
            station_intensity = 0

    # 根据变化正负确定卡片颜色
    def get_change_color(value):
        if value > 0:
            return "red"
        elif value < 0:
            return "green"
        else:
            return "black"

    day_color = get_change_color(day_change_pct)
    week_color = get_change_color(week_change_pct)

    # 格式化变化显示
    def format_change_pct(value):
        if value > 0:
            return f"+{value:.3f}%"
        elif value < 0:
            return f"{value:.3f}%"
        else:
            return f"{value:.3f}%"

    def format_change_amount(value):
        if value > 0:
            return f"+{abs(value):.2f}万"
        elif value < 0:
            return f"-{abs(value):.2f}万"
        else:
            return f"{abs(value):.2f}万"

    def format_change_with_amount(pct_value, amount_value):
        return f"{format_change_pct(pct_value)}<br>{format_change_amount(amount_value)}"

    def format_line_info(line_count, station_count):
        return f"{line_count}条<br>{station_count}站"

    # HTML 模板（唯一修改处：站点客流强度显示中去掉了“万”字）
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>南京地铁客流分析 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
        }}
        header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eaeaea;
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .update-time {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            min-width: 340px;
        }}
        .stat-card.green {{
            background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        }}
        .stat-card.orange {{
            background: linear-gradient(135deg, #fde68a 0%, #f97316 100%);
        }}
        .stat-card.dark-blue {{
            background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
        }}
        .stat-card.green-purple {{
            background: linear-gradient(135deg, #10b981 0%, #8b5cf6 100%);
        }}
        .stat-card.purple {{
            background: linear-gradient(135deg, #d8b4fe 0%, #a855f7 100%);
        }}
        .stat-card.red {{
            background: linear-gradient(135deg, #fdba74 0%, #ef4444 100%);
        }}
        .stat-card.black {{
            background: linear-gradient(135deg, #d1d5db 0%, #6b7280 100%);
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .change-card .stat-value,
        .line-card .stat-value {{
            white-space: normal;
            line-height: 1.3;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .change-detail {{
            font-size: 0.8em;
            opacity: 0.9;
            margin-top: 5px;
        }}
        .images-grid {{
            display: flex;
            flex-direction: column;
            gap: 30px;
            margin-bottom: 40px;
        }}
        .image-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.3s ease;
            width: 100%;
        }}
        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        .image-card img {{
            width: 100%;
            height: auto;
            display: block;
            object-fit: contain;
        }}
        .image-card .caption {{
            padding: 15px;
            text-align: center;
            background: #f8f9fa;
        }}
        .table-container {{
            overflow-x: auto;
            margin-bottom: 30px;
            height: 320px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .line-legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .line-item {{
            display: flex;
            align-items: center;
            margin-right: 15px;
        }}
        .line-color {{
            width: 20px;
            height: 20px;
            margin-right: 8px;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eaeaea;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        @media (max-width: 1400px) {{
            .stats-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        @media (max-width: 1100px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            .stat-card {{
                min-width: auto;
            }}
            .container {{
                padding: 15px;
            }}
            h1 {{
                font-size: 2em;
            }}
            .stat-value {{
                font-size: 2em;
            }}
            .change-card .stat-value,
            .line-card .stat-value {{
                font-size: 1.8em;
            }}
        }}
        @media (orientation: landscape) {{
            .images-grid {{
                flex-direction: column;
            }}
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>南京地铁日客流分析</h1>
            <p class="update-time">更新时间（北京时间）：{(datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p class="update-time">最新数据日期：{latest_date}</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">最新日客流量</div>
                <div class="stat-value">{round(latest_total, 2) if latest_total != 'N/A' else 'N/A'}{'' if latest_total == 'N/A' else '万'}</div>
                <div class="stat-label">人次</div>
            </div>

            <div class="stat-card green-purple">
                <div class="stat-label">昨日站点客流强度</div>
                <!-- 修改点：删除了“万”字，原为 {station_intensity} 万/站 -->
                <div class="stat-value">{station_intensity if station_intensity > 0 else 'N/A'}人/站</div>
                <div class="stat-label">客流强度 = 总客流量 / 总车站数</div>
            </div>

            <div class="stat-card orange">
                <div class="stat-label">7日平均客流量</div>
                <div class="stat-value">{avg_total:.2f}万</div>
                <div class="stat-label">人次</div>
            </div>

            <div class="stat-card {day_color} change-card">
                <div class="stat-label">日环比</div>
                <div class="stat-value">{format_change_with_amount(day_change_pct, day_change_amount)}</div>
                <div class="stat-label">与昨日相比</div>
            </div>

            <div class="stat-card {week_color} change-card">
                <div class="stat-label">周同比</div>
                <div class="stat-value">{format_change_with_amount(week_change_pct, week_change_amount)}</div>
                <div class="stat-label">与上周同日相比</div>
            </div>

            <div class="stat-card dark-blue line-card">
                <div class="stat-label">运营线路</div>
                <div class="stat-value">{format_line_info(quantity, total_stations)}</div>
                <div class="stat-label">市区 + 市郊线路</div>
            </div>
        </div>

        <h2>可视化图表</h2>
        <div class="images-grid">
            <div class="image-card">
                <img src="images/yesterday_passenger_line_proportion.png" alt="昨日线路客流占比图">
                <div class="caption"><h3>昨日各线路客流占比</h3></div>
            </div>
            <div class="image-card">
                <img src="images/last_30_days_total_passenger_trend.png" alt="总客流量趋势图">
                <div class="caption"><h3>总客流量趋势</h3></div>
            </div>
            <div class="image-card">
                <img src="images/last_30_days_station_intensity_trend.png" alt="站点客流强度趋势图">
                <div class="caption"><h3>站点客流强度趋势</h3></div>
            </div>
            <div class="image-card">
                <img src="images/last_30_days_line_proportion_trend.png" alt="线路客流占比趋势图">
                <div class="caption"><h3>各线路客流占比趋势</h3></div>
            </div>
        </div>

        <h2>最近30天数据明细</h2>
        <div class="table-container">
            {df.to_html(index=False, classes='data-table') if len(df) > 0 else '<p>暂无数据</p>'}
        </div>

        <div class="footer">
            <p>Copyright &copy; 2025-{datetime.now().year} 南京地铁客流分析系统 | 自动生成</p>
            <p>数据仅供参考，准确性请以官方发布为准。</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存 HTML 文件
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

    print("HTML 报告已生成（中文版）")


if __name__ == "__main__":
    generate_html_report()
