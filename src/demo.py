from spatial import Point

p = Point("A", 121.0, 14.6)
print(p.id, p.lon, p.lat)
print(p.to_tuple())

print(p.distance_to(Point("B", 123.1, 15.7)))

# q = Point("X", 999, 14)
# print(p.id, p.lon, p.lat)