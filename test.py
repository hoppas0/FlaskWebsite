import csv

with open('spider/rank_2024_07_08.csv','r',encoding="utf-8-sig") as f:
    csv_reader = csv.reader(f)
    print(csv_reader)
    for row in csv_reader:
        print(row)


