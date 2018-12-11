import socket
import os

path = "c:\www\monitor"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('.....',8081))
if result == 0:
   print ("Port is open")
else:
    os.chdir(path)
    os.system("python manage.py runserver .....:8081")
    print ("Port is not open")
