import csv
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyCDjLrnFnVPqfcUb7o3hkDPJjA8LTMaLZo')

def fetchAddress(address):
    try:
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
    except Exception:
        lat = 0.0
        lon = 0.0
        print("lat", lat, "lon", lon)
        return lat, lon

    print("lat", lat, "lon", lon)
    return lat, lon


with open('./Customer List Piped.CSV') as csvfile:
    cfile = csv.reader(csvfile, delimiter='|')
    headers = next(cfile, None) 
    custData = []
    for line in cfile:
        custData.append(line)

header = [val for i, val in enumerate(headers) if len(val) > 0]
noEmptyList = [i for i, val in enumerate(headers) if len(val) > 0]

header.append('lat')
header.append('lon')

data = []
for element in custData:
    validData = [element[i] for i in noEmptyList]
    validData.append(0.0)
    validData.append(0.0)
    data.append(validData)
    

dt = data[:10]
for idx, customer in enumerate(dt):
    address = ','.join([ele for ele in customer[1:-3] if len(ele) > 0])
    lat, lon = fetchAddress(address)
    dt[idx][-1] = lon
    dt[idx][-2] = lat

with open('./customerlistwith_test.csv', 'w', newline='\n') as csvfile:
    writeline = csv.writer(csvfile, delimiter='|')
    writeline.writerow(header)
    for d in dt:
        writeline.writerow(d)    