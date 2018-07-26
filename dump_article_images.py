import MySQLdb

g_host = '10.104.26.243'
g_user = 'shard_user'
g_password = 'QB_20!50&@7'
g_database = 'qqq1'

conn = MySQLdb.connect(g_host, g_user, g_password, g_database)

cursor = conn.cursor()

with open('dump.sql', 'wb') as f:
    flag = True
    while (flag)
        s = 0
        sql = 'select pid from article_images where tag="image" order by id desc limit {}, {}; ' % (s, 2000)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            f.write(row[0]+'\n')

        s += 2000
        exit()

conn.close()
