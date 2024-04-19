class Coordinates:
    def __init__(self, dms: str):
        coords = dms.split('.')
        self.d = coords[0]
        self.m = int(coords[1])
        self.s = int(coords[2])
        self.decimal = 0
        if len(coords) > 3:
            self.decimal = int(coords[3])

    def __str__(self):
        return f"{self.d} {self.m} {self.s}.{self.decimal}"

    def dd(self):
        seconds = float(f"{self.s}.{self.decimal}")
        decimal = self.m/60 + (seconds/3600)
        return f"{self.d}{str(decimal)[1:]}"


class LatLong:
    def __init__(self, lat: Coordinates, lng: Coordinates):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return f"{self.lat} {self.lng}"

    def __repr__(self):
        return f"LatLong({self.lat}, {self.lng})"
