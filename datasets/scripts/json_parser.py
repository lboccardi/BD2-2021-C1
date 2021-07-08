import json

if __name__ == '__main__':

    f = open('restaurants.geojson', 'r')
    data = json.load(f)
    aux = []

    for r in data:
        obj = {
            "type": r["type"],
            "geometry": r["geometry"],
            "properties": {
                "address": r["properties"]["address"],
                "name": r["properties"]["name"]
            }
        }
        aux.append(obj)

    f.close()

    jsonFile = open('restaurants.json', 'w')
    jsonFile.write(json.dumps(aux))
    jsonFile.close()
