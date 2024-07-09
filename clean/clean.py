import pandas as pd

df = pd.read_csv('data.csv')
df.drop_duplicates(subset=['名字'])
df['名字'] = df['名字'].str.replace('𡶶', '峰')

df['评分'] = df['评分'].astype(str)
df['评分'] = df['评分'].str.strip()

df['价格'] = df['价格'].replace('￥', '', regex=True)

df['可住几人'] = df['可住几人'].str.extract('(\d+)').astype(int)

df.to_csv('clean.csv', index=False)
