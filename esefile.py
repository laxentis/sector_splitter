from utils import LatLong


class Position:
    def __init__(self, name, callsign, frequency, identifier, middle_letter, prefix, suffix, ssr_start, ssr_end,
                 vis_lat=None, vis_lon=None):
        self.name = name
        self.callsign = callsign
        self.frequency = frequency
        self.identifier = identifier
        self.middle_letter = middle_letter
        self.prefix = prefix
        self.suffix = suffix
        self.ssr_start = ssr_start
        self.ssr_end = ssr_end
        self.vis_lat = vis_lat
        self.vis_lon = vis_lon

    @staticmethod
    def from_string(string):
        string = string.split(':')
        name = string[0]
        callsign = string[1]
        frequency = string[2]
        identifier = string[3]
        middle_letter = string[4]
        prefix = string[5]
        suffix = string[6]
        ssr_start = string[9]
        ssr_end = string[10]
        vis_lat = None
        if len(string) > 11:
            vis_lat = LatLong(string[11])
        vis_lon = None
        if len(string) > 12:
            vis_lon = LatLong(string[12])
        return Position(name, callsign, frequency, identifier, middle_letter, prefix, suffix, ssr_start, ssr_end,
                        vis_lat, vis_lon)

    def __str__(self):
        return f"{self.callsign} ({self.name} - {self.frequency})"


class ESE_File:
    Positions = set()
    file = None

    def __init__(self, file):
        self.file = open(file)

    def __del__(self):
        self.file.close()