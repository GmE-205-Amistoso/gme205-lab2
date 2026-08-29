import math as Math
import pandas as pd

# ----------------------
# File paths
# ----------------------

class PointSet:
    def __init__(self, points=None):
        # Initialize the PointSet with a list of Point objects or an empty list if no data is in CSV.
        self.points = points or []

    # ---------------------------------------------------------------------------
    # Instance methods
    # ---------------------------------------------------------------------------
    def count(self):
        return len(self.points)

    def bbox(self) -> tuple[float, float, float, float] | None:
        """
        Calculate the bounding box of the points.
        Returns a tuple of (min_lon, min_lat, max_lon, max_lat).
        """
        if not self.points:
            return None

        min_lon = min(point.lon for point in self.points)
        max_lon = max(point.lon for point in self.points)
        min_lat = min(point.lat for point in self.points)
        max_lat = max(point.lat for point in self.points)

        return (min_lon, min_lat, max_lon, max_lat)

    def filter_by_tag(self, tag):
        filtered_points = []

        # Check individual points for the tag
        for point in self.points:
            if point.tag == tag:
                filtered_points.append(point)   # Add matching point to the filtered list

        return PointSet(filtered_points)

    # ---------------------------------------------------------------------------
    # Class methods
    # ---------------------------------------------------------------------------

    @classmethod
    def from_csv(cls, csv_file):
        points = []

        # Read the CSV file into df
        print(f"Reading points from {csv_file}...")
        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"Error: The file {csv_file} was not found.")
            print("Please ensure the file \"points.csv\" exists in the specified path.")
            exit(1)


        print(f"Parsing {len(df)} rows from the CSV file...")
        missing_values = df.isnull().sum()

        # Check for missing values in CSV
        if missing_values.any():
            print("Missing values per column:")
            print(missing_values)
        else:
            print("No missing values detected.")

        # Parse each row in CSV into a Point object
        for index, row in df.iterrows():
            try:
                point = Point.from_row(row)     # Create a Point object using the class method from_row
                points.append(point)
                #print(f"Added Point: {point.id}, Lon: {point.lon}, Lat: {point.lat}")
            except ValueError as e:
                print(f"Skipping row due to missing or invalid data.")

        return cls(points)  # Initialize the PointSet object
        

class Point:
    def __init__(self, id, lon, lat, name=None, tag=None):
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees.")

        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees.")
        
        self.id = id
        self.lon = lon
        self.lat = lat
        self.name = name
        self.tag = tag

    # ---------------------------------------------------------------------------
    # Instance methods
    # ---------------------------------------------------------------------------
    def to_tuple(self) -> tuple[float, float]:
        """
        Return the coordinate as a (lon, lat) tuple.
        """
        return (self.lon, self.lat)

    def distance_to(self, other):
        return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)

    def is_poi(self):
            return (self.tag or "").lower() == "poi"

    # ---------------------------------------------------------------------------
    # Static methods
    # ---------------------------------------------------------------------------

    @staticmethod
    def haversine_m(lon1:float, lat1:float, lon2:float, lat2:float) -> float:
        """
        Calculate the Haversine distance between two lat/lon points in meters.
        """
        R = 6_371_000.0     #Earth radius in meters

        phi1 = Math.radians(lat1)
        phi2 = Math.radians(lat2)
        dphi = Math.radians(lat2 - lat1)
        dlambda = Math.radians(lon2 - lon1)

        a = (
            Math.sin(dphi / 2.0) ** 2
            + Math.cos(phi1)
            * Math.cos(phi2)
            * Math.sin(dlambda / 2.0) ** 2
        )
        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

        return R * c

    # ---------------------------------------------------------------------------
    # Class methods
    # ---------------------------------------------------------------------------

    @classmethod
    def from_row(cls, row):
        return cls(
            id = row["id"], 
            lon = row["lon"], 
            lat = row["lat"], 
            name = row.get("name"), 
            tag = row.get("tag")
        )