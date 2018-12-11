import re
import collections
import sys
import os
import numpy as np
import datetime
import MySQLdb as mysql

logfile = './data/queues/mk1/q_test_data.csv'



month2text = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06','jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}


regEx1 = r"^(#.*)"
regEx2 = r"^([0-9]+) (.*)"
regEx3 = r"^MK(.*)"
regEx4 = r"^([0-9]+ X) (.*)"
regEx5 = r"^([0-9]+ XI) (.*)"
pppoe = 'pppoe'




    

def readBlock( fileHandle, line):
    item_list = dict()
    rows = line.split()
##    print(rows)
    items = [ ele.split('=')   for ele in rows]
##    print(items)
    for i in range(len(items)):
        try:
            item_list[items[i][0]] = items[i][1]
        except Exception as ex:
            continue
        
    while True:
        line = fileHandle.readline()
        if line.strip()=='' or re.search(regEx1, line.lstrip()):
            break
        else:
            rows = line.split()
            items = [ ele.split('=')   for ele in rows]
            for i in range(len(items)):
                try:
                    item_list[items[i][0]] = items[i][1]
                except Exception as ex:
                    continue

       
    name = ''
    if 'name' in item_list:
        name = item_list['name']
        name = name.replace('"','')

    target = '0,0'
    if 'target' in item_list:
        target = item_list['target'] 

    bytes_ = '0'
    if 'bytes' in item_list:
        bytes_ = item_list['bytes']

    packets_ = '0'
    if 'packets' in item_list:
        packets_ = item_list['packets']

    dropped = '0'
    if 'dropped' in item_list:
        dropped = item_list['dropped']        

    output = [name,target,bytes_,packets_,dropped]  

    return output

def remove_queues(period):
    now = datetime.datetime.now()
    duration = now- datetime.timedelta(days=period)
    
    conn = mysql.connect(user='root', password='.....',host='.....',database='.....')
    cursor = conn.cursor()
    sql= "delete from queues_queue_data where date(mk_time) < date('" + str(duration) + "')"
    #print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
##    #print("nr of rows", cursor.rowcount)
##    sql= "delete from queues_queue_data where b_tx = 0 or b_rx = 0"
##    #print(sql)
##    cursor.execute(sql)
##    rows = cursor.fetchall()
##    print("nr of rows had empty data", cursor.rowcount)
    cursor.execute('COMMIT')

    

def saveToDB(logFile, mk_time):            
    filteredList = []
    for line in logFile:
        if re.search(regEx2, line.lstrip()) and not re.search(regEx4, line.lstrip()) and not re.search(regEx5, line.lstrip()) and pppoe not in line:
            output = readBlock(logFile,line)
            filteredList.append(output)
 

    ds = np.array(filteredList)
    ds = np.hstack((ds, np.zeros((ds.shape[0], 6), dtype=ds.dtype)))
    ds[:,0] = [s if s.find('_[') == -1 else s[:s.find('_[')] for s in ds[:,0]]
    ds[:,1] = [s[:s.find('/')] for s in ds[:,1]]
    list_a = []
    list_b = []

    for ele in ds[:,2]:
        e_t, e_r = ele.split('/')
        list_a.append(e_t)
        list_b.append(e_r)

    ds[:,5] = np.array(list_a)
    ds[:,6] = np.array(list_b)

    list_a = []
    list_b = []

    for ele in ds[:,3]:
        e_t, e_r = ele.split('/')
        list_a.append(e_t)
        list_b.append(e_r)

    ds[:,7] = np.array(list_a)
    ds[:,8] = np.array(list_b)

    list_a = []
    list_b = []
    for ele in ds[:,4]:
        e_t, e_r = ele.split('/')
        list_a.append(e_t)
        list_b.append(e_r)

    ds[:,9] = np.array(list_a)
    ds[:,10] = np.array(list_b)

    ds = np.delete(ds,[2,3,4],axis=1)

    now = datetime.datetime.now()
    
##    '2012-06-18 10:34:09'
    time_stamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)  + ' ' + str(now.hour)  + ':'  + str(now.minute) + ':00'
    mk_stamp = mk_time[-4] + '-' + month2text[mk_time[-6]] + '-' + mk_time[-5] + ' ' + mk_time[-3] + ':' + mk_time[-2] + ':00'
##    print(mk_stamp)
    
    rest = mk_time[0]
    for i in mk_time[1:-6]: rest=rest + '_' + i
    device_name = rest
    #print(device_name)

    conn = mysql.connect(user='root', password='dupa@123',host='127.0.0.1',database='routcom')
    cursor = conn.cursor()
    for item in ds:
        sql = "select * from queues_queues where name='"+item[0] + "'"
        cursor.execute(sql)
        row = cursor.fetchall()
        queue_owner = item[0]
        if cursor.rowcount == 0:
            sql = "insert into queues_queues (name, ip,device_name) values ('"+item[0]+"','" +item[1]+"','" + device_name + "')"
            cursor.execute(sql)
            print('added',item[0])
            cursor.execute('COMMIT')
            sql = "select * from queues_queues where name='"+item[0] + "'"
            queue_owner = item[0]
            cursor.execute(sql)
            row = cursor.fetchone()
            queue_id = row[0]
        else:
            queue_id = row[0][0]
            
        #print('row details', row[0][0])
        sql = "insert into queues_queue_data (queue_id, owner,ip,b_tx, b_rx, p_tx, p_rx, drop_tx,drop_rx,time_st,mk_time) values ('"+str(queue_id)+"','" + queue_owner +"','" +item[1]+"','" + item[2]+"','" +item[3]+"','" + item[4]+"','" +item[5]+"','" + item[6]+"','" + item[7]+ "','"+ time_stamp+ "','" + mk_stamp + "')"
        #print(sql)
        if int(item[2]) > 0 and int(item[3]) > 0:
            cursor.execute(sql)
        
    cursor.execute('COMMIT')


    cursor.close()
    conn.close()

    print('.', end="")


    

# old data (60 days) is removed from the data base automatically
remove_queues(10)
    
now = datetime.datetime.now()
time_stamp = str(now.year) + str(now.month) + str(now.day) + str(now.hour)  +  str(now.minute) + str(now.second)

folder_loc = '../data/queues/'
arc_folder_loc = './data/queues/mk1/archive/'
listing = os.listdir(folder_loc)
for item in listing:
    if re.search(regEx3, item) and '.csv' in item:
        mk_time_stamp = item.split('_')
        #print(mk_time_stamp)
        src_file = folder_loc + str(item)
        dst_file = arc_folder_loc + str(item) + '_' + time_stamp
        #print(src_file, dst_file)
        logFile = open(src_file,'r')
        try:
            #print(src_file)
            saveToDB(logFile, mk_time_stamp)
        except IndexError as e:
            print("corrupted log file",e)
            continue       
        logFile.close()
##        os.rename(src_file,dst_file)
        os.remove(src_file)


