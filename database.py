import pymysql
import datetime

def insert(outsideTemp, insideTemp, targetTemp, fanState):
    sql = "INSERT INTO FANS ( `time`, `outside_temp`, `inside_temp`, `target_temp`, `fan_state`) "
    sql += "VALUES ( \"{0}\", {1}, {2}, {3}, {4})".format(datetime.datetime.now(), outsideTemp, insideTemp, targetTemp, fanState)
    try:
        connection = pymysql.connect(host='localhost', db='fans')
        #connection = pymysql.connect(host='localhost', user='root', db='fans', password='c0staRic4')
        #connection = pymysql.connect(host='localhost', user='pi', db='fans')
        cursor = connection.cursor()
        #print(sql)
        cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()

def select_today():
    sql = "SELECT * FROM FANS WHERE DATE(time)=CURRENT_DATE()"
    try:
        connection = pymysql.connect(host='localhost', db='fans')
        cursor = connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
    finally:
        connection.close()
    return result
'''

CREATE TABLE `FANS` (
	`time` TIMESTAMP NOT NULL,
	`outside_temp` FLOAT NOT NULL,
	`inside_temp` FLOAT NOT NULL,
	`target_temp` FLOAT NOT NULL,
	`fan_state` BOOLEAN NOT NULL,
	PRIMARY KEY (`time`)
);

INSERT INTO fans ( `time`, `outside_temp`, `inside_temp`, `fan_state`)
VALUES ( datetime.datetime.now(), 56.7, 74.0, TRUE )
'''