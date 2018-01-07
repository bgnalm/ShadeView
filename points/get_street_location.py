# coding=utf-8
import json
import googlemaps

STREETS_FILE = 'streets.txt'
TEL_AVIV = ' תל אביב'
KEY = 'AIzaSyC-ouodO4ERCgJDjzku5_mghCBH0wribio'

def get_all_streets(file_name):
    f = open(file_name, 'r')
    data = f.read()
    f.close()
    return data.splitlines()

def get_locations(out_file):
    streets = set(get_all_streets(STREETS_FILE))

    c = 0

    collected_data = []
    g = googlemaps.Client(key=KEY)
    for i in streets:
        c += 1
        print c
        try:
            street_start = g.geocode(i + ' 1 ' + TEL_AVIV)[0]['geometry']['location']
            street_middle = g.geocode(i + TEL_AVIV)[0]['geometry']['location']
            street_end = {u'lat' : street_middle['lat'] - street_start['lat'] + street_middle['lat'],
                          u'lng' : street_middle['lng'] - street_start['lng'] + street_middle['lng']
            }

            collected_data.append({'name': i, 'start':street_start, 'middle': street_middle, 'end': street_end})
        except Exception, e:
            print e

    f = open(out_file, 'w')
    f.write(json.dumps(collected_data))

if __name__ == '__main__':
    get_locations('streets_data.json')
