import json

FILE = 'images.json'

data = []

f = open(FILE, 'r')
text = f.read()
f.close()

last = 0
new = 0

while last != -1 and new != -1:
    last = text.find('{"lat"', new)
    new = text.find('{"lat"', last+1)

    try:
        data.append(json.loads(text[last:new]))
    except:
        pass

f = open('images2.json', 'w')
f.write(json.dumps(data))
f.close()