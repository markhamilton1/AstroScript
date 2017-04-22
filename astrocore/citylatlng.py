import mathutils


CITIES = {}


def __readline(fref):
    line = fref.readline()
    while line:
        line = line.strip()
        if len(line) > 0:
            return line
        line = fref.readline()
    return None


def load(file="USCityLatLng.csv"):
    global CITIES
    with open(file, 'r') as fref:
        line = __readline(fref)
        while line:
            parts = line.split(',')
            city = unicode(parts[0])
            region = unicode(parts[1])
            lat = mathutils.to_float(parts[2])
            lng = mathutils.to_float(parts[3])
            key = city.lower()
            entry = (city, region, lat, lng)
            if CITIES.has_key(key):
                CITIES[key].append(entry)
            else:
                CITIES[key] = [entry]
            line = __readline(fref)


def lookup(city, region=None):
    global CITIES
    key = unicode(city.lower())
    if CITIES.has_key(key):
        entry = CITIES[key]
        if region is None:
            return entry
        for e in entry:
            if unicode(e[1].lower()) == unicode(region.lower()):
                return e
    return None


if __name__ == "__main__":


    load()
    e = lookup('Provo', 'UT')
    print(e)
