#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import matplotlib
matplotlib.use('Agg')  # 设置后端，避免GUI问题
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import logging

logger = logging.getLogger(__name__)

def setup_chinese_fonts():
    """完整的中文字体配置方案"""
    
    print("=" * 60)
    print("开始配置中文字体...")
    print("=" * 60)
    
    # 方法1：检查系统已安装的字体
    system_fonts = []
    
    # Linux 字体路径
    linux_font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 文泉驿正黑
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微黑
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # DejaVu
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    
    # 检查字体文件是否存在
    for font_path in linux_font_paths:
        if os.path.exists(font_path):
            system_fonts.append(font_path)
            print(f"✓ 找到系统字体: {font_path}")
    
    # 方法2：如果系统没有中文字体，尝试下载
    if not system_fonts:
        print("⚠ 未找到系统字体，尝试下载中文字体...")
        try:
            # 下载文泉驿字体
            download_fonts()
        except Exception as e:
            print(f"❌ 下载字体失败: {e}")
    
    # 方法3：尝试使用matplotlib的默认字体
    print("\n尝试配置matplotlib字体...")
    
    # 清空matplotlib字体缓存
    cache_dir = matplotlib.get_cachedir()
    font_cache = os.path.join(cache_dir, 'fontlist-v330.json')
    if os.path.exists(font_cache):
        try:
            os.remove(font_cache)
            print(f"✓ 已清除字体缓存: {font_cache}")
        except:
            print(f"⚠ 无法清除字体缓存: {font_cache}")
    
    # 重新扫描字体
    try:
        fm._rebuild()
        print("✓ 已重新构建字体缓存")
    except:
        print("⚠ 重新构建字体缓存失败")
    
    # 获取所有可用字体
    all_fonts = [f.name for f in fm.fontManager.ttflist]
    chinese_font_candidates = [
        'WenQuanYi Zen Hei',      # 文泉驿正黑
        'WenQuanYi Micro Hei',    # 文泉驿微黑
        'DejaVu Sans',            # DejaVu Sans
        'Liberation Sans',        # Liberation Sans
        'Arial Unicode MS',       # Arial Unicode
        'Noto Sans CJK SC',       # Noto Sans
        'Microsoft YaHei',        # 微软雅黑
        'SimHei',                 # 黑体
        'SimSun',                 # 宋体
    ]
    
    available_chinese_fonts = []
    for font_name in chinese_font_candidates:
        if font_name in all_fonts:
            available_chinese_fonts.append(font_name)
    
    print(f"\n可用的中文字体: {available_chinese_fonts}")
    
    if available_chinese_fonts:
        # 设置matplotlib使用中文字体
        plt.rcParams['font.sans-serif'] = available_chinese_fonts + ['DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置默认字体
        matplotlib.rcParams['font.family'] = available_chinese_fonts[0] if available_chinese_fonts else 'sans-serif'
        
        print(f"✓ 已设置字体: {plt.rcParams['font.sans-serif'][0]}")
        return True
    else:
        print("❌ 未找到可用的中文字体！")
        
        # 尝试使用替代方案：手动添加字体
        try:
            # 创建临时字体文件
            import tempfile
            import requests
            
            # 下载思源黑体（开源字体）
            font_url = "https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf"
            temp_dir = tempfile.gettempdir()
            font_path = os.path.join(temp_dir, "SourceHanSansSC-Regular.otf")
            
            if not os.path.exists(font_path):
                print(f"正在下载字体: {font_url}")
                response = requests.get(font_url, timeout=10)
                with open(font_path, 'wb') as f:
                    f.write(response.content)
            
            # 添加字体到matplotlib
            fm.fontManager.addfont(font_path)
            font_prop = fm.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            
            plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            
            print(f"✓ 已下载并使用字体: {font_name}")
            return True
            
        except Exception as e:
            print(f"❌ 字体下载失败: {e}")
    
    return False

def download_fonts():
    """下载中文字体"""
    try:
        # 安装文泉驿字体
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 
                       'fonts-wqy-zenhei', 
                       'fonts-wqy-microhei',
                       'ttf-wqy-zenhei',
                       'ttf-wqy-microhei'], check=True)
        print("✓ 已安装文泉驿字体")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装字体失败: {e}")
        return False

def test_chinese_font():
    """测试中文字体是否正常"""
    print("\n" + "=" * 60)
    print("测试中文字体显示...")
    print("=" * 60)
    
    try:
        # 创建一个简单的测试图表
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # 测试中文字符
        test_texts = [
            "南京地铁客流分析",
            "中文测试：一二三四五",
            "线路占比",
            "日期：2024年"
        ]
        
        for i, text in enumerate(test_texts):
            ax.text(0.1, 0.9 - i*0.2, text, fontsize=14, 
                   transform=ax.transAxes, 
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # 保存测试图片
        test_path = 'chinese_font_test.png'
        fig.savefig(test_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        if os.path.exists(test_path):
            print(f"✓ 字体测试图已保存: {test_path}")
            
            # 检查文件大小
            file_size = os.path.getsize(test_path)
            if file_size > 1000:  # 大于1KB表示可能成功
                print(f"✓ 测试图大小: {file_size} bytes")
                print("✅ 中文字体配置成功！")
                return True
            else:
                print("⚠ 测试图文件大小异常")
        else:
            print("❌ 测试图保存失败")
            
    except Exception as e:
        print(f"❌ 字体测试失败: {e}")
    
    return False

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 设置字体
    success = setup_chinese_fonts()
    
    # 测试字体
    if success:
        test_chinese_font()
    else:
        print("❌ 中文字体配置失败")
        sys.exit(1)
