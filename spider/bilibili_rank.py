from selenium import webdriver
from selenium.webdriver.edge.options import Options
from time import sleep
from lxml import etree
import datetime
import csv
import json


def get_video_info(li):
    rank = li.get("data-rank")
    BV = li.xpath('.//a[@class="title"]/@href')[0].split('/')[-1]
    title = li.xpath('.//a[@class="title"]/@title')[0]
    img = li.xpath('.//img[@class="lazy-image cover"]/@data-src')[0]
    up_name = li.xpath('.//span[@class="data-box up-name"]/text()')[0].strip()
    plays, barrage = [item.strip() for item in li.xpath('.//span[@class="data-box"]/text()')]

    return {
        "rank": rank,
        "BV": BV,
        "title": title,
        "img": img,
        "up_name": up_name,
        "plays": plays,
        "barrage": barrage
    }


def get_video_ranking():
    video_list = []
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("start-maximized")
    edge_options.add_argument("--headless")

    with webdriver.Edge(options=edge_options) as edge_browser:
        url = "https://www.bilibili.com/v/popular/rank/all"
        edge_browser.get(url)
        sleep(2)
        html = edge_browser.page_source
        tree = etree.HTML(html)
        li_list = tree.xpath('//li[@class="rank-item"]')

        for li in li_list:
            video_info = get_video_info(li)
            video_list.append(video_info)

    return video_list


if __name__ == "__main__":
    video_list = get_video_ranking()

    # 设置CSV文件保存路径和文件名
    current_date = datetime.datetime.now().strftime('%Y_%m_%d')
    csv_file = f"rank_{current_date}.csv"

    # 将视频信息写入CSV文件
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["rank", "BV", "title", "img", "up_name", "plays", "barrage"])

        # 写入表头
        writer.writeheader()

        # 写入每个视频的信息
        for video_info in video_list:
            writer.writerow(video_info)

    print(f"视频信息已保存至{csv_file}文件。")

    # # 设置JSON文件保存路径和文件名
    # json_file = "video_ranking.json"
    #
    # # 将视频信息写入JSON文件
    # with open(json_file, "w", encoding="utf-8") as file:
    #     json.dump(video_list, file, ensure_ascii=False, indent=4)
    #
    # print(f"视频信息已保存至{json_file}文件。")
