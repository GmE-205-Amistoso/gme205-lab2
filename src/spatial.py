import math as Math

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