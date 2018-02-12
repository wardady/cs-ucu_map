import folium
from geopy.geocoders import ArcGIS


def r_file(path):
    with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
        inp = {tuple(line.strip().split('\t')) for line in file}
        return inp


def film_dict(films, year):
    films_countries = dict()
    for film in films:
        if '(' + str(year) in film[0]:
            if '(' in film[-1] or ')' in film[-1]:
                pos = [film[-2], ]
            else:
                pos = [film[-1], ]
            if film[0] in films_countries:
                films_countries[film[0]] += pos
            else:
                films_countries[film[0]] = pos
    return films_countries


def get_pos(loc):
    geolocator = ArcGIS(timeout=10)
    location = geolocator.geocode(loc)
    return location.latitude, location.longitude


wrld_map = folium.Map(location=[0, 0], zoom_start=1)
film_map = folium.FeatureGroup(name='FilmsMap')
data = r_file('locations.list')
film_places = film_dict(data, int(input("Please, enter the year:")))
lmt = int(input("Enter amount of fillms, you want to locate on the map:"))
amount = 0
for key in film_places:
    if amount >= lmt:
        break
    print("Looking for the places where {0} was filmed".format(key))
    amount += 1
    for pos in film_places[key]:
        try:
            lat, lng = get_pos(pos)
            film_map.add_child(folium.Marker(location=[lat, lng], popup=key,
                                             icon=folium.Icon()))
        except:
            continue
population = folium.FeatureGroup(name='Population')
population.add_child(
    folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                    style_function=lambda x: {
                    'fillColor': 'green' if x['properties']['POP2005']
                    < 10000000 else 'orange' if 10000000 <=
                    x['properties']['POP2005'] < 20000000 else 'red'}))
wrld_map.add_child(population)
wrld_map.add_child(film_map)
wrld_map.add_child(folium.LayerControl())
wrld_map.save('Yavorskyi_webmap.html')

