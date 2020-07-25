from collections import namedtuple

metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)), ]

LatLong = namedtuple('LatLong', 'lat long')
Metropolis = namedtuple('Metropolis', 'name cc pop coord')
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_data]

# metro_areas[0]
# Out[3]: Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))
# metro_areas[0].coord.lat
# Out[4]: 35.689722

from operator import attrgetter

name_lat = attrgetter('name', 'coord.lat')  # 定义一个 attrgetter，获取 name 属性和嵌套的 coord.lat 属性
for city in sorted(metro_areas, key=attrgetter('coord.lat')):  # 使用 attrgetter，按照纬度排序城市列表。
    print(name_lat(city))  # 使用定义的 attrgetter, 即name_lat，只显示城市名和纬度。

# ('Sao Paulo', -23.547778)
# ('Mexico City', 19.433333)
# ('Delhi NCR', 28.613889)
# ('Tokyo', 35.689722)
# ('New York-Newark', 40.808611)
