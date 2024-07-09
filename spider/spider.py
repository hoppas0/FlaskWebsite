import random
import time

import requests
from lxml import etree
import pandas as pd


def spider(city, page):
    url = f'https://www.muniao.com/{city}/null-0-0-0-0-0-0-0-{page}.html?tn=mn19091015'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Cookie': 'Bsksdjd=down_app; route=08f42880ec49b6034f8be01f1d53ca1b; sl-session=WUL2PXiMWmZ5ZGUetMYsUw==; ASP.NET_SessionId=4u452qalznu3tykkct1hz4c2; Front_LoginUserKey=85EFE19FA89BC4804B73D1060E8099601D6B300D5719B9E98435AABE6FF8F633027DCCD2DCE8D2C356DFF999908DF577725E32714A04549FFEFB35EAD2EF76894A7FCA98EDFFCC038829F34775804A1C73B2597F36B48F9B3D7F48BF20CEEF631A9E91EC3329C8C9D1FDCDD4B72489B18E3C6B0D518296D72C6440132CAC90E69BECBBC2B539EB69C763EC1FBB0EE46F4FEBE95CF34109DB74CEC05565EF07623218A4AF7AC4BD5987B0EDC350F9D39FF66D9739D310FF048C421A50096DF6A5E3B74A9074973C94'
    }
    resp = requests.get(url=url, headers=header)
    resp.encoding = 'utf-8'
    html = resp.text
    tree = etree.HTML(html)
    title = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[1]/a/text()')
    score = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[2]/div[2]/div[2]/span/text()')
    hx = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[1]/text()')
    cz_type = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[2]/text()')
    kz = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[3]/text()')
    price = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/div[2]/span/text()')
    img_url = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[2]/div[1]/a/img/@data-original')

    data = pd.DataFrame({
        '城市': city,
        '名字': title,
        '评分': score,
        '户型': hx,
        '出租类型': cz_type,
        '可住几人': kz,
        '价格': price,
        '图片地址': img_url
    })
    return data


if __name__ == '__main__':
    citys = ['beijing', 'shanghai']
    all_data = pd.DataFrame()
    for city in citys:
        for page in range(1, 11):
            print(f'正在爬取{city}第{page}页')
            time.sleep(2)
            data = spider(city, page)
            all_data = pd.concat([all_data, data], ignore_index=True)
    all_data.to_csv('data.csv', index=False)
