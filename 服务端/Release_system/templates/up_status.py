import pymysql, requests, re, json, time

date = time.strftime('%Y-%m-%d %H:%M:%S')
time.strptime(date, '%Y-%m-%d %H:%M:%S')
j = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
z = float(j) - 600

ltime = time.localtime(z)
timeStr = time.strftime("%Y%m%d%H%M%S", ltime)
datestrftime = time.strftime('%Y%m%d%H%M%S', ltime)
qian5mindate = time.strftime('%Y-%m-%d %H:%M:%S', ltime)

print(qian5mindate)
def insert_mysql(sql):
    conn = pymysql.connect(host='121.201.68.21', port=3307, user='jiang', passwd='jiangwenhui', db='Release_system',

                           charset='UTF8')

    cur = conn.cursor()

    cur.execute(sql)
    nRet = cur.fetchall()
    conn.commit()

    cur.close()

    conn.close()
    return nRet

if __name__=="__main__":
    sql="update app01_his_rel set status=0 where status=1 and relea_time<'{}'".format(qian5mindate)#sql时间小于10分钟之前
    insert_mysql(sql)
    sql = "update app01_his_rool set status=0 where status=1 and relea_time<'{}'".format(qian5mindate)
    insert_mysql(sql)
    print("ok")