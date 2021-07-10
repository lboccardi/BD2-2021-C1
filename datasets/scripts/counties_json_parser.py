import json

if __name__ == '__main__':

    f = open('us-county-boundaries.geojson', 'r')
    data = json.load(f)
    aux = []

    for r in data["features"]:
        obj = {
            "type": r["type"],
            "geometry": r["geometry"],
            "properties": {
                "name": r["properties"]["name"]
            }
        }
        aux.append(obj)

    f.close()

    jsonFile = open('../Parsed Datasets/Mongo/counties.json', 'w')
    jsonFile.write(json.dumps(aux))
    jsonFile.close()