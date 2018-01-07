import json
from os.path import exists
from os.path import join
import math
from PIL import Image
from PIL import ImageFilter

IMAGE_DIR = '../images'
META_FILE = 'images2.json'
SHADE_PROFILE = 'shade_profile.json'

MAX_DIFF = 12

def diff(p1, p2):
    r1,g1,b1 = p1
    r2,g2,b2 = p2
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2

    return math.sqrt(dr * dr + dg * dg + db *db)

def get_sky_value(image_path):
    t1 = Image.open(join(IMAGE_DIR, image_path))
    t = t1.filter(ImageFilter.BLUR)
    last = [(x, 0) for x in range(t.width)]
    all_points = []

    while len(last) > 0:
        all_points += last
        new_last = []
        for i in last:
            x, y = i
            if y + 1 < t.height:
                if diff(t.getpixel((x, y)), t.getpixel((x, y + 1))) < MAX_DIFF:
                    new_last.append((x, y + 1))

        last = new_last

    t.close()
    return float(len(all_points))/(t.width * t.height)

locs = []

f = open(META_FILE, 'r')
data = json.loads(f.read())
f.close()

c = 0

for i in data:
    c += 1
    print c

    try:
        images = i['images']

        north_path = join(IMAGE_DIR, images['0'])
        east_path = join(IMAGE_DIR, images['90'])
        south_path = join(IMAGE_DIR, images['180'])
        west_path = join(IMAGE_DIR, images['270'])
        # check if the image exists
        if exists(north_path) and exists(east_path) and exists(south_path) and exists(west_path):
            north = get_sky_value(north_path)
            east = get_sky_value(east_path)
            south = get_sky_value(south_path)
            west = get_sky_value(west_path)

            locs.append({'lat': i['lat'], 'lng': i['lng'], 'north':north, 'east':east, 'south':south, 'west':west})

    except:
        pass

f = open(SHADE_PROFILE, 'w')
f.write(json.dumps(locs))
f.close()