#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
from metro_data import NanjingSubwayDataCollector
import pandas as pd
import os
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metro_analysis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 解决中文乱码问题的完整方案
def setup_chinese_font():
    """设置中文字体，解决乱码问题"""
    try:
        # 方法1: 查找系统中已安装的中文字体
        chinese_fonts = []
        font_paths = [
            # Windows 字体路径
            'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
            'C:/Windows/Fonts/simkai.ttf',  # 楷体
            # Linux 字体路径
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 文泉驿正黑
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # DejaVu Sans
            # Mac 字体路径
            '/System/Library/Fonts/PingFang.ttc',  # 苹方
            '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                chinese_fonts.append(font_path)
        
        if chinese_fonts:
            # 添加字体到matplotlib
            for font_file in chinese_fonts:
                try:
                    fm.fontManager.addfont(font_file)
                    font_name = fm.FontProperties(fname=font_file).get_name()
                    plt.rcParams['font.sans-serif'] = [font_name]
                    plt.rcParams['axes.unicode_minus'] = False
                    logger.info(f"成功加载字体: {font_name}")
                    break
                except Exception as e:
                    logger.warning(f"加载字体 {font_file} 失败: {e}")
        
        # 方法2: 使用默认配置作为后备
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
    except Exception as e:
        logger.error(f"设置中文字体时出错: {e}")

# 调用字体设置函数
setup_chinese_font()

# 设置图表样式
mpl.rcParams['figure.dpi'] = 100
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['figure.figsize'] = (14, 8)

class NanjingSubwayVisualizer:
    """南京地铁数据可视化器"""
    
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.line_colors = self._get_line_colors()
        
    def _get_line_colors(self):
        """获取线路颜色，如果没有配置则生成默认颜色"""
        colors = {}
        line_colors_config = self.data_collector.get_line_colors()
        
        if line_colors_config:
            return line_colors_config
        
        all_lines = self.data_collector.all_lines
        n_lines = len(all_lines)
        
        cmap = plt.cm.Set3
        for i, line in enumerate(all_lines):
            colors[line] = cmap(i / max(1, n_lines - 1))
        
        return colors
    
    def plot_latest_line_proportion(self):
        """绘制最新一天各线路客流占比图"""
        try:
            proportions = self.data_collector.get_latest_line_proportions()
            latest_date = self.data_collector.get_latest_date()
            
            if not proportions:
                logger.warning("没有找到最新数据")
                return None
            
            sorted_items = sorted(proportions.items(), key=lambda x: x[1], reverse=True)
            lines = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            
            colors = [self.line_colors.get(line, '#CCCCCC') for line in lines]
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # 饼图
            wedges, texts, autotexts = ax1.pie(
                values, 
                labels=lines, 
                autopct='%1.1f%%',
                colors=colors,
                startangle=90,
                textprops={'fontsize': 9}
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax1.set_title(f'{latest_date} 南京地铁各线路客流占比（饼图）', fontsize=14, fontweight='bold')
            ax1.axis('equal')
            
            # 条形图
            y_pos = np.arange(len(lines))
            bars = ax2.barh(y_pos, values, color=colors)
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(lines, fontsize=10)
            ax2.invert_yaxis()
            ax2.set_xlabel('占比 (%)', fontsize=12)
            ax2.set_title(f'{latest_date} 南京地铁各线路客流占比（条形图）', fontsize=14, fontweight='bold')
            
            for bar, value in zip(bars, values):
                width = bar.get_width()
                ax2.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{value:.1f}%', ha='left', va='center', fontsize=9)
            
            latest_data = self.data_collector.get_latest_data()
            total = latest_data['passenger_data'].get('总客流量', 0)
            
            fig.suptitle(f'南京地铁客流分析 - {latest_date}（总客流量: {total:.1f}万）', 
                        fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            # 保存图片
            os.makedirs('docs/images', exist_ok=True)
            fig.savefig('docs/images/昨日客流线路占比图.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            logger.info("昨日客流线路占比图已生成")
            return fig
            
        except Exception as e:
            logger.error(f"生成占比图时出错: {e}")
            return None
    
    def plot_last_n_days_line_trend(self, n_days=7):
        """绘制最近n天各线路客流强度变化趋势图"""
        try:
            df = self.data_collector.get_last_n_days_line_data(n_days)
            
            if df.empty:
                logger.warning(f"没有找到最近{n_days}天的数据")
                return None
            
            fig, ax = plt.subplots(figsize=(14, 8))
            
            for line in self.data_collector.all_lines:
                if line in df.columns:
                    if df[line].notna().any():
                        color = self.line_colors.get(line, '#CCCCCC')
                        ax.plot(df['date'], df[line], 
                               label=line, 
                               color=color,
                               marker='o',
                               linewidth=2.5,
                               markersize=8)
            
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('客流量（万）', fontsize=12)
            ax.set_title(f'最近{n_days}天南京地铁各线路客流强度变化趋势', fontsize=14, fontweight='bold')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            ax.grid(True, alpha=0.3, linestyle='--')
            
            plt.xticks(rotation=45, ha='right')
            
            if 'total' in df.columns:
                ax.plot(df['date'], df['total'], 
                       label='总客流量', 
                       color='black',
                       linewidth=3,
                       linestyle='--',
                       marker='s',
                       markersize=10,
                       alpha=0.7)
            
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            
            # 保存图片
            os.makedirs('docs/images', exist_ok=True)
            fig.savefig(f'docs/images/最近{n_days}天客流强度变化趋势图.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            logger.info(f"最近{n_days}天客流强度变化趋势图已生成")
            return fig
            
        except Exception as e:
            logger.error(f"生成趋势图时出错: {e}")
            return None
    
    def plot_comprehensive_analysis(self, n_days=7):
        """绘制综合分析仪表板"""
        try:
            fig = plt.figure(figsize=(18, 12))
            gs = fig.add_gridspec(3, 3)
            
            df = self.data_collector.get_last_n_days_line_data(n_days)
            
            if not df.empty:
                # 饼图
                proportions = self.data_collector.get_latest_line_proportions()
                if proportions:
                    ax1 = fig.add_subplot(gs[0, 0])
                    sorted_items = sorted(proportions.items(), key=lambda x: x[1], reverse=True)
                    top5_lines = [item[0] for item in sorted_items[:5]]
                    top5_values = [item[1] for item in sorted_items[:5]]
                    top5_colors = [self.line_colors.get(line, '#CCCCCC') for line in top5_lines]
                    
                    ax1.pie(top5_values, labels=top5_lines, autopct='%1.1f%%',
                           colors=top5_colors, startangle=90)
                    ax1.set_title('TOP5线路占比', fontsize=12, fontweight='bold')
                
                # 总客流趋势
                ax2 = fig.add_subplot(gs[0, 1:])
                if 'total' in df.columns:
                    ax2.plot(df['date'], df['total'], 'b-o', linewidth=2, markersize=8)
                    ax2.fill_between(df['date'], df['total'], alpha=0.2)
                    ax2.set_xlabel('日期')
                    ax2.set_ylabel('总客流量（万）')
                    ax2.set_title(f'最近{n_days}天总客流趋势', fontsize=12, fontweight='bold')
                    ax2.grid(True, alpha=0.3)
                    ax2.set_xticklabels(df['date'], rotation=45, ha='right')
                
                # 热力图
                ax3 = fig.add_subplot(gs[1:, :])
                main_lines = self.data_collector.all_lines[:8]
                
                heatmap_data = []
                valid_lines = []
                for line in main_lines:
                    if line in df.columns and df[line].notna().any():
                        heatmap_data.append(df[line].values)
                        valid_lines.append(line)
                
                if heatmap_data:
                    heatmap_data = np.array(heatmap_data)
                    im = ax3.imshow(heatmap_data, aspect='auto', cmap='YlOrRd', interpolation='nearest')
                    
                    ax3.set_yticks(range(len(valid_lines)))
                    ax3.set_yticklabels(valid_lines)
                    ax3.set_xticks(range(len(df)))
                    ax3.set_xticklabels(df['date'], rotation=45, ha='right')
                    
                    cbar = plt.colorbar(im, ax=ax3)
                    cbar.set_label('客流量（万）')
                    
                    for i in range(len(valid_lines)):
                        for j in range(len(df)):
                            value = heatmap_data[i, j]
                            if not np.isnan(value):
                                ax3.text(j, i, f'{value:.0f}', 
                                        ha='center', va='center', 
                                        color='black' if value > heatmap_data.max()/2 else 'white',
                                        fontsize=8)
                    
                    ax3.set_title(f'主要线路客流量热力图（最近{n_days}天）', fontsize=14, fontweight='bold')
                
                # 统计信息
                ax4 = fig.add_subplot(gs[2, 0])
                ax4.axis('off')
                
                stats_text = "统计信息:\n"
                if 'total' in df.columns:
                    avg_total = df['total'].mean()
                    max_total = df['total'].max()
                    min_total = df['total'].min()
                    latest_total = df['total'].iloc[0]
                    
                    stats_text += f"平均总客流: {avg_total:.1f}万\n"
                    stats_text += f"最高总客流: {max_total:.1f}万\n"
                    stats_text += f"最低总客流: {min_total:.1f}万\n"
                    stats_text += f"最新总客流: {latest_total:.1f}万\n"
                    
                    if len(df) >= 2:
                        change = df['total'].iloc[0] - df['total'].iloc[1]
                        change_pct = (change / df['total'].iloc[1]) * 100 if df['total'].iloc[1] != 0 else 0
                        trend = "↑增长" if change > 0 else "↓下降"
                        stats_text += f"日变化: {change:+.1f}万 ({change_pct:+.1f}%) {trend}"
                
                ax4.text(0.1, 0.5, stats_text, fontsize=10, 
                        verticalalignment='center', fontfamily='monospace')
            
            fig.suptitle('南京地铁客流综合分析仪表板', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            # 保存图片
            os.makedirs('docs/images', exist_ok=True)
            fig.savefig('docs/images/综合分析仪表板.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            logger.info("综合分析仪表板已生成")
            return fig
            
        except Exception as e:
            logger.error(f"生成分析仪表板时出错: {e}")
            return None

def main():
    """主函数"""
    logger.info("开始收集南京地铁客流数据...")
    
    try:
        # 初始化数据收集器
        collector = NanjingSubwayDataCollector("config.json")
        
        # 收集数据
        passenger_records = collector.collect_data()
        
        logger.info(f"共收集到 {len(passenger_records)} 条客流记录")
        
        if passenger_records:
            latest_date = collector.get_latest_date()
            latest_data = collector.get_latest_data()
            total = latest_data['passenger_data'].get('总客流量', 0)
            
            logger.info(f"最新数据: {latest_date}")
            logger.info(f"总客流量: {total:.1f}万")
            
            # 初始化可视化器
            visualizer = NanjingSubwayVisualizer(collector)
            
            # 生成图表
            logger.info("正在生成可视化图表...")
            visualizer.plot_latest_line_proportion()
            visualizer.plot_last_n_days_line_trend(7)
            visualizer.plot_comprehensive_analysis(7)
            
            # 保存数据
            os.makedirs('docs/data', exist_ok=True)
            df = collector.get_last_n_days_line_data(7)
            if not df.empty:
                df.to_csv('docs/data/最近7天客流数据.csv', index=False, encoding='utf-8-sig')
                logger.info("数据已保存")
            
            # 保存最新数据到JSON
            data_summary = {
                'update_time': datetime.now().isoformat(),
                'latest_date': latest_date,
                'latest_total': float(total),
                'record_count': len(passenger_records),
                'lines_analyzed': collector.all_lines
            }
            
            with open('docs/data/latest_summary.json', 'w', encoding='utf-8') as f:
                json.dump(data_summary, f, ensure_ascii=False, indent=2)
            
            logger.info("分析完成！")
            
        else:
            logger.warning("没有收集到数据")
            
    except Exception as e:
        logger.error(f"运行过程中发生错误: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
