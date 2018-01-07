import json
import matplotlib.pyplot as plt
import numpy as np
import math

distances = []
f = open('streets_data.json', 'r')
data = f.read()
s = json.loads(data)
for i in s:
    lat_diff = abs(i['start']['lat'] - i['end']['lat'])
    lng_diff = abs(i['start']['lng'] - i['end']['lng'])

    distances.append(math.sqrt(lat_diff*lat_diff + lng_diff * lng_diff))

while 0 in distances:
    distances.remove(0)

np_distances = np.array(distances)
plt.hist(np_distances, range=[0,0.01])
plt.title("street length")
plt.xlabel("length")
plt.ylabel("Frequency")
plt.show()


