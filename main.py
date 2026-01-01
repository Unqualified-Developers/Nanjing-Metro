import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from metro_data import NanjingSubwayDataCollector
import pandas as pd

# 设置中文字体和图表样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
mpl.rcParams['figure.dpi'] = 100


class NanjingSubwayVisualizer:
    """南京地铁数据可视化器"""
    
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.colors = plt.cm.Set3(np.linspace(0, 1, len(data_collector.all_lines)))
        
    def plot_latest_line_proportion(self):
        """绘制最新一天各线路客流占比图"""
        proportions = self.data_collector.get_latest_line_proportions()
        latest_date = self.data_collector.get_latest_date()
        
        if not proportions:
            print("没有找到最新数据")
            return None
        
        # 按占比从大到小排序
        sorted_items = sorted(proportions.items(), key=lambda x: x[1], reverse=True)
        lines = [item[0] for item in sorted_items]
        values = [item[1] for item in sorted_items]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 1. 饼图
        wedges, texts, autotexts = ax1.pie(
            values, 
            labels=lines, 
            autopct='%1.1f%%',
            colors=self.colors[:len(lines)],
            startangle=90,
            textprops={'fontsize': 9}
        )
        
        # 美化饼图文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax1.set_title(f'{latest_date} 南京地铁各线路客流占比（饼图）', fontsize=14, fontweight='bold')
        ax1.axis('equal')
        
        # 2. 条形图
        y_pos = np.arange(len(lines))
        bars = ax2.barh(y_pos, values, color=self.colors[:len(lines)])
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(lines, fontsize=10)
        ax2.invert_yaxis()  # 最高的在最上面
        ax2.set_xlabel('占比 (%)', fontsize=12)
        ax2.set_title(f'{latest_date} 南京地铁各线路客流占比（条形图）', fontsize=14, fontweight='bold')
        
        # 在条形上添加数值标签
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax2.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{value:.1f}%', ha='left', va='center', fontsize=9)
        
        # 添加总客流量信息
        latest_data = self.data_collector.get_latest_data()
        total = latest_data['passenger_data'].get('总客流量', 0)
        
        fig.suptitle(f'南京地铁客流分析 - {latest_date}（总客流量: {total:.1f}万）', 
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        return fig
    
    def plot_last_7_days_line_trend(self):
        """绘制最近7天各线路客流强度变化趋势图"""
        df = self.data_collector.get_last_n_days_line_data(7)
        
        if df.empty:
            print("没有找到最近7天的数据")
            return None
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # 绘制每条线路的趋势线
        for i, line in enumerate(self.data_collector.all_lines):
            if line in df.columns:
                # 只显示有数据的线路
                if df[line].notna().any():
                    ax.plot(df['date'], df[line], 
                           label=line, 
                           color=self.colors[i],
                           marker='o',
                           linewidth=2.5,
                           markersize=8)
        
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('客流量（万）', fontsize=12)
        ax.set_title('最近7天南京地铁各线路客流强度变化趋势', fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 设置x轴标签旋转
        plt.xticks(rotation=45, ha='right')
        
        # 添加总客流趋势线
        if 'total' in df.columns:
            ax.plot(df['date'], df['total'], 
                   label='总客流量', 
                   color='black',
                   linewidth=3,
                   linestyle='--',
                   marker='s',
                   markersize=10,
                   alpha=0.7)
        
        # 设置y轴从0开始
        ax.set_ylim(bottom=0)
        
        plt.tight_layout()
        return fig
    
    def plot_last_7_days_proportion_trend(self):
        """绘制最近7天各线路客流占比变化趋势图"""
        df_prop = self.data_collector.get_last_n_days_proportions(7)
        
        if df_prop.empty:
            print("没有找到最近7天的数据")
            return None
        
        # 创建子图
        fig, axes = plt.subplots(2, 1, figsize=(14, 12))
        
        # 1. 主要线路占比趋势（前6条线路）
        main_lines = self.data_collector.all_lines[:6]  # 1-5号线和7号线
        
        for i, line in enumerate(main_lines):
            col_name = f'{line}_占比'
            if col_name in df_prop.columns:
                axes[0].plot(df_prop['date'], df_prop[col_name], 
                           label=line, 
                           color=self.colors[i],
                           marker='o',
                           linewidth=2.5,
                           markersize=8)
        
        axes[0].set_xlabel('日期', fontsize=12)
        axes[0].set_ylabel('占比 (%)', fontsize=12)
        axes[0].set_title('最近7天主要线路客流占比变化趋势', fontsize=14, fontweight='bold')
        axes[0].legend(loc='upper right', fontsize=10)
        axes[0].grid(True, alpha=0.3, linestyle='--')
        axes[0].set_xticklabels(df_prop['date'], rotation=45, ha='right')
        
        # 2. S线占比趋势
        s_lines = [line for line in self.data_collector.all_lines if line.startswith('S')]
        
        for i, line in enumerate(s_lines):
            col_name = f'{line}_占比'
            if col_name in df_prop.columns:
                axes[1].plot(df_prop['date'], df_prop[col_name], 
                           label=line, 
                           color=self.colors[i + len(main_lines)],
                           marker='s',
                           linewidth=2.5,
                           markersize=8)
        
        axes[1].set_xlabel('日期', fontsize=12)
        axes[1].set_ylabel('占比 (%)', fontsize=12)
        axes[1].set_title('最近7天S线路客流占比变化趋势', fontsize=14, fontweight='bold')
        axes[1].legend(loc='upper right', fontsize=10)
        axes[1].grid(True, alpha=0.3, linestyle='--')
        axes[1].set_xticklabels(df_prop['date'], rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def plot_comprehensive_analysis(self):
        """绘制综合分析仪表板"""
        fig = plt.figure(figsize=(18, 12))
        
        # 创建子图网格
        gs = fig.add_gridspec(3, 3)
        
        # 1. 最新一天占比饼图
        ax1 = fig.add_subplot(gs[0, 0])
        proportions = self.data_collector.get_latest_line_proportion()
        latest_date = self.data_collector.get_latest_date()
        
        if proportions:
            sorted_items = sorted(proportions.items(), key=lambda x: x[1], reverse=True)
            top5_lines = [item[0] for item in sorted_items[:5]]
            top5_values = [item[1] for item in sorted_items[:5]]
            
            ax1.pie(top5_values, labels=top5_lines, autopct='%1.1f%%',
                   colors=self.colors[:5], startangle=90)
            ax1.set_title(f'{latest_date} TOP5线路占比', fontsize=12, fontweight='bold')
        
        # 2. 最近7天总客流趋势
        ax2 = fig.add_subplot(gs[0, 1:])
        df = self.data_collector.get_last_n_days_line_data(7)
        if not df.empty and 'total' in df.columns:
            ax2.plot(df['date'], df['total'], 'b-o', linewidth=2, markersize=8)
            ax2.fill_between(df['date'], df['total'], alpha=0.2)
            ax2.set_xlabel('日期')
            ax2.set_ylabel('总客流量（万）')
            ax2.set_title('最近7天总客流趋势', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.set_xticklabels(df['date'], rotation=45, ha='right')
        
        # 3. 主要线路趋势热力图
        ax3 = fig.add_subplot(gs[1:, :])
        main_lines = self.data_collector.all_lines[:8]  # 取前8条主要线路
        
        if not df.empty:
            # 准备热力图数据
            heatmap_data = []
            for line in main_lines:
                if line in df.columns:
                    heatmap_data.append(df[line].values)
            
            if heatmap_data:
                heatmap_data = np.array(heatmap_data)
                
                # 创建热力图
                im = ax3.imshow(heatmap_data, aspect='auto', cmap='YlOrRd', interpolation='nearest')
                
                # 设置坐标轴
                ax3.set_yticks(range(len(main_lines)))
                ax3.set_yticklabels(main_lines)
                ax3.set_xticks(range(len(df)))
                ax3.set_xticklabels(df['date'], rotation=45, ha='right')
                
                # 添加颜色条
                cbar = plt.colorbar(im, ax=ax3)
                cbar.set_label('客流量（万）')
                
                # 添加数值标签
                for i in range(len(main_lines)):
                    for j in range(len(df)):
                        value = heatmap_data[i, j]
                        if not np.isnan(value):
                            ax3.text(j, i, f'{value:.0f}', 
                                    ha='center', va='center', 
                                    color='black' if value > heatmap_data.max()/2 else 'white',
                                    fontsize=8)
                
                ax3.set_title('主要线路客流量热力图（最近7天）', fontsize=14, fontweight='bold')
        
        # 4. 统计信息文本框
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.axis('off')
        
        # 计算统计信息
        stats_text = "统计信息:\n"
        if not df.empty and 'total' in df.columns:
            avg_total = df['total'].mean()
            max_total = df['total'].max()
            min_total = df['total'].min()
            latest_total = df['total'].iloc[0]
            
            stats_text += f"平均总客流: {avg_total:.1f}万\n"
            stats_text += f"最高总客流: {max_total:.1f}万\n"
            stats_text += f"最低总客流: {min_total:.1f}万\n"
            stats_text += f"最新总客流: {latest_total:.1f}万\n"
            
            # 计算增长/下降
            if len(df) >= 2:
                change = df['total'].iloc[0] - df['total'].iloc[1]
                change_pct = (change / df['total'].iloc[1]) * 100
                trend = "↑增长" if change > 0 else "↓下降"
                stats_text += f"日变化: {change:+.1f}万 ({change_pct:+.1f}%) {trend}"
        
        ax4.text(0.1, 0.5, stats_text, fontsize=10, 
                verticalalignment='center', fontfamily='monospace')
        
        fig.suptitle('南京地铁客流综合分析仪表板', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return fig


def main():
    """主函数"""
    print("开始收集南京地铁客流数据...")
    
    # 初始化数据收集器
    collector = NanjingSubwayDataCollector()
    
    # 收集数据
    passenger_records = collector.collect_data()
    
    print(f"\n共收集到 {len(passenger_records)} 条客流记录")
    
    # 显示基本信息
    if passenger_records:
        latest_date = collector.get_latest_date()
        latest_data = collector.get_latest_data()
        total = latest_data['passenger_data'].get('总客流量', 0)
        
        print(f"\n最新数据: {latest_date}")
        print(f"总客流量: {total:.1f}万")
        
        # 初始化可视化器
        visualizer = NanjingSubwayVisualizer(collector)
        
        # 1. 绘制昨日客流线路占比图
        print("\n1. 正在绘制昨日客流线路占比图...")
        fig1 = visualizer.plot_latest_line_proportion()
        if fig1:
            fig1.savefig('昨日客流线路占比图.png', dpi=300, bbox_inches='tight')
            print("  已保存为: 昨日客流线路占比图.png")
        
        # 2. 绘制最近7天客流强度变化趋势图
        print("\n2. 正在绘制最近7天客流强度变化趋势图...")
        fig2 = visualizer.plot_last_7_days_line_trend()
        if fig2:
            fig2.savefig('最近7天客流强度变化趋势图.png', dpi=300, bbox_inches='tight')
            print("  已保存为: 最近7天客流强度变化趋势图.png")
        
        # 3. 绘制最近7天客流占比变化趋势图
        print("\n3. 正在绘制最近7天客流占比变化趋势图...")
        fig3 = visualizer.plot_last_7_days_proportion_trend()
        if fig3:
            fig3.savefig('最近7天客流占比变化趋势图.png', dpi=300, bbox_inches='tight')
            print("  已保存为: 最近7天客流占比变化趋势图.png")
        
        # 4. 绘制综合分析仪表板（可选）
        print("\n4. 正在绘制综合分析仪表板...")
        fig4 = visualizer.plot_comprehensive_analysis()
        if fig4:
            fig4.savefig('综合分析仪表板.png', dpi=300, bbox_inches='tight')
            print("  已保存为: 综合分析仪表板.png")
        
        # 显示图表
        plt.show()
        
        print("\n所有图表已生成完成！")
        
        # 打印数据统计
        print("\n=== 数据统计 ===")
        for line in collector.all_lines[:5]:  # 只显示前5条线路的统计
            line_data = collector.get_line_last_n_days(line, 7)
            if line_data:
                counts = [d['passenger_count'] for d in line_data if d['passenger_count'] is not None]
                if counts:
                    avg = sum(counts) / len(counts)
                    print(f"{line}: 最近7天平均 {avg:.1f}万")
        
        # 保存数据到文件
        df = collector.get_last_n_days_line_data(7)
        df.to_csv('最近7天客流数据.csv', index=False, encoding='utf-8-sig')
        print("\n数据已保存为: 最近7天客流数据.csv")
    else:
        print("没有收集到数据")


if __name__ == "__main__":
    main()
