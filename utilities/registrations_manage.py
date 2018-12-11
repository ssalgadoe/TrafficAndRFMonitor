import re
import collections
import sys
import os
import numpy as np
import datetime
import MySQLdb as mysql




def remove_registrations(period):
    now = datetime.datetime.now()
    duration = now- datetime.timedelta(days=period)
    
    conn = mysql.connect(user='root', password='.....',host='127.0.0.1',database='.....')
    cursor = conn.cursor()
    sql= "delete from registrations_registrations where date(mk_time) < date('" + str(duration) + "')"
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    print("nr of rows", cursor.rowcount)
    cursor.execute('COMMIT')
    print('done')

   

remove_registrations(6)

