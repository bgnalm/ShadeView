import json
import math

DATA_FILE = 'streets_data.json'
JUMP = 0.0014

telaviv_southwest = {'lat':32.033243, 'lng':34.742720}
telaviv_northeast = {'lat': 32.128343, 'lng': 34.841883}

def load_data(file_path):
    f = open(file_path, 'r')
    j = json.loads(f.read())
    f.close()
    return j

def generate_points(p1, p2, jump=JUMP):
    lat_diff = p1['lat'] - p2['lat']
    lng_diff = p1['lng'] - p2['lng']

    distance = math.sqrt(lat_diff * lat_diff + lng_diff * lng_diff)
    points_in_between = int(math.floor(distance/jump));

    points = []
    for i in range(1,points_in_between+1):
        new_lat = float(lat_diff * i) / (points_in_between+1) + p2['lat']
        new_lng = float(lng_diff * i) / (points_in_between+1) + p2['lng']
        points.append({'lat': new_lat, 'lng': new_lng})

    return points

def validate_point(point):
    if point['lat'] > telaviv_northeast['lat']:
        return False

    if point['lng'] > telaviv_northeast['lng']:
        return False

    if point['lat'] < telaviv_southwest['lat']:
        return False

    if point['lng'] < telaviv_southwest['lng']:
        return False

    return True

def generate_all_points(out):
    data = load_data(DATA_FILE)
    points = []
    for i in data:
        # check if point is in tel aviv:
        if validate_point(i['start']) and validate_point(i['end']):
            points.append(i['start'])
            points.append(i['middle'])
            points.append(i['end'])
            points += generate_points(i['start'], i['middle'])
            points += generate_points(i['middle'], i['end'])

    print len(points)
    f = open(out, 'w')
    f.write(json.dumps(points))
    f.close()


if __name__ == '__main__':
    generate_all_points('points.json')


