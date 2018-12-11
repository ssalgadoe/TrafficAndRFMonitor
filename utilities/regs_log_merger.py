import re
import collections
import sys
import os
import shutil
import numpy as np
import datetime
import MySQLdb as mysql



month2text = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06','jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}


regEx1 = r"^(#.*)"
regEx2 = r"^([0-9]+) (.*)"

def extractTime(s):
    week=day=hour=sec=minute=0
    
    pos = s.find('w')
    if pos != -1:
        week = s[:pos]
        s = s[pos+1:]

    
    pos = s.find('d')
    if pos != -1:
        day = s[:pos]
        s = s[pos+1:]

    pos = s.find('h')
    if pos != -1:
        hour = s[:pos]
        s = s[pos+1:]

    pos = s.find('m')
    if pos != -1:
        minute = s[:pos]
        s = s[pos+1:]

    pos = s.find('s')
    if pos != -1:
        sec = s[:pos]
        s = s[pos+1:]

   
    total = int(week)*7*24*3600 +int(day)*24*3600+ int(hour)*3600 + int(minute)*60+ int(sec)        
    return round(total/3600.)


def file_transfer_from_212():
    #src_folder = 'z:/registrations/'
    src_folder = '//...../log-data//registrations/'
    dst_folder = '../data/registrations/'
    listing = os.listdir(src_folder)
    for item in listing:
        if '.csv' in item:
            src_file = src_folder + str(item)
            dst_file = dst_folder + str(item)
            #print(src_file, dst_file)
            shutil.copy(src_file,dst_file)
            os.remove(src_file)




def readBlock( fileHandle, line):
    item_list = dict()
    rows = line.split()
##    print(rows)
    items = [ ele.split('=')   for ele in rows]
    #print(items)
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
            #print(items)
            for i in range(len(items)):
                try:
                    item_list[items[i][0]] = items[i][1]
                except Exception as ex:
                    continue

        
        
    signal_strength = '0'
    if 'signal-strength' in item_list:
        signal_strength = item_list['signal-strength']
        signal_strength = signal_strength[0:3]
        if int(signal_strength) < -100 or int(signal_strength) > 0:
            signal_strength = '0'
##        print('signal', signal_strength)
##        if '@6Mbps' in signal_strength:
##            pos = signal_strength.find('@6Mbps')
##            signal_strength = signal_strength[0:pos]
##        if 'dBm@' in signal_strength:
##            pos = signal_strength.find('dBm@')
##            signal_strength = signal_strength[0:pos]
##            print('signal stren', signal_strength)
        
    packets = '0,0'
    if 'packets' in item_list:
        packets = item_list['packets']        

    bytes_ = '0,0'
    if 'bytes' in item_list:
        bytes_ = item_list['bytes'] 

    uptime = '0s'
    if 'uptime' in item_list:
        uptime = item_list['uptime']

    signal_to_noise = '0dB'
    if 'signal-to-noise' in item_list:
        signal_to_noise = item_list['signal-to-noise']

    rx_ccq = '0%'
    if 'rx-ccq' in item_list:
        rx_ccq = item_list['rx-ccq']        

    tx_ccq = '0%'
    if 'tx-ccq' in item_list:
        tx_ccq = item_list['tx-ccq'] 

    frames = '0,0'
    if 'frames' in item_list:
        frames = item_list['frames'] 


    distance = '0'
    if 'distance' in item_list:
        distance = item_list['distance']


    last_ip = '0'
    if 'last-ip' in item_list:
        last_ip = item_list['last-ip']

    mac_address = '0'
    if 'mac-address' in item_list:
        mac_address = item_list['mac-address']
		
    radio_name = '0'
    if 'radio-name' in item_list:
        radio_name = item_list['radio-name']
        radio_name = radio_name.replace('"','')
        if not '^' in radio_name:
            radio_name = radio_name + '^'

    
    output = [mac_address,signal_strength,packets,bytes_,uptime, signal_to_noise,rx_ccq,tx_ccq,frames,distance,last_ip,radio_name]  
    return (output)
 
def remove_registrations(period):
    now = datetime.datetime.now()
    duration = now- datetime.timedelta(days=period)
    
    conn = mysql.connect(user='.....', password='.....',host='.....',database='.....')
    cursor = conn.cursor()
    sql= "delete from registrations_registrations where date(mk_time) < date('" + str(duration) + "')"
    #print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    #print("nr of rows", cursor.rowcount)
    cursor.execute('COMMIT')

    
            

def saveToDB(logFile, mk_time,radio_data):
    filteredList = []

    for line in logFile:
        if re.search(regEx2, line.lstrip()):
            output = readBlock(logFile,line)
            filteredList.append(output)

    ds = np.array(filteredList)

    #ds[:,1] = [ele[:-3] for ele in ds[:,1]]
    ds[:,5] = [ele[:-2] for ele in ds[:,5]]
    ds[:,6] = [ele[:-1] for ele in ds[:,6]]
    ds[:,7] = [ele[:-1] for ele in ds[:,7]]
    ds[:,9] = [ele for ele in ds[:,9]]

    #adding 2 additional rows with zero filled

    ds = np.hstack((ds, np.zeros((ds.shape[0], 4), dtype=ds.dtype)))

               
    ds[:,12] = [s for s in ds[:,4]]
    ds[:,13] = [s[:s.find('^')] for s in ds[:,11]]
    ds[:,14] = [s[s.find('^'):] for s in ds[:,11]]
    ds[:,15] = [extractTime(s) for s in ds[:,4]]
   
    ds = np.delete(ds,[2,3,4,8],axis=1)
    now = datetime.datetime.now()
    time_stamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)  + ' ' + str(now.hour)  + ':'  + str(now.minute) + ':00'
    mk_stamp = mk_time[-4] + '-' + month2text[mk_time[-6]] + '-' + mk_time[-5] + ' ' + mk_time[-3] + ':' + mk_time[-2] + ':00'
    rest = mk_time[0]
    for i in mk_time[1:-6]: rest=rest + '_' + i
    device_name = rest
    #print(device_name)
    device_name = device_name.replace('(','_')
    device_name = device_name.replace(')','_')
    device_name = device_name.replace(' ','')
    device_name = device_name.replace(',','')
    conn = mysql.connect(user='.....', password='.....',host='.....',database='.....')
    cursor = conn.cursor()
    tower_id = radio_data[0]
    frequency = radio_data[1]


    default_lat_id = "43.911823"
    default_lon_id = "-79.524228"
    default_ip = "0.0.0.0"
    
    sql = "select * from registrations_towers where loc_id='"+tower_id + "'"
    cursor.execute(sql)
    row = cursor.fetchall()
    if cursor.rowcount == 0:
        temp_str = "not assigned"
        sql = "insert into registrations_towers (loc_id, name, address, lon_id, lat_id) values ('"+ tower_id + "','" + temp_str + "','" + temp_str + "','" +str(default_lon_id) + "','" + str(default_lat_id) + "')"
        cursor.execute(sql)
        print('added',device_name)
        cursor.execute('COMMIT')
        sql = "select * from registrations_towers where loc_id='"+tower_id + "'"
        cursor.execute(sql)
        row = cursor.fetchone()
        loc_id = row[5]
        lat_id = row[4]
        lon_id = row[3]
        address = row[2]
    else:
        loc_id = row[0][5]
        lat_id = row[0][4]
        lon_id = row[0][3]
        address = row[0][2]

    default_lat_id = lat_id
    default_lon_id = lon_id        
    
    sql = "select * from registrations_aps where name='"+device_name + "'"
    cursor.execute(sql)
    row = cursor.fetchall()
   
    if cursor.rowcount == 0:
        sql = "insert into registrations_aps (name, ip, frequency, loc_id, lon_id, lat_id) values ('"+ device_name + "','" + str(default_ip) + "','" + str(frequency) + "','" + str(loc_id) + "','" + str(lon_id) + "','" + str(lat_id) + "')"
        cursor.execute(sql)
        cursor.execute('COMMIT')
        sql = "select * from registrations_aps where name='"+device_name + "'"
        cursor.execute(sql)
        row = cursor.fetchone()
        ap_id = row[0]
        frequency = row[5]
    else:
        ap_id = row[0][0]
        frequency = row[0][5]

    #print("frequency", frequency)    
    for item in ds:
        comment_ = item[7]
        cust_name = item[9]
        comment_ = comment_[comment_.find('^')+1:]
        sql = "select * from registrations_customers where name='"+cust_name + "'"
        cursor.execute(sql)
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            sql = "insert into registrations_customers (name, loc_id, ap_id, frequency, lon_id, lat_id) values ('"+ cust_name + "','" + str(loc_id)+ "','" + str(ap_id) + "','" + str(frequency) + "','" + str(default_lon_id) + "','" + str(default_lat_id) + "')"
            cursor.execute(sql)
            cursor.execute('COMMIT')
            sql = "select * from registrations_customers where name='"+cust_name + "'"
            cursor.execute(sql)
            row = cursor.fetchone()
            cust_id = row[0]
        else: 
            cust_id = row[0][0]
            

        sql = "insert into registrations_registrations (ap_id, cust_id, loc_id, mac, rssi,snr, ccq_rx, ccq_tx, distance, ip,comment, uptime,uptime_sec, cust_name,time_st,mk_time,device_name) values ('" + str(ap_id) + "','" + str(cust_id) + "','" + str(loc_id) + "','" + item[0]+"','" +item[1]+"','" + item[2]+"','" +item[3]+"','" + item[4]+"','" +item[5]+"','" + item[6]+"','" + comment_+"','"+ item[8]+"','" + item[11]+"','" +item[9]+"','"+ time_stamp+ "','" + mk_stamp + "','" + device_name +  "')"
       # print(sql)
        cursor.execute(sql)

    cursor.execute('COMMIT')
    cursor.close()
    conn.close()

    print('.', end="")



# old data (60 days) is removed from the data base automatically
remove_registrations(60)


now = datetime.datetime.now()
time_stamp = str(now.year) + str(now.month) + str(now.day) + str(now.hour)  +  str(now.minute) + str(now.second)

folder_loc = '../data/registrations/'
arc_folder_loc = './data/reg_data/archive/'
listing = os.listdir(folder_loc)
for item in listing:
    if '.csv' in item:
        mk_time_stamp = item.split('_')
        #print(mk_time_stamp)
        radio_data = mk_time_stamp[-1]
        radio_info= radio_data.split('##')
        radio_info = radio_info[1:-1]
        #print('radio_info', radio_info)
        src_file = folder_loc + str(item)
        dst_file = arc_folder_loc + str(item) + '_' + time_stamp
        #print(src_file, dst_file)
        logFile = open(src_file,'r')
        try:
            saveToDB(logFile,mk_time_stamp,radio_info)
        except IndexError as e:
            print("corrupted log file",src_file, e)
            logFile.close()
            os.remove(src_file)
            continue
        logFile.close()
        #os.rename(src_file,dst_file)
        os.remove(src_file)

file_transfer_from_212()

