from spatial import PointSet

DATA_PATH = "../data/points.csv"

point_set = PointSet.from_csv(DATA_PATH)
print("No of points:", point_set.count())
print("Bounding box:", point_set.bbox())
filtered_set = point_set.filter_by_tag("poi")
print("No of points with tag 'poi':", filtered_set.count())

# q = Point("X", 999, 14)
# print(p.id, p.lon, p.lat)