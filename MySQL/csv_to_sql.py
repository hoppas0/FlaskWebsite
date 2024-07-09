import pymysql
import pandas as pd

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='bnb',
    charset='utf8'
)

cur = conn.cursor()


def createTable():
    create_table_sql = """
    create table if not exists bnb_data(
    id int primary key auto_increment,
    city varchar(255),
    name varchar(255),
    score varchar(255),
    hx varchar(255),
    cz_type varchar(255),
    kz varchar(255),
    price varchar(255),
    img_url varchar(255)
    )
    """
    cur.execute(create_table_sql)


def insertTable():
    df = pd.read_csv('clean.csv')
    insert_sql = "insert into bnb_data(city,name,score,hx,cz_type,kz,price,img_url) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cnt = 0
    for index, row in df.iterrows():
        cnt += 1
        if cnt <= 20:
            continue
        print(tuple(row))
        cur.execute(insert_sql, tuple(row))

        # if cnt >= 20:
        #     break
    conn.commit()

    # 检查已插入的数据
    cur.execute("SELECT count(*) FROM bnb_data")
    result = cur.fetchall()
    print(result)

    cur.close()
    if not conn.open:
        conn.close()


if __name__ == "__main__":
    createTable()
    insertTable()
