import sys
import httplib
import json
import time
import string
import urllib
import codecs

cimfile =  open("input_for_geocode.txt", 'r')
parsed_addresses = cimfile.readlines()
conn = httplib.HTTPSConnection('maps.googleapis.com')
path =('/maps/api/geocode/json?')
lat = 0
lng = 0
writeline = "NA"+ '\n'
fd = open('output.txt','a')
api_key = 'AIzaSyA2YZzGA-KAXvJKxlho7yQ1V91E9rNnQYY'

for parsed_address in parsed_addresses:
        parsed_address = parsed_address.strip()
        pa2 = parsed_address
        parsed_address = parsed_address.decode('latin-1')
        parsed_address = parsed_address.encode('utf-8')
        values = {'address' : parsed_address, 'output': 'json', 'sensor' : 'false', 'key' : 'AIzaSyA2YZzGA-KAXvJKxlho7yQ1V91E9rNnQYY'}
        #values = {'address' : parsed_address, 'output': 'json', 'sensor' : 'false'}
        data = urllib.urlencode(values)
        csekk = path+data
        #print csekk
        conn.request('GET', path+data)
        r = conn.getresponse()
        if r.status == 200:
                jsonResponse = json.loads(r.read())
                addr_db = len(jsonResponse["results"])
                #print jsonResponse
                if jsonResponse['status'] <> 'ZERO_RESULTS':
                        lat = jsonResponse['results'][0]['geometry']['location']['lat']
                        lng = jsonResponse['results'][0]['geometry']['location']['lng']
                        addr_long = jsonResponse['results'][0]['formatted_address']
                if lat <> 0 or lng <> 0:
                        for x in range(0, (addr_db)):
                                lat = jsonResponse['results'][x]['geometry']['location']['lat']
                                lng = jsonResponse['results'][x]['geometry']['location']['lng']
                                addr_long = jsonResponse['results'][x]['formatted_address']
                                addr_lw = addr_long.encode('cp1250')
                                writeline = pa2 + ';' + str(lat) + ';' + str(lng) + ';' + addr_lw + ';' + 'OK;''' + str(x+1) + '|' + str(addr_db) + '\n'
                                fd.write(writeline)
                        print 'UPDATING address = %s, lat = %s, lng = %s' % (parsed_address, lat, lng)
                else:
                        writeline = pa2 + ';' + str(lat) + ';' + str(lng) + ';NA;NoLoc_ERR: %s' % r.status + ';0|1' + '\n'
                        fd.write(writeline)
                        print 'error: %s' % r.status
                        
        else:
                writeline = pa2 + ';' + str(lat) + ';' + str(lng) + ';NA;SYS_ERR:' + str(r.status) + '|' + str(r.reason) + ';0|1' + '\n'
                fd.write(writeline)
                print 'error: %s, reason: %s' % (r.status, r.reason)
        lat = 0
        lng = 0

fd.close()
conn.close
