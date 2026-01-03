#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime, timedelta
import pandas as pd

def generate_html_report():
    """生成HTML报告"""

    # 优先从 docs/data 目录读取
    data_dirs = [
        'docs/data/最近7天客流数据.csv',
        '最近7天客流数据.csv',
        '最近7天客流数据.csv'
    ]
    
    df = pd.DataFrame()
    for csv_path in data_dirs:
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, encoding='utf-8')
                if not df.empty:
                    break
            except Exception as e:
                print(f"读取 {csv_path} 时出错: {e}")
                continue

    if os.path.exists('最近7天客流数据.csv'):
        df = pd.read_csv('最近7天客流数据.csv')
        latest_date = df['date'].iloc[0] if len(df) > 0 else "N/A"
        latest_total = df['total'].iloc[0] if len(df) > 0 else "N/A"
    else:
        latest_date = "N/A"
        latest_total = "N/A"
    
    # 统计信息
    if len(df) > 0:
        avg_total = df['total'].mean()
        max_total = df['total'].max()
        min_total = df['total'].min()
        change_7d = ((df['total'].iloc[0] - df['total'].iloc[-1]) / df['total'].iloc[-1] * 100) if len(df) > 1 else 0
    else:
        avg_total = max_total = min_total = change_7d = "N/A"
    
    # HTML模板
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>南京地铁客流分析 - {datetime.now().strftime('%Y年%m月%d日')}</title>
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
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
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
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-card.green {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}
        
        .stat-card.orange {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }}
        
        .stat-card.blue {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .images-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .image-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.3s ease;
        }}
        
        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        
        .image-card img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        
        .image-card .caption {{
            padding: 15px;
            text-align: center;
            background: #f8f9fa;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-bottom: 30px;
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
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .images-grid {{
                grid-template-columns: 1fr;
            }}
            
            .container {{
                padding: 15px;
            }}
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🚇 南京地铁客流每日分析</h1>
            <p class="update-time">数据更新于: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}</p>
            <p class="update-time">最新数据日期: {latest_date}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label"><i class="fas fa-users"></i> 最新日客流</div>
                <div class="stat-value">{latest_total if latest_total != 'N/A' else 'N/A'}万</div>
                <div class="stat-label">万人次</div>
            </div>
            
            <div class="stat-card green">
                <div class="stat-label"><i class="fas fa-chart-line"></i> 7日平均</div>
                <div class="stat-value">{avg_total if avg_total != 'N/A' else 'N/A':.1f}万</div>
                <div class="stat-label">万人次</div>
            </div>
            
            <div class="stat-card orange">
                <div class="stat-label"><i class="fas fa-arrow-up"></i> 周变化</div>
                <div class="stat-value">{change_7d if change_7d != 'N/A' else 'N/A':.1f}%</div>
                <div class="stat-label">与上周相比</div>
            </div>
            
            <div class="stat-card blue">
                <div class="stat-label"><i class="fas fa-subway"></i> 运营线路</div>
                <div class="stat-value">13条</div>
                <div class="stat-label">地铁+S线</div>
            </div>
        </div>
        
        <h2><i class="fas fa-chart-bar"></i> 可视化图表</h2>
        <div class="images-grid">
            <div class="image-card">
                <img src="images/昨日客流线路占比图.png" alt="昨日客流线路占比">
                <div class="caption">
                    <h3>昨日客流线路占比</h3>
                    <p>各线路在总客流中的比例分布</p>
                </div>
            </div>
            
            <div class="image-card">
                <img src="images/最近7天客流强度变化趋势图.png" alt="7天站点客流强度趋势">
                <div class="caption">
                    <h3>7天站点客流强度趋势</h3>
                    <p>各线路站点客流强度变化趋势</p>
                </div>
            </div>
            
            <div class="image-card">
                <img src="images/综合分析仪表板.png" alt="综合分析仪表板">
                <div class="caption">
                    <h3>综合分析仪表板</h3>
                    <p>多维度的数据分析视图</p>
                </div>
            </div>
        </div>
        
        <h2><i class="fas fa-table"></i> 最近7天数据</h2>
        <div class="table-container">
            {df.to_html(index=False, classes='data-table') if len(df) > 0 else '<p>暂无数据</p>'}
        </div>
        
        <h2><i class="fas fa-info-circle"></i> 使用说明</h2>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
            <h3>📊 数据来源</h3>
            <p>数据来源于微博公开数据，每日自动更新。</p>
            
            <h3>⏰ 更新频率</h3>
            <p>每天上午10点(北京时间)自动更新分析报告。</p>
            
            <h3>🔧 技术栈</h3>
            <ul>
                <li>Python 数据采集与处理</li>
                <li>Matplotlib 可视化</li>
                <li>GitHub Actions 自动化</li>
                <li>GitHub Pages 部署展示</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>© {datetime.now().year} 南京地铁客流分析系统 | 自动生成 | 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>数据仅供参考，具体以官方发布为准。</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存HTML文件
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("HTML报告已生成")

if __name__ == "__main__":
    generate_html_report()
