import sys
import os
import shutil



src_folder = 'z:/registrations/'
dst_folder = '../data/registrations/'
listing = os.listdir(src_folder)
for item in listing:
    if '.csv' in item:
        src_file = src_folder + str(item)
        dst_file = dst_folder + str(item)
        #print(src_file, dst_file)
        shutil.copy(src_file,dst_file)
        os.remove(src_file)
         
        
