from spatial import Point

p = Point("A", 121.0, 14.6)
print(p.id, p.lon, p.lat)

q = Point("X", 999, 14)
print(p.id, p.lon, p.lat)