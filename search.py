import requests
import csv

def seach(page):
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

    url = f"https://weibo.com/ajax/statuses/searchProfile?"

    return requests.get(url, headers=headers, params=params).json()

DailyData = []
for i in range(1,10):
    response = seach(i)
    for j in range(0, len(response['data']['list'])):
        DailyData.append(response['data']['list'][j]['text_raw'])
    print(i)
print(DailyData)
print(len(DailyData))

#初步的收集数据（还没进行数据处理）
FileName = 'data.txt'

with open(FileName, 'w', encoding = 'utf-8', newline = '') as f:
    writer = csv.writer(f)
    for row in DailyData:
        writer.writerow(row)
