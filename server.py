from flask import Flask
app = Flask(__name__)
from flask import request
import requests
import json

import googlemaps

KEY = 'AIzaSyB7hFRySQ2mCR3ymlkDcOnqGxyoPqev1jM'
URL = 'https://maps.googleapis.com/maps/api/directions/json?mode=walking&origin={0},{1}&destination={2},{3}&key={4}'

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/route/')
@crossdomain(origin='*')
def route():
    lat1 = request.args.get('lat1')
    lng1 = request.args.get('lng1')
    lat2 = request.args.get('lat2')
    lng2 = request.args.get('lng2')


    url = URL.format(lat1, lng1, lat2, lng2, KEY)
    r = requests.get(url)
    route = r.json()['routes'][0]['legs']
    points = []
    for i in route:
        for j in i['steps']:
            points.append(j['start_location'])

    print points
    return json.dumps(points)

if __name__ == '__main__':
    app.debug = True
    app.run()

    # other setup tasks

