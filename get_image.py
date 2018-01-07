import urllib, os
import google_streetview.api
import json
from os.path import join

META_FILE = 'images.json'
POINTS_FILE = 'points.json'
IMAGE_DIR = 'images'
URL = 'https://maps.googleapis.com/maps/api/streetview?size=1200x800&location={0},{1}&heading=175&pitch={2}&key=AIzaSyC-ouodO4ERCgJDjzku5_mghCBH0wribio'
image_counter = 1

def get_location(lat, lng, meta_file):
    global image_counter
    names = {}
    for i in (0,90,180,270):
        try:
            params = [{
                'size' : '640x640',
                'location' : '{0},{1}'.format(lat,lng),
                'pitch' : '35',
                'heading' : '{0}'.format(i),
                'key': 'AIzaSyC-ouodO4ERCgJDjzku5_mghCBH0wribio'
            }]

            image_name = str(image_counter) + '.jpg'
            names[str(i)] = image_name
            image_counter += 1

            r = google_streetview.api.results(params)
            r.download_links(IMAGE_DIR)


            os.rename(join(IMAGE_DIR, 'gsv_0.jpg'), join(IMAGE_DIR, image_name))

        except Exception, e:
            print e


    all_data = {'lat':lat, 'lng':lng, 'images':names}
    meta_file.write(json.dumps(all_data))

def main():
    meta = open(META_FILE, 'a')
    f = open(POINTS_FILE, 'r')
    data = json.loads(f.read())
    f.close()

    c = 0
    for i in data:
        print c
        try:
            get_location(i['lat'], i['lng'], meta)
        except Exception, e:
            print e

        c += 1

    meta.close()

if __name__ == '__main__':
    main()