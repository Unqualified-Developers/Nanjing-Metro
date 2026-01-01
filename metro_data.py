import requests
import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd


class NanjingSubwayDataCollector:
    """南京地铁数据收集器"""
    
    def __init__(self):
        self.passenger_records = []
        self.line_data = {}
        self.all_lines = [
            "1号线", "2号线", "3号线", "4号线", "5号线", "7号线", "10号线",
            "S1号线", "S3号线", "S6号线", "S7号线", "S8号线", "S9号线"
        ]
    
    def search_weibo(self, page: int) -> dict:
        """
        搜索微博数据
        
        Args:
            page: 页码
            
        Returns:
            dict: 返回的JSON数据
        """
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Client-Version": "v2.47.142",
            "Cookie": "XSRF-TOKEN=dPJyf43qgrCE7oU0r4KZK2Ya; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaMouseten=null; ariaStatus=false; SCF=Aq-c9YP3yXfiDqh9zXt5_kpDe7HMxnxDWXB_OEknXWQPyc-YXQfU4gzOdOjDf6gqI-S_qQUh20JmwSpVLcsXcT4.; SUB=_2A25ES4Z-DeRhGe5M4lIR8ijMyTqIHXVnKIe2rDV8PUNbmtAYLXfEkW9NdKSSYXrL569k38XkwoWjJk2-fG2pmuSJ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5kZs3mN9X52i3GwiBiSw_G5NHD95QReo.7ehzcehzcWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zN1hz4eh5ESo5ESntt; ALF=02_1769440046; WBPSESS=krzeCBEgQh8TvPwaITf8yZ3XMZnkBuzLNUry0NLOIzWJSMDmQhlriF2HX6nC_FqvcPUpEdYaGj8QtopYstgpSUUgiqFEDtDoQ0suh3Lp0dIBrdF10iLSQyFOsGz_PuYyzzeT3ZkIpkzRcnKPbArOWA==; _s_tentry=passport.weibo.com; Apache=5652403287654.71.1766848028206; SINAGLOBAL=5652403287654.71.1766848028206; ULV=1766848028209:1:1:1:5652403287654.71.1766848028206;",
            "Referer": "https://weibo.com/u/2638276292?tabtype=feed",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Server-Version": "v2025.12.26.3",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "x-xsrf-token": "dPJyf43qgrCE7oU0r4KZK2Ya"
        }
        
        params = {
            "uid": "2638276292",
            "page": page,
            "q": "昨日客流"
        }
        
        url = "https://weibo.com/ajax/statuses/searchProfile?"
        
        return requests.get(url, headers=headers, params=params).json()
    
    def extract_passenger_data(self, text: str) -> Optional[Dict[str, float]]:
        """
        从文本中提取客流数据
        
        Args:
            text: 包含客流数据的文本
            
        Returns:
            Optional[Dict[str, float]]: 线路到客流量的字典，如果提取失败返回None
        """
        # 定义线路名称和对应的正则表达式模式
        line_patterns = {
            "1号线": r'1号线\s*(\d+(?:\.\d+)?)',
            "2号线": r'2号线\s*(\d+(?:\.\d+)?)',
            "3号线": r'3号线\s*(\d+(?:\.\d+)?)',
            "4号线": r'4号线\s*(\d+(?:\.\d+)?)',
            "5号线": r'5号线\s*(\d+(?:\.\d+)?)',
            "7号线": r'7号线\s*(\d+(?:\.\d+)?)',
            "10号线": r'10号线\s*(\d+(?:\.\d+)?)',
            "S1号线": r'S1号线\s*(\d+(?:\.\d+)?)',
            "S3号线": r'S3号线\s*(\d+(?:\.\d+)?)',
            "S6号线": r'S6号线\s*(\d+(?:\.\d+)?)',
            "S7号线": r'S7号线\s*(\d+(?:\.\d+)?)',
            "S8号线": r'S8号线\s*(\d+(?:\.\d+)?)',
            "S9号线": r'S9号线\s*(\d+(?:\.\d+)?)'
        }
        
        passenger_data = {}
        
        for line_name, pattern in line_patterns.items():
            match = re.search(pattern, text)
            if match:
                try:
                    passenger_data[line_name] = float(match.group(1))
                except ValueError:
                    # 如果转换失败，尝试查找"停运"关键字
                    if "停运" in text or f"{line_name}停运" in text:
                        passenger_data[line_name] = 0.0
                    else:
                        passenger_data[line_name] = None
            else:
                # 检查是否有停运的情况
                if f"{line_name}停运" in text:
                    passenger_data[line_name] = 0.0
                else:
                    passenger_data[line_name] = None
        
        # 提取总客流量（如果有）
        total_pattern = r'客运量\s*(\d+(?:\.\d+)?)'
        total_match = re.search(total_pattern, text)
        if total_match:
            try:
                passenger_data["总客流量"] = float(total_match.group(1))
            except ValueError:
                passenger_data["总客流量"] = None
        
        return passenger_data if passenger_data else None
    
    def extract_date(self, text: str) -> Optional[str]:
        """
        从文本中提取日期
        
        Args:
            text: 包含日期的文本
            
        Returns:
            Optional[str]: 格式为"MM-DD"的日期字符串，如果提取失败返回None
        """
        # 匹配"X月X日"的格式
        date_pattern = r'(\d{1,2})月(\d{1,2})日'
        match = re.search(date_pattern, text)
        
        if match:
            month = match.group(1).zfill(2)
            day = match.group(2).zfill(2)
            return f"{month}-{day}"
        
        return None
    
    def collect_data(self) -> List[Dict]:
        """
        收集南京地铁客流数据
        
        Returns:
            List[Dict]: 包含日期和客流数据的字典列表
        """
        passenger_records = []
        
        for page in range(1, 10):
            try:
                response = self.search_weibo(page)
                
                if 'data' in response and 'list' in response['data']:
                    for item in response['data']['list']:
                        text = item.get('text_raw', '')
                        
                        # 跳过非客流相关的内容
                        if '客流' not in text or '南京地铁' not in text:
                            continue
                        
                        # 提取日期
                        date_str = self.extract_date(text)
                        
                        # 提取客流数据
                        passenger_data = self.extract_passenger_data(text)
                        
                        if date_str and passenger_data:
                            record = {
                                "date": date_str,
                                "passenger_data": passenger_data,
                                "raw_text": text[:100]
                            }
                            passenger_records.append(record)
                            
                print(f"已处理第 {page} 页数据")
                
            except Exception as e:
                print(f"处理第 {page} 页数据时出错: {e}")
                continue
        
        self.passenger_records = passenger_records
        self._organize_by_line()
        return passenger_records
    
    def _organize_by_line(self):
        """按线路整理数据"""
        for line in self.all_lines:
            self.line_data[line] = []
            for record in self.passenger_records:
                value = record['passenger_data'].get(line)
                self.line_data[line].append({
                    "date": record['date'],
                    "passenger_count": value,
                    "total": record['passenger_data'].get('总客流量')
                })
    
    def get_latest_date(self) -> str:
        """获取最新日期"""
        if not self.passenger_records:
            return ""
        return self.passenger_records[0]['date']
    
    def get_latest_data(self) -> Dict:
        """获取最新一天的数据"""
        if not self.passenger_records:
            return {}
        return self.passenger_records[0]
    
    def get_last_n_days(self, n: int = 7) -> List[Dict]:
        """获取最近n天的数据"""
        if not self.passenger_records:
            return []
        return self.passenger_records[:min(n, len(self.passenger_records))]
    
    def get_line_last_n_days(self, line_name: str, n: int = 7) -> List[Dict]:
        """获取指定线路最近n天的数据"""
        if line_name not in self.line_data:
            return []
        return self.line_data[line_name][:min(n, len(self.line_data[line_name]))]
    
    def get_latest_line_proportions(self) -> Dict[str, float]:
        """获取最新一天各线路占比"""
        latest_data = self.get_latest_data()
        if not latest_data:
            return {}
        
        passenger_data = latest_data['passenger_data']
        total = passenger_data.get('总客流量')
        if not total:
            return {}
        
        proportions = {}
        for line in self.all_lines:
            count = passenger_data.get(line)
            if count is not None:
                proportions[line] = (count / total) * 100
        
        return proportions
    
    def get_last_n_days_line_data(self, n: int = 7) -> pd.DataFrame:
        """获取最近n天各线路数据（DataFrame格式）"""
        last_n_days = self.get_last_n_days(n)
        
        data = []
        for record in last_n_days:
            row = {'date': record['date'], 'total': record['passenger_data'].get('总客流量')}
            for line in self.all_lines:
                row[line] = record['passenger_data'].get(line)
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def get_last_n_days_proportions(self, n: int = 7) -> pd.DataFrame:
        """获取最近n天各线路占比（DataFrame格式）"""
        df = self.get_last_n_days_line_data(n)
        
        # 计算每条线路的占比
        for line in self.all_lines:
            if line in df.columns:
                df[f'{line}_占比'] = df[line] / df['total'] * 100
        
        return df
